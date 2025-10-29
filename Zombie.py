from actor import Actor, Arena, Point
from random import choice, randint
IDLE = (())
class Zombie(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 20, 20
        self._spawn = False 
        self._speed = 2
        self._dx = choice([-self._speed,self._speed]) 
        self._dy = 0

        self._facing_right = True
        self._moving = True

        self._distance_walkable = randint(150,300) #distanze che può percorrere
        self._distance_walked = 0


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
        return self._w, self._h

    def sprite(self) -> Point:
        return 0, 20