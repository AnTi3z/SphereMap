from peewee import *
from config import MYSQL_USER, MYSQL_PASS

database = MySQLDatabase('sphere_map',
                         user=MYSQL_USER, password=MYSQL_PASS,
                         host='anti3z.ru', port=3306)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class EventTypes(BaseModel):
    name = CharField(max_length=32, unique=True)

    class Meta:
        table_name = 'event_types'


class LocDescription(BaseModel):
    txt_regexp = CharField(max_length=255, unique=True)
    type = ForeignKeyField(column_name='type', field='id', model=EventTypes)

    class Meta:
        table_name = 'loc_description'


class Streets(BaseModel):
    x = IntegerField(primary_key=True)
    name = CharField(max_length=32, unique=True)

    class Meta:
        table_name = 'streets'


class Rooms(BaseModel):
    street = ForeignKeyField(column_name='x', field='x', model=Streets)
    y = IntegerField()

    class Meta:
        table_name = 'rooms'
        indexes = (
            (('x', 'y'), True),
        )


class Users(BaseModel):
    tg_id = IntegerField(primary_key=True)
    name = CharField(max_length=16)

    class Meta:
        table_name = 'event_users'


class Events(BaseModel):
    loc_desc = ForeignKeyField(column_name='loc_desc', field='id', model=LocDescription)
    location = ForeignKeyField(column_name='location', field='id', model=Rooms)
    user = ForeignKeyField(column_name='user', field='tg_id', model=Users)
    timestamp = TimestampField(utc=True)

    class Meta:
        table_name = 'Events'


class Teleports(BaseModel):
    source = ForeignKeyField(column_name='event_id', field='id', model=Events)
    target = ForeignKeyField(column_name='to_location', field='id', model=Rooms)

    class Meta:
        table_name = 'teleports'


class EntryPoints(BaseModel):
    event = ForeignKeyField(column_name='event_id', field='id', model=Events)

    class Meta:
        table_name = 'entry_points'


class Passages(BaseModel):
    end = ForeignKeyField(backref='end_room', column_name='end', field='id', model=Rooms)
    start = ForeignKeyField(backref='start_room', column_name='start', field='id', model=Rooms)

    class Meta:
        table_name = 'Passages'
        indexes = (
            (('start', 'end'), True),
        )
        primary_key = False

