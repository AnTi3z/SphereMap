from PIL import Image, ImageColor, ImageDraw, ImageFont
from db_models import *

room_coords = tuple([] for _ in range(len(Streets)))


class MapDrawer:

    def __init__(self, w=38, h=34):
        self.node_width = 124
        self.node_height = 86
        self.x_span = int(self.node_width * 0.75)
        self.y_span = int(self.node_height * 0.75)
        width = w * (self.node_width + self.x_span) + self.x_span
        height = h * (self.node_height + self.y_span) + self.y_span
        self.image = Image.new("RGBA", (width, height), color=ImageColor.getrgb("black"))
        self.draw = ImageDraw.Draw(self.image)
        ico_size = self.node_height // 2
        self.trap_ico = Image.open("icons//trap3.png").resize((ico_size, ico_size))
        self.bandit_ico = Image.open("icons//bandit.png").resize((ico_size, ico_size))
        self.trainer_ico = Image.open("icons//trainer2.png").resize((ico_size, ico_size))
        self.trader_ico = Image.open("icons//trader.png").resize((ico_size, ico_size))
        self.citizen_ico = Image.open("icons//citizen2.png").resize((ico_size, ico_size))
        self.teleport_ico = Image.open("icons//teleport5.png").resize((ico_size, ico_size))
        self.potion_ico = Image.open("icons//potion.png").resize((ico_size, ico_size))
        self.present_ico = Image.open("icons//present.png").resize((ico_size, ico_size))

    def _draw_entry(self, x, y):
        span = 40
        width = self.node_width + self.x_span - span
        height = self.node_height + self.y_span - span
        left = (y-1) * (width+40) + self.x_span // 2 + span/2 + 3
        up = (x-1) * (height+40) + self.y_span // 2 + span/2 + 3
        self.draw.rectangle((left, up, left + width, up + height), fill=ImageColor.getrgb("LightBlue"))

    def draw_node(self, x, y, name, num, poi, visits, entry=False):
        if entry:
            self._draw_entry(x, y)
        width = self.node_width
        height = self.node_height
        x_span = self.x_span
        y_span = self.y_span
        left = y * (width + x_span) - width
        up = x * (height + y_span) - height
        fill = None
        outline = None
        ico = None
        if poi == 1 and visits >= 5:
            fill = ImageColor.getrgb("DimGray")
        elif poi == 2:
            fill = ImageColor.getrgb("DimGray")
            outline = ImageColor.getrgb("blue")
            ico = self.trainer_ico
        elif poi == 3:
            fill = ImageColor.getrgb("green")
            ico = self.present_ico
        elif poi == 4:
            fill = ImageColor.getrgb("DarkRed")
            ico = self.trap_ico
        elif poi == 5:
            fill = ImageColor.getrgb("DimGray")
            outline = ImageColor.getrgb("blue")
            ico = self.teleport_ico
        elif poi == 6:
            fill = ImageColor.getrgb("DimGray")
            outline = ImageColor.getrgb("blue")
            ico = self.trader_ico
        elif poi == 7:
            fill = ImageColor.getrgb("DarkRed")
            ico = self.bandit_ico
        elif poi == 8:
            fill = ImageColor.getrgb("DimGray")
            outline = ImageColor.getrgb("blue")
            ico = self.citizen_ico
        elif poi == 9:
            fill = ImageColor.getrgb("DimGray")
            outline = ImageColor.getrgb("blue")
            ico = self.potion_ico

        # if poi > 1 or visits >= 10:
        #     self.draw.rectangle((left + 5, up + 5, left + width + 5, up + height + 5), fill=(48, 48, 48))
        self.draw.rectangle((left, up, left + width, up + height), fill=fill, outline=outline, width=2)
        self.draw_text(left, up, name, num)
        if ico:
            self.image.alpha_composite(ico, (left + width // 2 + 10, up + height // 2 - 10))

    def draw_text(self, left, up, name, num):
        x_span = 4
        y_span = 3
        fnt1 = ImageFont.truetype('Roboto-Medium.ttf', size=16)
        fnt2 = ImageFont.truetype('Roboto-Regular.ttf', size=21)
        name_width = self.draw.textsize(name, font=fnt2)[0]
        if name_width > self.node_width - x_span * 2:
            name = name.replace(" ", "\n")
        self.draw.multiline_text((left + x_span, up + y_span), name, font=fnt1, spacing=y_span)
        self.draw.text((left + x_span, up + self.node_height // 2 - y_span), str(num), font=fnt2)

    def draw_edge(self, x1, y1, x2, y2):
        width = self.node_width
        height = self.node_height
        x_span = self.x_span
        y_span = self.y_span
        left = y1 * (width + x_span) - width // 2
        up = x1 * (height + y_span) - height // 2
        right = y2 * (width + x_span) - width // 2
        down = x2 * (height + y_span) - height // 2
        if left < right:
            left += width // 2
            right -= width // 2
        elif right < left:
            right += width // 2
            left -= width // 2
        if up < down:
            up += height // 2
            down -= height // 2
        elif down < up:
            down += height // 2
            up -= height // 2
        self.draw.line((left, up, right, down), fill=ImageColor.getrgb("red"), width=2)

    def render_png(self, name='map.png'):
        self.image.save(name, "PNG")


def draw_nodes(drawer):
    for room in RoomsInfoView.select():
        drawer.draw_node(room.x, room.seq_y, room.name, room.y, room.type, room.visits, room.entry_flag)


def draw_edges(drawer):
    for passage in PassagesView.select():
        drawer.draw_edge(passage.start_x, passage.start_seq_y, passage.end_x, passage.end_seq_y)


if __name__ == "__main__":
    draw = MapDrawer()
    print("Generating nodes...")
    draw_nodes(draw)
    print("Generating edges...")
    draw_edges(draw)
    print("Generating png...")
    draw.render_png()
    print("Image map ready")
