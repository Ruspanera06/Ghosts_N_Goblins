from actor import Actor, Arena, Point
from random import choice, randint

#___________        ANIMATIONS          ____________
THROW_RIGHT = [
    ((18, 398), (33, 414)),
    ((38, 398), (52, 414)),
    ((57, 398), (71, 414)),
    ((77, 398), (92, 412))
]

THROW_LEFT = [
    ((478, 398), (493, 414)),
    ((459, 398), (473, 414)),
    ((440, 398), (454, 414)),
    ((419, 398), (434, 414))
]

class Torch(Actor):
    def __init__(self, pos, dx):
        self._x, self._y = pos
        self._w, self._h = 15, 14
        self._spawn = True 
        self._speed = 4
        self._dx = dx*self._speed
        self._dy = 0
        self._direction = dx
        self._sprite_start, self._sprite_end = THROW_LEFT[0] if self._direction == 1 else THROW_RIGHT[0]

    def move(self, arena:Arena):
        G = 0.2
        aw, ah = arena.size()
        ah -= 45
        if self._y == ah - self._h:
            self._dx = 0
            # self.hit(self, arena)
        self._dx
        self._x += self._dx
        self._y += G
        self._x = min(max(self._x, 5), aw - self._w)  # clamp
        self._y = min(max(self._y, 5), ah - self._h)  # clamp

    def hit(self, arena: Arena):
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        iw, ih = self._sprite_start
        ew, eh = self._sprite_end
        dw = ew-iw
        dh = eh-ih
        return dw, dh

    def sprite(self) -> Point:
        return self._sprite_start