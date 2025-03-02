import math

from microbit import display


class Loc:
    __x = 0.0
    __y = 2.0
    __angle = 0

    @staticmethod
    def add(x, angle):
        Loc.__draw(5)
        Loc.__x += math.cos(math.radians(Loc.__angle)) * x
        Loc.__y += math.sin(math.radians(Loc.__angle)) * x
        Loc.__angle += angle
        Loc.__draw(9)

    @staticmethod
    def __draw(value):
        x = round(Loc.__y)
        y = round(Loc.__x)
        if 0 <= x <= 4 and 0 <= y <= 4:
            display.set_pixel(x, y, value)
