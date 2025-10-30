from actor import Actor, Arena, Point

class Gravestone(Actor):
    def __init__(self, pos, pos_end):
        self._x, self._y = pos
        self._end_x, self._end_y = pos_end
    
    def pos(self) -> Point:
        return self._x, self._y
    
    def pos_end(self) -> Point:
        return self._end_x, self._end_y

    def size(self) -> Point:
        x, y = self.pos()
        end_x, end_y = self.pos_end()
        dx = abs(x, end_x)
        dy = abs(y, end_y)
        return dx, dy

    def sprite(self) -> Point:
        return None