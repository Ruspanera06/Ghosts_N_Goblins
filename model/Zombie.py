from actor import Actor, Arena, Point
from random import choice, randint

#ZOMBIE_RISE_RIGHTs=   
# ===  (RISING FROM THE GROUND) === 
ZOMBIE_RISE_LEFT = [
    ((511, 64), (528, 97)),   # testa che emerge
    ((532, 64), (558, 97)),   # busto visibile
    ((561, 64), (581, 97)),   # metà corpo
    ((584, 64), (607, 97)),   # quasi fuori
]

# Mirroring a sinistra
sprite_x_inizio = 511
sprite_end = 794
ZOMBIE_RISE_RIGHT = []
for s in ZOMBIE_RISE_LEFT:
    x = sprite_end - (abs(sprite_x_inizio - s[0][0])) - (abs(s[0][0] - s[1][0]))
    y = s[0][1]
    size_x = x + (abs(s[0][0] - s[1][0]))
    size_y = s[1][1]
    ZOMBIE_RISE_RIGHT.append(((x, y), (size_x, size_y)))


# === Camminata (WALKING) ===
ZOMBIE_WALK_LEFT = [
    ((584, 64), (607, 97)),  # passo 1
    ((609, 64), (629, 97)),  # passo 2
    ((630, 64), (652, 97)),  # passo 3
]
ZOMBIE_WALK_LEFT = ZOMBIE_WALK_LEFT[::-1]
# print(ZOMBIE_WALK_LEFT[::-1])

# Mirroring a sinistra
sprite_x_inizio = 584
sprite_end = 721
ZOMBIE_WALK_RIGHT = []
for s in ZOMBIE_WALK_LEFT:
    x = sprite_end - (abs(sprite_x_inizio - s[0][0])) - (abs(s[0][0] - s[1][0]))
    y = s[0][1]
    size_x = x + (abs(s[0][0] - s[1][0]))
    size_y = s[1][1]
    ZOMBIE_WALK_RIGHT.append(((x, y), (size_x, size_y)))


class Zombie(Actor):
    def __init__(self, pos, dx):
        self._x, self._y = pos
        self._w, self._h = 23, 35
        self._spawn = True 
        self._speed = 2
        self._dx = dx*self._speed
        self._dy = 0
        self._direction = dx

        self._moving = True
        self._distance_walkable = randint(150,300) #distance it is gonna do
        self._distance_walked = 0

        self._points = 100


        #animation stats
        self._frame = 0
        self._duration_frame = 3
        self._sprite_start, self._sprite_end = ZOMBIE_RISE_RIGHT[0]  #start with the exit sprite
        self._spawn_frame = 10



    def move(self, arena: Arena):
        aw, ah = arena.size()
        ##########             WALKING LOGIC      ###############  
        if not self._spawn:
            self._distance_walked += abs(self._dx)
            if self._distance_walked < self._distance_walkable:
                self._moving = True 
                self._x += self._dx
            if self._distance_walked >= self._distance_walkable:
                self._frame = 0
                self._moving  = False
                self._spawn = True
                self._dx = 0

        ###########          ANIMATION ZONE      ################

        if self._spawn:
            #           RISING ANIMATION
            if self._moving:
                if self._dx  > 0:
                    animation = ZOMBIE_RISE_RIGHT.copy()
                else:
                    animation = ZOMBIE_RISE_LEFT.copy()
                if ((self._frame+1)//self._spawn_frame) >= len(animation):
                    self._spawn = not self._spawn
            #____________           BURY ANIMATION          _____________
            else:
                if self._direction > 0:
                    animation = ZOMBIE_RISE_RIGHT.copy()[::-1]
                else:
                    animation = ZOMBIE_RISE_LEFT.copy()[::-1]

                if ((self._frame+1)//self._spawn_frame) > len(animation)-1:
                    arena.kill(self)
            index = (self._frame//self._spawn_frame)%(len(animation))
            self._sprite_start, self._sprite_end = animation[index]
        #_________________       WALKING ANIMATION          ______________
        else:
            if self._dx != 0:
                if self._dx  > 0:
                    animation = ZOMBIE_WALK_RIGHT.copy()
                else:
                    animation = ZOMBIE_WALK_LEFT.copy()
                index = (self._frame//self._spawn_frame)%(len(animation))
                self._sprite_start, self._sprite_end = animation[index]

        
        if self._frame >= 120:
            self._frame = 0
        else:
            self._frame += 1

        self._x = min(max(self._x, 0), aw - self._w)  # clamp
        self._y = min(max(self._y, 0), ah - self._h)  # clamp

    def hit(self, arena: Arena):
        arena.add_score(self._points)
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

def main():
    print(f"{ZOMBIE_RISE_LEFT=}")
    print(f"{ZOMBIE_RISE_RIGHT=}")
    print(f"{ZOMBIE_WALK_LEFT=}")
    print(f"{ZOMBIE_WALK_RIGHT=}")

if __name__ == "__main__":
    main()