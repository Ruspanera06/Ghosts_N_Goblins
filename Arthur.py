from actor import Actor, Arena, Point
#animations sprites
#the tuple will contain ((start_x, start_y), (end_x, end_y)) of the png
IDLE_RIGHT = ((5, 42), (26, 73))
IDLE_LEFT = ((485, 42), (506, 74))
RUNNING = ((39, 41), (65, 41), (88, 41), (108, 41))

class Arthur(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx, self._ = 0, 0
        self._w, self._h = 20, 20
        self._dx, self._dy = 0, 0
        self._jump = False
        self.max_jump = 40
        self._djump = 4
        self._speed = 2
        self._health = 2
        self._frame = 0
        self._duration_frame = 10
        
        #animation stats
        self._sprite_start, self._sprite_end = IDLE_RIGHT
        

    def move(self, arena: Arena):
        G = 5
        aw, ah = arena.size()
        #-45 perchè così tiooca il suolo
        ah -=45
        self._dx = 0
        # for other in arena.collisions():
        #     if isinstance(other, Arthur):
        #         self.hit(arena)

        keys = arena.current_keys()
        if ("Spacebar" in keys or "w" in keys) and self._y + self._h == ah :
            self._jump = True
            self._dy -= self._djump
        elif self._y + self._h == ah:
            self._dy = 0
            self._jump = False
        if "a" in keys:
            self._dx -= self._speed
        elif "d" in keys:
            self._dx += self._speed
        
        self._x += self._dx
        self._x = min(max(self._x, 5), aw - self._w)  # clamp
        self._y = min(max(self._y, 5), ah - self._h)  # clamp

        if self._y > ah-self.max_jump and self._jump == True:
            self._y += self._dy
        else:
            self._jump = False
        if self._y + self._h < ah and self._jump == False:
            self._y += G
        

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