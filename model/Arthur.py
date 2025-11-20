from actor import Actor, Arena, Point
from random import choice, randint
from model.Torch import Torch
from model.Platform import Platform 
from model.Ladder import Ladder
from model.Zombie import Zombie
from model.Gravestone import Gravestone

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
][::-1]

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

THROW_RIGHT_ARMOR = [
    ((4,132), (27, 163)),
    ((29,132), (53, 163))
]

THROW_LEFT_ARMOR = []

for s in THROW_RIGHT_ARMOR:
    s_x = (s[1][0]-s[0][0])
    x = sprite_x - s[0][0] - s_x
    y = s[0][1]
    size_x = x + s_x
    size_y = s[1][1]
    THROW_LEFT_ARMOR.append(
        ((x, y), (size_x, size_y))
)
    
THROW_RIGHT_NAKED = [
    ((6, 164), (26, 193)),
    ((30, 164), (54, 193))
]

THROW_LEFT_NAKED = []

for s in THROW_RIGHT_NAKED:
    s_x = (s[1][0]-s[0][0])
    x = sprite_x - s[0][0] - s_x
    y = s[0][1]
    size_x = x + s_x
    size_y = s[1][1]
    THROW_LEFT_NAKED.append(
        ((x, y), (size_x, size_y))
)

    

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

CLIMBING_LADDER_ARMOR = [
    ((149, 132), (171, 162)),
    ((340, 132), (361, 162))
]

CLIMBING_LADDER_NAKED = [
    ((149, 163), (170, 193)),
    ((341, 163), (362, 193))
]

TOP_LADDER_ARMOR = [
    ((197, 131), (220, 157)),
    ((223, 131), (246, 149)),
]

