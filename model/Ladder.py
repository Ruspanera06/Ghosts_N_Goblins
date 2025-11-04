from actor import Actor, Arena, Point

LADDERS = [
    ((722, 121), (740, 202)),
    ((912, 121), (932, 202)),
    ((1072, 121), (1092, 202))
]

class Ladder(Actor):
    def __init__(self, pos, end):
        self._x, self._y = pos
        self._x_end, self._y_end = end

    def move(self, arena: Arena):
        pass

    def hit(self, arena: Arena):
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y
    
    def end(self) -> Point:
        return self._x_end, self._y_end

    def size(self) -> Point:
        iw, ih = self.pos()
        ew, eh = self.end()
        dw = abs(ew-iw)
        dh = abs(eh-ih)
        return dw, dh
    
    def sprite(self) -> Point:
        return None