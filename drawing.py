from PIL import Image, ImageColor, ImageDraw, ImageFont
from db_models import *


class MapDrawer:

    def __init__(self, width=22800, height=3200):
        self.image = Image.new("RGB", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.node_width = 100
        self.node_height = 60

    def draw_node(self, x, y, name, poi):
        width = self.node_width
        height = self.node_height
        x_span = 50
        y_span = 30
        x0 = y * (width+x_span)
        y0 = x * (height+y_span)
        fnt = ImageFont.truetype('arial.ttf', size=15)
        fill = None
        if poi in (1, 2, 5, 6, 8, 9):
            fill = ImageColor.getrgb("grey")
        elif poi in (4, 7):
            fill = ImageColor.getrgb("red")
        elif poi in (3, 10, 11):
            fill = ImageColor.getrgb("green")
        self.draw.rectangle((x0, y0, x0+width, y0+height), fill=fill)
        self.draw.text((x0+2, y0+2), name, font=fnt, fill=ImageColor.getrgb("blue"))

    def draw_edge(self, x1, y1, x2, y2):
        width = self.node_width
        height = self.node_height
        x_span = 50
        y_span = 30
        x0 = y1 * (width+x_span) + width/2
        y0 = x1 * (height+y_span) + height/2
        x1 = y2 * (width+x_span) + width/2
        y1 = x2 * (height+y_span) + height/2
        self.draw.line((x0, y0, x1, y1), fill=ImageColor.getrgb("red"))

    def render_png(self, name='test.png'):
        self.image.save(name, "PNG")


def draw_nodes(drawer):
    for room in Rooms.select().order_by('x'):
        event_history = (Events.select().where(Events.location == room))
        poi = None
        if event_history:
            poi = 1
            for event in event_history:
                if event.loc_desc.type.id != 1:
                    poi = event.loc_desc.type.id
                    break
        name = f"{room.street.name} {room.y}"
        drawer.draw_node(room.x, room.y, name, poi)


def draw_edges(drawer):
    query = (Passages.select(Passages.start, Passages.end).where(Passages.start > Passages.end)
             |
             Passages.select(Passages.end, Passages.start).where(Passages.end > Passages.start))
    for link in query:
        drawer.draw_edge(link.start.x, link.start.y, link.end.x, link.end.y)


if __name__ == "__main__":
    draw = MapDrawer()
    draw_nodes(draw)
    draw_edges(draw)
    draw.render_png()