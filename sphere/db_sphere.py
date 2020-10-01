import logging
import re

from .db_models import *

logger = logging.getLogger('SphereMap')


def check_description(desc):
    with database.connection_context():
        query = LocDescription.select()
        for row in query:
            if re.search(row.txt_regexp, desc):
                return row

        return LocDescription.create(txt_regexp=desc, type=1)


def erase_bandits(room_id):
    # TODO: удалить бандитов
    return 0  # число удаленных строк


def get_last_room_stat(user_id):
    with database.connection_context():
        event = Events.select().join(Users).order_by(Events.timestamp.desc()).where(Users.tg_id == user_id).get()
        return get_room_stat(event)


def get_room_stat(event_id):
    with database.connection_context():
        event = Events.get(Events.id == event_id)
        room = event.location
        query = (Events
                 .select(Events, fn.COUNT(EventTypes.id).alias('cnt'))
                 .join(LocDescription)
                 .join(EventTypes)
                 .where(Events.location == room)
                 .group_by(EventTypes.id)
                 .order_by(EventTypes.id))
        stats = {
            "event_id": event.id,
            "name": room.street.name,
            "num": room.y,
            "last_type": event.loc_desc.type.name,
            "entry": EntryPoints.select().join(Events).where(Events.location == room).count(),
            "portal_exit": PortalExits.select().join(Events).where(Events.location == room).count(),
            "events": [(ev.loc_desc.type.name, ev.cnt) for ev in query]
        }
        return stats
