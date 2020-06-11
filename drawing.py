from PIL import Image, ImageColor, ImageDraw, ImageFont
from db_models import *

room_coords = tuple([] for _ in range(len(Streets)))


class MapDrawer:

    def __init__(self, width=7800, height=4400):
        self.image = Image.new("RGB", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.node_width = 100
        self.node_height = 60

    def draw_node(self, x, y, name, poi):
        width = self.node_width
        height = self.node_height
        x_span = width
        y_span = height
        left = y * (width+x_span)
        up = x * (height+y_span)
        fnt = ImageFont.truetype('arial.ttf', size=15)
        fill = None
        if poi in (1, 2, 5, 6, 8, 9):
            fill = ImageColor.getrgb("grey")
        elif poi in (4, 7):
            fill = ImageColor.getrgb("red")
        elif poi in (3, 10, 11):
            fill = ImageColor.getrgb("green")
        self.draw.rectangle((left, up, left+width, up+height), fill=fill)
        self.draw.text((left+2, up+2), name, font=fnt, fill=ImageColor.getrgb("blue"))

    def draw_edge(self, x1, y1, x2, y2):
        width = self.node_width
        height = self.node_height
        x_span = width
        y_span = height
        left = y1 * (width + x_span) + width / 2
        up = x1 * (height + y_span) + height / 2
        right = y2 * (width + x_span) + width / 2
        down = x2 * (height + y_span) + height / 2
        if left < right:
            left += width/2
            right -= width / 2
        elif right < left:
            right += width / 2
            left -= width/2
        if up < down:
            up += height/2
            down -= height / 2
        elif down < up:
            down += height / 2
            up -= height/2
        self.draw.line((left, up, right, down), fill=ImageColor.getrgb("red"), width=2)

    def render_png(self, name='test.png'):
        self.image.save(name, "PNG")


def draw_nodes(drawer):
    for room in Rooms.select().order_by(+Rooms.x, +Rooms.y):
        y = append_y(room.x, room.y)
        event_history = (Events.select().where(Events.location == room))
        poi = None
        if event_history:
            poi = 1
            for event in event_history:
                if event.loc_desc.type.id != 1:
                    poi = event.loc_desc.type.id
                    break
        name = f"{room.street.name} {room.y}"
        drawer.draw_node(room.x, y, name, poi)


def draw_edges(drawer):
    query = (Passages.select(Passages.start, Passages.end).where(Passages.start > Passages.end)
             |
             Passages.select(Passages.end, Passages.start).where(Passages.end > Passages.start))
    for link in query:
        drawer.draw_edge(link.start.x, get_y(link.start.x, link.start.y),
                         link.end.x, get_y(link.end.x, link.end.y))


def append_y(x, num):
    global room_coords
    room_coords[x-1].append(num)
    return len(room_coords[x-1])


def get_y(x, num):
    global room_coords
    return room_coords[x-1].index(num)+1


if __name__ == "__main__":
    draw = MapDrawer()
    draw_nodes(draw)
    draw_edges(draw)
    draw.render_png()
