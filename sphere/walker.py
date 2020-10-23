import logging
import random
import time

import networkx as nx
from telethon import events, errors

from .db_models import *
from . import tasks
from .sphere import BOT_ID


logger = logging.getLogger('Sphere.walker')
logger.setLevel(logging.INFO)

nx_map = nx.Graph()
cur_room = None
dst_room = None

WALKER_CFG = {}


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


def generate_dst():
    logger.debug("Generating new dst point!")
    if not cur_room:
        logger.warning("Can't generate path from None room")
        return None

    while True:
        # Генерируем произвольные координаты
        dst = random.choice(list(nx_map.nodes))
        # Проверяем построение маршрута
        if nx.has_path(nx_map, cur_room, dst):
            return dst


# Возвращалка в город
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=r"Твоё ❤️ здоровье и 🛡 щит полностью восстановились!"))
async def auto_return(event):
    if WALKER_CFG['auto_return']:
        time.sleep(random.uniform(1.1, 2.5))
        await event.message.respond("🔮 Сфериум")
        time.sleep(random.uniform(1.1, 2.5))
        await event.message.respond("🏡 Прогулка по городу")


@events.register(events.MessageEdited(chats=(BOT_ID,), pattern=r"(?s)^Ты находишься на 🏡(.+?) (\d+)\s+(.+)"))
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=r"(?s)^Ты находишься на 🏡(.+?) (\d+)\s+(.+)"))
async def town_handler(event):
    global cur_room
    global dst_room

    # Загружаем кнопки в список
    btn_data = list()
    for row in event.message.buttons:
        for btn in row:
            btn_data.append(btn.data.decode('utf-8'))

    # Если включена тренировка, и мы у тренера - жмём её
    if 'cwa_training' in btn_data and WALKER_CFG['training']:
        time.sleep(random.uniform(1.1, 2.5))
        await event.message.click(data=b'cwa_training')
        return

    # Если нарвались на торговца, телепорт и т.п. жмем "Уйти"
    if 'cwa_nothing' in btn_data:
        time.sleep(random.uniform(1.1, 2.5))
        await event.message.click(data=b'cwa_nothing')
        return

    # Проверяем текущее задание и настройку автогуляния
    if tasks.CURRENT_TASK == tasks.Task.NONE and WALKER_CFG['auto_walk']:
        tasks.CURRENT_TASK = tasks.Task.WALKING
    elif tasks.CURRENT_TASK == tasks.Task.WALKING and not WALKER_CFG['auto_walk']:
        tasks.CURRENT_TASK = tasks.Task.NONE

    # Если текущее задание не гулять - возвращаемся в бараки
    if tasks.CURRENT_TASK not in (tasks.Task.WALKING, tasks.Task.NONE):
        time.sleep(random.uniform(1.1, 2.5))
        try:
            await event.message.click(data=b'cwgoto_-1_-1')
        except errors.rpcerrorlist.BotResponseTimeoutError:
            logger.warning(f"Goto barracks button answer timeout")
        return

    # Координаты текущей комнаты
    x = Streets.get_or_none(Streets.name == event.pattern_match.group(1)).x
    database.close()
    y = int(event.pattern_match.group(2))
    cur_room = (x, y)

    # # Если включено авто-гуляние
    # if WALKER_CFG['auto_walk']:
    # Если конечная точка не определена или мы уже в конечной точке
    if (dst_room is None) or (cur_room == dst_room):
        # Генерируем новую конечную точку
        dst_room = generate_dst()
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
        if next_btn_data in btn_data:
            time.sleep(random.uniform(1.3, 4.5))
            try:
                await event.message.click(data=next_btn_data.encode('utf-8'))
            except errors.MessageIdInvalidError:
                logger.warning(f"Message with {next_btn_data} was deleted")


def activate(client, walker_cfg):
    global WALKER_CFG
    WALKER_CFG = walker_cfg
    load_graph(nx_map, 0.1, 0.01)
    client.add_event_handler(town_handler)
    client.add_event_handler(auto_return)
    # if WALKER_CFG['auto_walk']:
    #     tasks.CURRENT_TASK = tasks.Task.WALKING
    logger.info("Walker script activated")


def deactivate(client):
    client.remove_event_handler(town_handler)
    client.remove_event_handler(auto_return)
    logger.info("Walker script deactivated")
