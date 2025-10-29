from actor import Actor, Arena, Point
class Zombie(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 20, 20
        self._dx = 0
        self._spawn = False 
        self._djump = 4
        self._speed = 2

    def move(self, arena: Arena):
        aw, ah = arena.size()
        self._x += self._dx 
        
        if self._x <=0 or self.x+self._w >= aw:
            self._dx = -self._dx
            
        self._x = min(max(self._x, 0), aw - self._w)  # clamp
        self._y = min(max(self._y, 0), ah - self._h)  # clamp

    def hit(self, arena: Arena):
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 0, 20