class Arthur(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx, self._dy = 0, 0
        self._jump = False
        self.max_jump = 40
        self._djump = 15
        self._speed = 3
        self._health = 2
        self._attack_speed = 10
        self._attack_frame = self._attack_speed
        self._ladder_speed = 2

        self._grace_max = 3 * 60
        self._grace = self._grace_max
        
        #animation stats
        self._sprite_start, self._sprite_end = IDLE_RIGHT_ARMOR
        self._frame = 0
        self._duration_frame = 2
        self._direction = 0 
        self._jump_anim = False
        self._i_jump = None

        self._w, self._h = self.size()

        self._attack_animation = False
        self._attack_duration = 5

        self._ladder = None
        self._climb_duration = 3
        self._climb_frame = 0

        self._top_ladder = False

        
        

    def move(self, arena: Arena):
            G = 2
            aw, ah = arena.size()
            keys = arena.current_keys()

            #_________________        Input Control Zone        ________________
            self._dx = 0
            if "a" in keys:
                self._dx -= self._speed
                self._direction = 1
            elif "d" in keys:
                self._direction = 0
                self._dx += self._speed
            
            
            self._attack_frame = min(self._attack_frame+1, self._attack_speed)

            #________________       Collision Detection     ________________


            self._is_grounded = False

            # checking floor
            floor_y = ah - 45 
            if self._y + self._h >= floor_y and self._dy >= 0:
                self._y = floor_y - self._h
                self._dy = 0
                self._is_grounded = True
                self._jump_anim = False # get if we hit the ground

            # checking platforms
            for other in arena.collisions():
                if isinstance(other, (Platform,Gravestone)):
                    plat_x, plat_y = other.pos()
                    plat_w, plat_h = other.size()
                    if self._y + self._h > plat_y and self._dy and not(plat_y<=self._y <= plat_y+plat_h) > 0 and self._ladder == None:
                        self._y = plat_y - self._h
                        self._dy = 0
                        self._is_grounded = True
                        self._jump_anim = False 
                    
                    # 2. up ⤒ 
                    elif (plat_y<=self._y <= plat_y+plat_h) and self._dy < 0 and self._ladder == None:
                        print(plat_y + plat_h, self._y)
                        self._y = plat_y + plat_h + 1
                        self._dy = 0
                    
                    # 3. left ⇥ 
                    elif self._x < plat_x and self._dx > 0:
                        self._x = plat_x - self._w
                        self._dx = 0 # Block movement
                    
                    # 4.right ⇤ 
                    elif self._x + self._w > plat_x + plat_w and self._dx < 0:
                        self._x = plat_x + plat_w
                        self._dx = 0 # Block movement

            if ("s" in keys) and self._is_grounded:
                for other in arena.collisions():
                    if isinstance(other, Ladder):
                        x, y = other.pos()
                        x_end, y_end = other.end()
                        if (x <= self._x <= x_end) or (x <= self.end()[0] <= x_end) and self._is_grounded:
                            self._y += 7
                            self._ladder = other
                            ladder_x_size = abs(x-x_end)/2
                            self._x = x + ladder_x_size - self.size()[0]/2 -4
                            break
            # 2.3 jumping control 
            if ("Spacebar" in keys or "w" in keys) and self._is_grounded:
                for other in arena.collisions():
                    if isinstance(other, Ladder):
                        x, y = other.pos()
                        x_end, y_end = other.end()
                        if (x <= self._x <= x_end) or (x <= self.end()[0] <= x_end) and other._y<=self._y <=other._y+other.size()[1] and self._is_grounded:
                            self._ladder = other
                            self._y -= 2
                            ladder_x_size = abs(x-x_end)/2
                            self._x = x + ladder_x_size - self.size()[0]/2 -4
                            break
                if self._ladder == None:
                    self._dy = -self._djump
                    self._jump_anim = True
                    self._i_jump = None
            if "f" in keys and self._ladder == None:
                if self._attack_frame == self._attack_speed:
                    self.throw_Torch(arena)
                    self._attack_frame = 0
                    self._attack_animation = True
                

            # collisions with zombies
            for other in arena.collisions():
                if isinstance(other, Zombie):
                    x, y = other.pos()
                    w, h = other.size()
                    
                    #________________       Collision Detection     ________________
                    if (self._x >= x and self._x <= x+h) or  (x <= self._x + self.size()[0] <= x+h) :
                        if  ((y <= self._y <= y+h) or (y <= self._y + self.size()[1] <= y+h)) and self._grace == self._grace_max:
                            self.hit(arena)
                            other.hit(arena)
                            # self._grace = 0
            #  Apply physics and movement
            
            # Apply gravity

            self._dy += G 
            if self._ladder != None:
                # self._frame = 0
                self._dx = 0
                if ("Spacebar" in keys or "w" in keys):
                    self._dy = -self._ladder_speed
                    self._climb_frame += 1
                elif "s" in keys:
                    self._dy = +self._ladder_speed
                    self._climb_frame += 1
                else:
                    self._dy = 0

                if self.end()[1] + self._dy <= self._ladder.pos()[1]:
                    self._top_ladder = True
                if self.end()[1] + self._dy >= floor_y:
                    self._ladder = None
                    self._climb_frame = 0
                    self._top_ladder = False
            
            # Moving
            self._x += self._dx
            self._y += self._dy
            self._grace = min(self._grace + 1, self._grace_max)

            # Clamp at the border of the arena 
            self._x = min(max(self._x, 5), aw - self._w)
            self._y = max(self._y, 5) # Clamp



            #           ANIMATION ZONE 

            if self._ladder != None:
                if not self._top_ladder and self._health >= 2:
                    animation = CLIMBING_LADDER_ARMOR.copy()
                elif not self._top_ladder and self._health == 1:
                    animation = CLIMBING_LADDER_NAKED.copy()
                else:
                    animation = TOP_LADDER_ARMOR.copy()
                
                index = (self._climb_frame//self._climb_duration)%(len(animation))
                self._sprite_start, self._sprite_end = animation[index]

                if self._top_ladder and index == 1:
                    self._top_ladder = False
                    self._ladder = None
                
            elif self._attack_animation:
                if self._attack_frame == self._attack_speed:
                    self._attack_animation = False

                if self._direction == 1 and self._health == 2:
                    animation = THROW_LEFT_ARMOR.copy()
                elif self._direction == 0 and self._health == 2:
                    animation = THROW_RIGHT_ARMOR.copy()
                elif self._direction == 1 and self._health == 1:
                    animation = THROW_LEFT_NAKED.copy()
                else:
                    animation = THROW_RIGHT_NAKED.copy()
                index = (self._frame//self._attack_duration)%(len(animation))
                self._sprite_start, self._sprite_end = animation[index]
            #________________JUMP FRAME LOGIC________________
            elif self._jump_anim :
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
                # self._frame = 0
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


            if (not self.check_grace()) and self._frame%6 == 0:
                    #casual coordinate of the png where there's nothing
                    self._sprite_start, self._sprite_end = (-38, 42), (-16, 74)

            if self._frame >= 120:
                self._frame = 0
            else:
                self._frame += 1
            
    def throw_Torch(self, arena: Arena):
        y = self.pos()[1] + 2
        x = self.pos()[0] if self._direction == 1 else self.pos()[0] + self.size()[0]
        direction = 0
        if self._direction == 1:
            direction = -1
        else:
            direction = 1
        arena.spawn(Torch((x, y), direction))

    def hit(self, arena: Arena):
        #comment the line below to activate the immortality for testing
        # self._grace = 0
        # self._health -= 1
        if self._health <= 0:
            arena.kill(self)
            
    
    def lives(self):
        return self._health

    def check_grace(self):
        return self._grace == self._grace_max
    
    def reset_grace(self):
        self._grace = 0

    def pos(self) -> Point:
        return self._x, self._y

    def center(self) -> Point:
        sx, sy = self.size()
        return self._x + sx/2, self._y + sy/2
    
    def end(self) -> Point:
        x, y = self.pos()
        w, h = self.size()
        return x+w, y+h

    def size(self) -> Point:
        iw, ih = self._sprite_start
        ew, eh = self._sprite_end
        dw = ew-iw
        dh = eh-ih
        return dw, dh

    def sprite(self) -> Point:
        return self._sprite_start

def main():
    print(f"{JUMP_RIGHT_ARMOR=}")
    print(f"{JUMP_LEFT_ARMOR=}")
    print(f"{JUMP_RIGHT_NAKED=}")
    print(f"{JUMP_LEFT_NAKED=}")
    print(f"{RUNNING_RIGHT_ARMOR=}")
    print(f"{RUNNING_LEFT_ARMOR=}")
    print(f"{RUNNING_RIGHT_NAKED=}")
    print(f"{THROW_RIGHT_ARMOR=}")
    print(f"{THROW_LEFT_ARMOR=}")
    print(f"{THROW_RIGHT_NAKED=}")
    print(f"{THROW_LEFT_NAKED=}")
    print(f"{RUNNING_LEFT_NAKED=}")
    print(f"{CLIMBING_LADDER_ARMOR=}")
    print(f"{CLIMBING_LADDER_NAKED=}")
    print(f"{TOP_LADDER_ARMOR=}")

if __name__ == "__main__":
    main