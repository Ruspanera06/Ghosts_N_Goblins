from actor import Actor, Arena, Point
from random import choice, randint

sprite_x = 652
#ZOMBIE_RISE_RIGHTs=   
# === Uscita dal terreno (RISING) ===
ZOMBIE_RISE_RIGHT = [
    ((630, 70), (652, 96)),# testa che emerge
    ((654, 70), (676, 98)),   # busto visibile
    ((678, 70), (700, 100)),  # metà corpo
    ((702, 70), (724, 102)),  # quasi fuori
    ((726, 70), (748, 104)),  # in piedi
]

# Mirroring a sinistra
ZOMBIE_RISE_LEFT = []
for s in ZOMBIE_RISE_RIGHT:
    x = sprite_x - s[0][0] - s[1][0]
    y = s[0][1]
    size_x = x + s[1][0]
    size_y = s[1][1]
    ZOMBIE_RISE_LEFT.append(((x, y), (size_x, size_y)))


# === Camminata (WALKING) ===
ZOMBIE_WALK_RIGHT = [
    ((630, 110), (652, 140)),  # passo 1
    ((654, 110), (676, 142)),  # passo 2
    ((678, 110), (700, 142)),  # passo 3
    ((702, 110), (724, 142)),  # passo 4
    ((726, 110), (748, 142)),  # passo 5
    ((750, 110), (772, 142)),  # passo 6 (facoltativo)
]

# Mirroring a sinistra
ZOMBIE_WALK_LEFT = []
for s in ZOMBIE_WALK_RIGHT:
    x = sprite_x - s[0][0] - s[1][0]
    y = s[0][1]
    size_x = x + s[1][0]
    size_y = s[1][1]
    ZOMBIE_WALK_LEFT.append(((x, y), (size_x, size_y)))



class Zombie(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 23, 35
        self._spawn = False 
        self._speed = 2
        self._dx = choice([-self._speed,self._speed]) 
        self._dy = 0

        self._facing_right = True
        self._moving = True

        self._distance_walkable = randint(150,300) #distanze che può percorrere
        self._distance_walked = 0

        self._sprite_start, self._sprite_end = ZOMBIE_RISE_RIGHT[0]  #inizia con lo sprite di uscita

    def move(self, arena: Arena):
        aw, ah = arena.size()
        if self._moving:
            self._x += self._dx 

        if self._x <=0 or self._x+self._w >= aw: #"rimbalzo zombie" contro l'arena
            self._dx = -self._dx
            self._moving = True

        if self._distance_walked < self._distance_walkable:
            self._moving = True 
            self._distance_walked += abs(self._dx) #aggiungo i passi anche se sono negativi

        elif self._distance_walked >= self._distance_walkable:
            self._moving  = False
            self._dx = 0
            self._dy = 0
             

        if self._dx>0: #dove lo zombi guarda (per modifica sprite..)"
            self._facing_right = True 
        else:
            self._facing_right = False     

        self._x = min(max(self._x, 0), aw - self._w)  # clamp
        self._y = min(max(self._y, 0), ah - self._h)  # clamp

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