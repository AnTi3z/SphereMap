import warnings

import pymysql
from peewee import *

import config

warnings.filterwarnings(
    action="ignore",
    message=".*Duplicate entry.*",
    category=pymysql.Warning
)

warnings.filterwarnings(
    action="ignore",
    message=".*NO_AUTO_CREATE_USER.*",
    category=pymysql.Warning
)

database = MySQLDatabase('sphere_map',
                         user=config.configs['sphere']['mysql']['user'], password=config.configs['sphere']['mysql']['pass'],
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
        table_name = 'events'


class EntryPoints(BaseModel):
    event = ForeignKeyField(column_name='event_id', field='id', model=Events, unique=True)

    class Meta:
        table_name = 'entry_points'
        primary_key = False


class PortalExits(BaseModel):
    event = ForeignKeyField(column_name='event_id', field='id', model=Events, unique=True)

    class Meta:
        table_name = 'portal_exits'
        primary_key = False


class EntryRooms(BaseModel):
    entry = ForeignKeyField(column_name='entry', field='id', model=Rooms, unique=True)

    class Meta:
        table_name = 'entry_rooms'
        primary_key = False


class Passages(BaseModel):
    end = ForeignKeyField(backref='end_room', column_name='end', field='id', model=Rooms)
    start = ForeignKeyField(backref='start_room', column_name='start', field='id', model=Rooms)

    class Meta:
        table_name = 'passages'
        indexes = (
            (('start', 'end'), True),
        )
        primary_key = False


class RoomsView(BaseModel):
    id = IntegerField()
    x = IntegerField()
    y = IntegerField()
    seq_y = IntegerField()

    class Meta:
        table_name = 'rooms_view'
        primary_key = False


class RoomsInfoView(BaseModel):
    id = IntegerField()
    x = IntegerField()
    y = IntegerField()
    seq_y = IntegerField()
    type = IntegerField()
    name = CharField()
    visits = IntegerField()
    entry_flag = BooleanField()

    class Meta:
        table_name = 'rooms_info_view'
        primary_key = False


class PassagesView(BaseModel):
    start_id = IntegerField()
    start_x = IntegerField()
    start_y = IntegerField()
    start_seq_y = IntegerField()
    start_type = IntegerField()
    end_id = IntegerField()
    end_x = IntegerField()
    end_y = IntegerField()
    end_seq_y = IntegerField()
    end_type = IntegerField()

    class Meta:
        table_name = 'passages_view'
        primary_key = False
