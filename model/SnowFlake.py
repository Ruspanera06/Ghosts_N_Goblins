from actor import Actor, Arena, Point
from random import randint, choice


# ((pos), (size))
# SNOWFLAKES_SPRITES = [
#     ((26, 16), (76, 75)),
#     ((140, 22), (64, 63)),
#     ((231, 16), (74, 74)),
#     ((332, 16), (74, 74)),
#     ((439, 16), (74, 74)),
#     ((27, 123), (74, 74)),
#     ((146, 136), (76, 75)),
#     ((332, 123), (76, 75)),
#     ((27, 230), (76, 75)),
#     ((129, 225), (76, 75)),
#     ((236, 236), (76, 75)),
#     ((331, 230), (76, 75)),
#     ((432, 224), (76, 75)),
# ]

SNOWFLAKES_SPRITES = [
    ((0, 0), (8, 8)),
    ((9, 0), (17, 8)),
    ((18, 0), (26, 8)),
    ((27, 0), (35, 8)),
    ((36, 0), (44, 8)),
    ((45, 0), (53, 8)),
    ((1, 10), (7, 16)),
    ((10, 10), (16, 16)),
    ((19, 10), (25, 16)),
    ((28, 10), (34, 16)),
    ((36, 9), (44, 17)),
    ((45, 9), (53, 17)),
    ((3, 21), (5, 23)),
    ((11, 20), (15, 24)),
    ((20, 20), (24, 24)),
    ((29, 20), (33, 24)),
    ((46, 19), (52, 25)),
]

class SnowFlake(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._speed_dy = randint(2, 8)
        self._speed_dx = randint(2, 4)
        self._dy = randint(1,3) * self._speed_dy
        self._dx = randint(-1,1)* self._speed_dx
        self._angle = 0
        tmp = choice(SNOWFLAKES_SPRITES)
        self._sprite = tmp[0]
        s_x, s_y = tmp[0]
        s_end_x, s_end_y = tmp[1]
        self._w, self._h = abs(s_end_x - s_x), abs(s_end_y - s_y)
        self._d_angle = 30
        self._change_dx = 30

    def move(self, arena: Arena):
        self._x += self._dx
        self._y += self._dy
        self._angle += self._d_angle
        self._change_dx = min(self._change_dx + 1,30)
        if self._change_dx == 30:
            self.change_direction()

        if self._y > arena.size()[1]+20:
            self.hit(arena)

    def change_direction(self):
        if self._change_dx == 30:
            n = randint(0, 20)
            if n == 0:
                self._change_dx = 0
                self._dx = -self._dx

    def hit(self, arena: Arena):
        arena.kill(self)
    
    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._sprite


