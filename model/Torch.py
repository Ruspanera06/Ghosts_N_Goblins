from actor import Actor, Arena, Point
from random import choice, randint
from model.Flame import Flame
from model.Zombie import Zombie
from model.Plant import Plant

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
        self._speed = 3
        self._dx = dx*self._speed
        self._dy = 0
        self._direction = dx
        #animation stats
        self._sprite_start, self._sprite_end = THROW_LEFT[0] if self._direction == 1 else THROW_RIGHT[0]
        self._frame = 0
        self._duration_frame = 4

    def move(self, arena:Arena):
        G = 0.3
        #G = 5 
        aw, ah = arena.size()
        ah -= 30
        if self._y == ah - self._h:
            self._dx = 0
            self.hit(arena)
            arena.spawn(Flame(self.pos()))
        self._dx
        self._x += self._dx
        self._y += G
        self._x = min(max(self._x, 5), aw - self._w)  # clamp
        self._y = min(max(self._y, 5), ah - self._h)  # clamp

        #________________       Collision Detection     ________________
        for other in arena.collisions():
                if isinstance(other, (Zombie, Plant)):
                    x, y = other.pos()
                    w, h = other.size()
                    
                    #checking if the point if the left-side or right-side is contained into the zombies x
                    if (self._x >= x and self._x <= x+h) or  (x <= self._x + self._w <= x+h) :
                        #same check but with the y
                        if  (y <= self._y <= y+h) or (y <= self._y + self._h <= y+h):
                            other.hit(arena)
                            self.hit(arena)


        #________________       Animation Zone     ________________

        if self._direction == 1:
            animation = THROW_RIGHT
        else:
            animation = THROW_LEFT
        index = (self._frame//self._duration_frame)%(len(animation))
        self._sprite_start, self._sprite_end = animation[index]

        if self._frame >= 120:
            self._frame = 0
        else:
            self._frame += 1


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