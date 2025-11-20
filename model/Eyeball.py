from actor import Actor, Arena, Point
from math import sin, cos, dist
from random import randrange


BULLET = [
    ((116, 427), (149, 459))
]

class Eyeball(Actor):
    def __init__(self, pos, dx, dy):
        self._orig_x, self.orig_y = pos
        self._x, self._y = pos
        self._dx, self._dy = dx, dy 
        self._sprite_start, self._sprite_end = BULLET[0]

    def move(self, arena: Arena):
        from model.Arthur import Arthur
        aw, ah = arena.size()
        self._x += self._dx
        self._y += self._dy
        for other in arena.collisions():
            if isinstance(other, Arthur):
                x, y = other.pos()
                w, h = other.size()
                
                #________________       Collision Detection     ________________
                if (self._x >= x and self._x <= x+h) or  (x <= self._x + self.size()[0] <= x+h) :
                    if  ((y <= self._y <= y+h) or (y <= self._y + self.size()[1] <= y+h)) and other.check_grace():
                        self.hit(arena)
                        # other.reset_grace()
                        other.hit(arena)

        # remove Eyeball when out of the borders
        if (self._y + self.size()[1]  < 0) or (self._y > ah) or (self._x + self.size()[0] < 0) or (abs(self._orig_x - self._x) >= 500):
            self.hit(arena)


    def hit(self, arena: Arena):
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y
    
    def end(self) -> Point:
        x, y = self.pos()
        w, h = self.size()
        return x+w, y+h

    def size(self) -> Point:
        iw, ih = self._sprite_start
        ew, eh = self._sprite_end
        dw = ew-iw
        dh = eh-ih
        return dw, dh

    def sprite(self) -> Point:
        return self._sprite_start