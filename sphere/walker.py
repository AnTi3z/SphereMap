import logging
import random
import time

import networkx as nx
from telethon import events

from .db_models import *
from .sphere import BOT_ID, global_state, Task
from button_clicker import ButtonClicker

logger = logging.getLogger('Sphere.walker')
logger.setLevel(logging.INFO)

# Global vars
nx_map = nx.Graph()
dst_room = None

MODULE_CFG = {}


def load_graph(graph, w1=1.0, w2=1.0):
    filtered_types = (4, 7)
    for passage in (PassagesView
                    .select(PassagesView.start_x, PassagesView.start_y, PassagesView.start_type,
                            PassagesView.end_x, PassagesView.end_y, PassagesView.end_type)
                    .where(PassagesView.start_type.not_in(filtered_types))
                    .where(PassagesView.end_type.not_in(filtered_types))):

        start_room = (passage.start_x, passage.start_y)
        end_room = (passage.end_x, passage.end_y)

        if passage.start_type != 3 and passage.end_type != 3:
            graph.add_edge(start_room, end_room, weight=1)
        elif passage.start_type == 3 and passage.end_type == 3:
            graph.add_edge(start_room, end_room, weight=w2)
        else:
            graph.add_edge(start_room, end_room, weight=w1)
    database.close()


def generate_dst(src):
    logger.debug("Generating new dst point!")
    if not src:
        logger.warning("Can't generate path from None room")
        return None

    while True:
        # Генерируем произвольные координаты
        dst = random.choice(list(nx_map.nodes))
        # Проверяем построение маршрута
        if nx.has_path(nx_map, src, dst):
            return dst


_heal_re = r"Твоё ❤️ здоровье и 🛡 щит полностью восстановились!"
_town_re = r"(?s)^Ты находишься на 🏡(.+?) (\d+)\s+(.+)"


# Возвращалка в город
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_heal_re))
async def auto_return(event):
    if MODULE_CFG['auto_return']:
        time.sleep(random.uniform(1.1, 2.5))
        await event.respond("🔮 Сфериум")
        time.sleep(random.uniform(1.1, 2.5))
        await event.respond("🏡 Прогулка по городу")


@events.register(events.MessageEdited(chats=(BOT_ID,), pattern=_town_re))
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_town_re))
async def town_handler(event):
    global dst_room
    clicker = ButtonClicker.get_clicker(BOT_ID)

    # Если включена тренировка, и мы у тренера - жмём её
    button = clicker.find_button(event, data='cwa_training')
    if button and MODULE_CFG['training']:
        await clicker.click(button)
        return

    # Если нарвались на торговца, телепорт и т.п. жмем "Уйти"
    button = clicker.find_button(event, data='cwa_nothing')
    if button:
        await clicker.click(button)
        return

    # Если нет других заданий - включаем автогуляние
    if not global_state['task']:
        global_state['task'] = Task.WALKING

    # Если текущее задание не гулять - возвращаемся в бараки
    if global_state['task'] != Task.WALKING:
        await clicker.click_cb_data(event, 'cwgoto_-1_-1')
        return

    # Координаты текущей комнаты
    x = Streets.get_or_none(Streets.name == event.pattern_match.group(1)).x
    database.close()
    y = int(event.pattern_match.group(2))
    cur_room = (x, y)

    # Если конечная точка не определена или мы уже в конечной точке
    if (dst_room is None) or (cur_room == dst_room):
        # Генерируем новую конечную точку
        dst_room = generate_dst(cur_room)
        if dst_room:
            logger.debug(f"New dst point generated!")

    # Если не достигли цели или у нас новая цель
    if dst_room and (cur_room != dst_room):
        try:
            # Строим маршрут до цели и берем следующую точку в маршруте
            next_room = nx.shortest_path(nx_map, cur_room, dst_room, weight='weight')[1]
        except nx.NetworkXNoPath:
            # До цели нет маршрута
            logger.warning(f"NO PATH to dst point!")
            dst_room = None
            return

        # data для кнопки в следующую точку
        next_btn_data = f"cwgoto_{next_room[0]}_{next_room[1]}"

        # Если такая кнопка есть в списке - давим ее
        await clicker.click_cb_data(event, next_btn_data)


def activate():
    load_graph(nx_map, 0.1, 0.01)
    logger.info("Sphere.Walker script activated")


def deactivate():
    logger.info("Sphere.Walker script deactivated")


HANDLERS = (town_handler, auto_return)
