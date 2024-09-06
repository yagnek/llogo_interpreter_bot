import math
from PIL import Image, ImageDraw


class Field():

    def __init__(self, size=(450, 400), color=(180, 142, 173)):
        self.size = size
        self.color = color  
        self.picture = Image.new("RGB", self.size, self.color)

    def clean(self):
        self.picture = Image.new("RGB", self.size, self.color)


class Turtle():

    def __init__(self, pos=[225, 200], angle=0, field=Field(), color=(236, 239, 244)):
        self.pos = pos
        self.angle = abs(angle)%360
        self.pen = True
        self.visible = True
        self.field = field
        self.color = color


    def forward(self, delta):
        old_pos = tuple(self.pos)
        angle_rads = math.radians(self.angle)
        sinus = round(math.sin(angle_rads), 2)
        delta_x = sinus * delta
        delta_y = math.sqrt(delta**2 - delta_x**2)
        if delta >= 0:
            if abs(self.angle) % 360 <= 90:
                self.pos[0] += delta_x
                self.pos[1] -= delta_y
            elif abs(self.angle) % 360 <= 270:
                self.pos[0] += delta_x
                self.pos[1] += delta_y
            elif abs(self.angle) % 360 < 360:
                self.pos[0] += delta_x
                self.pos[1] -= delta_y
        else:
            if abs(self.angle) % 360 < 90:
                self.pos[0] -= delta_x
                self.pos[1] += delta_y
            elif abs(self.angle) % 360 < 180:
                self.pos[0] += delta_x
                self.pos[1] += delta_y
            elif abs(self.angle) % 360 < 270:
                self.pos[0] -= delta_x
                self.pos[1] -= delta_y
            elif abs(self.angle) % 360 < 360:
                self.pos[0] += delta_x
                self.pos[1] -= delta_y

        if self.pen == True:
            self.draw_line(old_pos, self.pos)

    def draw_line(self, old_pos, new_pos):
        ImageDraw.Draw(self.field.picture).line(tuple(old_pos)+tuple(new_pos), fill=self.color, width=5)

    def setheading(self, angle):
        angle %= 360
        setattr(self, "angle", angle)

    def setpos(self, pos):
        old_pos = tuple(self.pos)
        self.pos = pos
        if self.pen == True:
            self.draw_line(old_pos, self.pos)

    def home(self):
        setattr(self, "pos", [225, 200])

    def backward(self, delta):
        delta *= -1
        self.forward(delta)


    def left(self, l):
        self.angle -= l
        self.angle %= 360


    def right(self, l):
        self.angle += l
        self.angle %= 360


    def penup(self):
        setattr(self, "pen", False)


    def pendown(self):
        setattr(self, "pen", True)


    def hideturtle(self):
        setattr(self, "visible", False)


    def showturtle(self):
        setattr(self, "visible", False)

    def clearscreen(self):
        self.home()
        self.setheading(0)
        self.field.clean()
