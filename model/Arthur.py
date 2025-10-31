from actor import Actor, Arena, Point
from random import choice, randint
from model.Torch import Torch
#animations sprites
#the tuple will contain ((start_x, start_y), (end_x, end_y)) of the png
IDLE_RIGHT_ARMOR = ((5, 42), (26, 73))
IDLE_LEFT_ARMOR = ((485, 42), (506, 74))
IDLE_RIGHT_NAKED = ((6, 76), (25, 106))
IDLE_LEFT_NAKED = ((486, 76), (505, 106))

JUMP_RIGHT_ARMOR = [
    ((143, 28), (176, 56)),
    ((179, 28), (207, 56))
]
JUMP_LEFT_ARMOR = [
    ((304, 28), (332, 56)),
    ((335, 28), (368, 56))
][::1]

JUMP_RIGHT_NAKED = [
    ((144, 61), (174, 88)),
    ((182, 61), (206, 88))
]
JUMP_LEFT_NAKED = [
    ((305, 61), (329, 88)),
    ((337, 61), (367, 88))
][::-1]


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
        self._w, self._h = 20, 20
        self._dx, self._dy = 0, 0
        self._jump = False
        self.max_jump = 40
        self._djump = 15
        self._speed = 3
        self._health = 1
        self._attack_speed = 10
        self._attack_frame = self._attack_speed
        
        #animation stats
        self._sprite_start, self._sprite_end = IDLE_RIGHT_ARMOR
        self._frame = 0
        self._duration_frame = 3
        self._direction = 0 
        self._jump_anim = False
        self._i_jump = None
        
        

    def move(self, arena: Arena):
        G = 2
        aw, ah = arena.size()
        #-45 in order to make arthur touch the ground
        ah -=45
        self._dx = 0

        keys = arena.current_keys()
        if ("Spacebar" in keys or "w" in keys) and self._y + self._h == ah:
            self._jump = True
            self._jump_anim = True
            self._dy = -self._djump
            self._i_jump = None
        elif self._y + self._h == ah:
            self._dy = 0
            self._jump = False
            self._jump_anim = False
            self._i_jump = None
        if "a" in keys:
            self._dx -= self._speed
            self._direction = 1
        elif "d" in keys:
            self._direction = 0
            self._dx += self._speed
        
        if "f" in keys:
            if self._attack_frame == self._attack_speed:
                self.throw_Torch(arena)
                self._attack_frame = 0
        
        self._attack_frame = min(self._attack_frame+1, self._attack_speed)        
        self._x += self._dx

        self._dy += G
        self._y += self._dy
        self._x = min(max(self._x, 5), aw - self._w)  # clamp
        self._y = min(max(self._y, 5), ah - self._h)  # clamp

        ###########          ANIMATION ZONE      ################
        if self._frame >= 120:
            self._frame = 0
        else:
            self._frame += 1

        #________________JUMP FRAME LOGIC________________
        if self._jump :
            if self._jump_anim:
                if self._i_jump == None:
                    self._i_jump = randint(0,1)
                if self._direction == 1 and self._health == 2:
                    self._sprite_start, self._sprite_end = JUMP_LEFT_ARMOR[self._i_jump]
                elif self._direction == 0 and self._health == 2:
                    self._sprite_start, self._sprite_end = JUMP_RIGHT_ARMOR[self._i_jump]
                elif self._direction == 1 and self._health == 1:
                    self._sprite_start, self._sprite_end = JUMP_LEFT_NAKED[self._i_jump]
                else:
                    self._sprite_start, self._sprite_end = JUMP_RIGHT_NAKED[self._i_jump]
        
        #________________IDLE FRAME LOGIC________________

        elif self._dx == 0:
            self._frame = 0
            if self._direction == 1 and self._health == 2:
                self._sprite_start, self._sprite_end = IDLE_LEFT_ARMOR
            elif self._direction == 0 and self._health == 2:
                self._sprite_start, self._sprite_end = IDLE_RIGHT_ARMOR
            elif self._direction == 1 and self._health == 1:
                self._sprite_start, self._sprite_end = IDLE_LEFT_NAKED
            else:
                self._sprite_start, self._sprite_end = IDLE_RIGHT_NAKED

        #________________RUNNING FRAME LOGIC________________

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
        
    def throw_Torch(self, arena: Arena):
        y = self.pos()[1] + 2
        x = self.pos()[0] if self._direction == 1 else self.pos()[0] + self.size()[0]
        # if self._direction == 1:
        #     x = self.pos()[0]
        # else:
        #     x = self.pos()[0] + self.size()[0]
        direction = 0
        if self._direction == 1:
            direction = -1
        else:
            direction = 1
        arena.spawn(Torch((x, y), direction))

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