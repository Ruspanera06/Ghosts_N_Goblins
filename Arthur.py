from actor import Actor, Arena, Point
class Arthur(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 20, 20
        self._dx, self._dy = 0, 0
        self._jump = False
        self.max_jump = 40
        self._djump = 4
        self._speed = 2
        self._health = 3

    def move(self, arena: Arena):
        G = 5
        # for other in arena.collisions():
        #     if isinstance(other, Arthur):
        #         self.hit(arena)

        keys = arena.current_keys()
        if ("Spacebar" in keys or "w" in keys) and self._y + self._h == arena.size()[1] :
            self._jump = True
            self._dy -= self._djump
        elif self._y + self._h == arena.size()[1]:
            self._dy = 0
            self._jump = False
        if "a" in keys:
            self._x -= self._speed
        elif "d" in keys:
            self._x += self._speed
        
        #self._x += self._dx
        aw, ah = arena.size()
        self._x = min(max(self._x, 5), aw - self._w)  # clamp
        self._y = min(max(self._y, 5), ah - self._h)  # clamp

        if self._y > arena.size()[1]-self.max_jump and self._jump == True:
            self._y += self._dy
        else:
            self._jump = False
        if self._y + self._h < arena.size()[1] and self._jump == False:
            self._y += G
        

    def hit(self, arena: Arena):
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 0, 20