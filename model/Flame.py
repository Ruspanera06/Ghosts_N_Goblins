from actor import Actor, Arena, Point
from model.Zombie import Zombie
from model.Plant import Plant

#___________        ANIMATIONS          ____________

DAMAGING_FLAME = [
    ((116, 427), (149, 459)),
    ((152, 427), (177, 459))
]
EXTINGUISH_FLAME = [
    ((209, 442), (226, 459)),
    ((228, 442), (239, 459))
]

class Flame(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._y -= 20
        x1, y1 = DAMAGING_FLAME[0][0]
        x2, y2 = DAMAGING_FLAME[0][1]
        self._w, self.h = abs(x1 - x2), abs(y1 - y2)

        #animation stats
        self._frame = 0
        self._duration_frame = 5
        self._life = 60
        self._change_y = True
        self._sprite_start, self._sprite_end = DAMAGING_FLAME[0]

    
    def move(self, arena: Arena):
        ###########          ANIMATION ZONE      ################

        for other in arena.collisions():
            if isinstance(other, Zombie) or isinstance(other, Plant):
                other.hit(arena)

        if self._frame <= 40:
            animation = DAMAGING_FLAME
        else:
            if self._change_y:
                self._y += 15
                self._change_y = not self._change_y
                x1, y1 = EXTINGUISH_FLAME[0][0]
                x2, y2 = EXTINGUISH_FLAME[0][1]
                self._w, self._h = abs(x1 - x2), abs(y1 - y2)
                self._x += self._w//2
            animation = EXTINGUISH_FLAME
        index = (self._frame//self._duration_frame)%(len(animation))
        self._sprite_start, self._sprite_end = animation[index]

        if self._frame >= self._life:
            self.extinguish(arena)
        else:
            self._frame += 1
        
    
    def extinguish(self, arena: Arena):
        arena.kill(self)
    
    def size(self) -> Point:
        iw, ih = self._sprite_start
        ew, eh = self._sprite_end
        dw = ew-iw
        dh = eh-ih
        return dw, dh

    def pos(self) -> Point:
        return self._x, self._y
    
    def sprite(self) -> Point:
        return self._sprite_start
        