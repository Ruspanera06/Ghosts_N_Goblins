from actor import Actor, Arena, Point

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
        self._frame = 0
        self._life = 60
        self._sprite_start, self._sprite_end = DAMAGING_FLAME[0]

    
    def move(self, arena: Arena):

        ###########          ANIMATION ZONE      ################
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
        