from PIL import Image, ImageColor, ImageDraw, ImageFont
from db_models import *

room_coords = tuple([] for _ in range(len(Streets)))


class MapDrawer:

    def __init__(self, width=9600, height=6000):
        self.image = Image.new("RGB", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.node_width = width/39 / 2
        self.node_height = height/35 / 2

    def draw_node(self, x, y, name, num, poi):
        width = self.node_width
        height = self.node_height
        x_span = width
        y_span = height
        left = y * (width+x_span)
        up = x * (height+y_span)
        fnt = ImageFont.truetype('arial.ttf', size=14)
        fill = None
        if poi in (1, 2, 5, 6, 8, 9):
            fill = ImageColor.getrgb("grey")
        elif poi in (4, 7):
            fill = ImageColor.getrgb("red")
        elif poi in (3, 10, 11):
            fill = ImageColor.getrgb("green")
        self.draw.rectangle((left, up, left+width, up+height), fill=fill)
        self.draw.multiline_text((left+2, up+2), name.replace(" ", "\n"), font=fnt, fill=ImageColor.getrgb("blue"))
        num_width = self.draw.textsize(str(num), font=fnt)[0]
        self.draw.text((left + width - num_width-2, up + 2), str(num), font=fnt, fill=ImageColor.getrgb("blue"))

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
    query = (Rooms
             .select(Rooms, fn.MAX(LocDescription.type).alias('type'), Streets.name)
             .join(Events, JOIN.LEFT_OUTER)
             .join(LocDescription, JOIN.LEFT_OUTER)
             .join(Streets, on=(Rooms.x == Streets.x))
             .group_by(Rooms.id)
             .order_by(+Rooms.x, +Rooms.y))
    for (_, room_x, room_y, room_type, street_name) in database.execute(query):
        y = append_y(room_x, room_y)
        drawer.draw_node(room_x, y, street_name, room_y, room_type)


def draw_edges(drawer):
    Start = Rooms.alias()
    End = Rooms.alias()
    cte = (Passages.select(Passages.start, Passages.end).where(Passages.start > Passages.end)
           |
           Passages.select(Passages.end, Passages.start).where(Passages.end > Passages.start))

    query = (cte.select(Start.x, Start.y, End.x, End.y)
             .join(Start, on=(Start.id == cte.c.start))
             .join(End, on=(End.id == cte.c.end)))
    for (start_x, start_y, end_x, end_y) in database.execute(query):
        drawer.draw_edge(start_x, get_y(start_x, start_y),
                         end_x, get_y(end_x, end_y))


def append_y(x, num):
    global room_coords
    room_coords[x-1].append(num)
    return len(room_coords[x-1])


def get_y(x, num):
    global room_coords
    return room_coords[x-1].index(num)+1


if __name__ == "__main__":
    draw = MapDrawer()
    print("Generating nodes...")
    draw_nodes(draw)
    print("Generating edges...")
    draw_edges(draw)
    print("Generating png...")
    draw.render_png()
    print("Image map ready")
