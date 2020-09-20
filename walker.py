from telethon import events, functions
from db_models import *
import networkx as nx
import logging
import time
import random

logger = logging.getLogger('SphereMap_walker')
logger.setLevel(logging.DEBUG)

nx_map = nx.Graph()
cur_room = None
dst_room = None
AUTO_WALK = True
DO_TRAINING = True  # очко Тренера


def load_graph(graph):
    filtered_types = (4, 7)
    for passage in (PassagesView
                    .select(PassagesView.start_x, PassagesView.start_y, PassagesView.end_x, PassagesView.end_y)
                    .where(PassagesView.start_type.not_in(filtered_types))
                    .where(PassagesView.end_type.not_in(filtered_types))):
        graph.add_edge((passage.start_x, passage.start_y), (passage.end_x, passage.end_y))
    database.close()


def generate_dst():
    global dst_room

    logger.debug("Generating new dst point!")
    if not cur_room:
        logger.warning("Can't generate path from None room")
        return False

    while True:
        # Генерируем произвольные координаты
        dst_room = random.choice(list(nx_map.nodes))
        try:
            # Проверяем построение маршрута
            nx.shortest_path(nx_map, cur_room, dst_room)
            break
        except nx.NetworkXNoPath:
            # Маршрут не найден, пробуем еще
            continue

    return True


@events.register(events.MessageEdited(chats=(944268265,), pattern=r"(?s)^Ты находишься на 🏡(.+?) (\d+)\s+(.+)"))
@events.register(events.NewMessage(chats=(944268265,), pattern=r"(?s)^Ты находишься на 🏡(.+?) (\d+)\s+(.+)"))
async def town_handler(event):
    global cur_room
    global dst_room

    # Загружаем кнопки в список
    btn_data = list()
    for row in event.message.buttons:
        for btn in row:
            btn_data.append(btn.data.decode('utf-8'))

    # Если нарвались на торговца, телепорт и т.п. жмем "Уйти"
    if 'cwa_training' in btn_data and DO_TRAINING:
        # Если включена тренировка, и мы у тренера - жмём её
        time.sleep(random.uniform(1.1, 2.5))
        await event.client(functions.messages.GetBotCallbackAnswerRequest(event.from_id, event.id,
                                                                          data='cwa_training'.encode("utf-8")))
    elif 'cwa_nothing' in btn_data:
        time.sleep(random.uniform(1.1, 2.5))
        await event.client(functions.messages.GetBotCallbackAnswerRequest(event.from_id, event.id,
                                                                          data='cwa_nothing'.encode("utf-8")))
        return

    # Координаты текущей комнаты
    x = Streets.get_or_none(Streets.name == event.pattern_match.group(1)).x
    database.close()
    y = int(event.pattern_match.group(2))
    cur_room = (x, y)

    # Если включено авто-гуляние
    if AUTO_WALK:
        # Если конечная точка не определена или мы уже в конечной точке
        if (dst_room is None) or (cur_room == dst_room):
            # Генерируем новую конечную точку
            if generate_dst():
                logger.info(f"New dst point generated!")

    # Если не достигли цели или у нас новая цель
    if dst_room and (cur_room != dst_room):
        try:
            # Строим маршрут до цели и берем следующую точку в маршруте
            next_room = nx.shortest_path(nx_map, cur_room, dst_room)[1]
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
            await event.client(functions.messages.GetBotCallbackAnswerRequest(event.from_id, event.id,
                                                                              data=next_btn_data.encode('utf-8')))


def activate(client):
    load_graph(nx_map)
    client.add_event_handler(town_handler)
