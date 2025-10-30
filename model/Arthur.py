from actor import Actor, Arena, Point
#animations sprites
#the tuple will contain ((start_x, start_y), (end_x, end_y)) of the png
IDLE_RIGHT_ARMOR = ((5, 42), (26, 73))
IDLE_LEFT_ARMOR = ((485, 42), (506, 74))
IDLE_RIGHT_NAKED = ((6, 76), (25, 106))
IDLE_LEFT_NAKED = ((486, 76), (505, 106))

RUNNING_RIGHT_ARMOR = [
    ((39, 41),(63, 72)), 
    ((65, 41), (85, 74)), 
    ((88, 41), (107, 74)), 
    ((108, 41), (133, 72))
]
sprite_x = 511
RUNNING_LEFT_ARMOR = []
#mirroring RUNNING_RIGHT_ARMOR so it become RUNNING_LEF_ARMOR
for s in RUNNING_RIGHT_ARMOR:
    s_x = (s[1][0]-s[0][0])
    x = sprite_x - s[0][0] - s_x
    y = s[0][1]
    size_x = x + s_x
    size_y = s[1][1]
    RUNNING_LEFT_ARMOR.append(
        ((x, y), (size_x, size_y))
    )

RUNNING_RIGHT_NAKED = [
    ((36, 76), (62, 101)),
    ((66, 76),(84, 106)),
    ((90, 76),(106, 106)),
    ((109, 76), (134, 102))
]

RUNNING_LEFT_NAKED = []
#mirroring RUNNING_RIGHT_ARMOR so it become RUNNING_LEF_ARMOR
for s in RUNNING_RIGHT_NAKED:
    s_x = (s[1][0]-s[0][0])
    x = sprite_x - s[0][0] - s_x
    y = s[0][1]
    size_x = x + s_x
    size_y = s[1][1]
    RUNNING_LEFT_NAKED.append(
        ((x, y), (size_x, size_y))
    )



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
        self._health = 1
        
        #animation stats
        self._sprite_start, self._sprite_end = IDLE_RIGHT_ARMOR
        self._frame = 0
        self._duration_frame = 3
        self._direction = 0 #0 = destra, 1 = sinistra
        

    def move(self, arena: Arena):
        G = 5
        aw, ah = arena.size()
        #-45 perchè così tocca il suolo
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
            self._direction = 1
        elif "d" in keys:
            self._direction = 0
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

        ###########          ANIMATION ZONE      ################
        if self._frame >= 120:
            self._frame = 0
        else:
            self._frame += 1



        if self._dx == 0:
            self._frame = 0
            if self._direction == 1 and self._health == 2:
                self._sprite_start, self._sprite_end = IDLE_LEFT_ARMOR
            elif self._direction == 0 and self._health == 2:
                self._sprite_start, self._sprite_end = IDLE_RIGHT_ARMOR
            elif self._direction == 1 and self._health == 1:
                self._sprite_start, self._sprite_end = IDLE_LEFT_NAKED
            else:
                self._sprite_start, self._sprite_end = IDLE_RIGHT_NAKED
        else:
            if self._direction == 1 and self._health == 2:
                animation = RUNNING_LEFT_ARMOR.copy()
            elif self._direction == 1 and self._health == 1:   
                animation = RUNNING_LEFT_NAKED.copy()
            elif self._direction == 0 and self._health == 2:
                animation = RUNNING_RIGHT_ARMOR.copy()
            else:
                animation = RUNNING_RIGHT_NAKED.copy()

            index = (self._frame//self._duration_frame)%(len(animation))
            self._sprite_start, self._sprite_end = animation[index]




        

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