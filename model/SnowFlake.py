from actor import Actor, Arena, Point
from random import randint, choice


# ((pos), (size))
204, 85
305, 90
SNOWFLAKES_SPRITES = [
    ((26, 16), (76, 75)),
    ((140, 22), (64, 63)),
    ((231, 16), (74, 74)),
    ((332, 16), (74, 74)),
    ((439, 16), (74, 74)),
    ((27, 123), (74, 74)),
    ((146, 136), (76, 75)),
    ((332, 123), (76, 75)),
    ((27, 230), (76, 75)),
    ((129, 225), (76, 75)),
    ((236, 236), (76, 75)),
    ((331, 230), (76, 75)),
    ((432, 224), (76, 75)),
]

class SnowFlake(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._speed = randint(5, 10)
        self._dy = randint(1,3) * self._speed
        self._dx = randint(-1,1)
        self._angle = 0
        tmp = choice(SNOWFLAKES_SPRITES)
        self._sprite = tmp[0]
        self._w, self._h = tmp[1]
        self._d_angle = 30

    def move(self, arena: Arena):
        self._x += self._dx
        self._y += self._dy
        self._angle += self._d_angle
        if self._y > arena.size()[1]+20:
            self.hit(arena)

    def hit(self, arena: Arena):
        arena.kill(self)
    
    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._sprite


