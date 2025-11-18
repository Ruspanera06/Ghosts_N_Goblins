from actor import Actor, Arena, Point
from math import sin, cos, dist, radians, atan2
from random import randrange
from model.Eyeball import Eyeball


SHOOT_ANIMATION = [
    (),
    (),
]

IDDLE_ANIMATION_LEFT = [
    ((563, 206),(580, 239)),
    ((581, 206),(598, 239)),
    ((599, 206),(616, 239)),
    ((617, 206),(634, 239)),
    ((635, 206),(652, 239))
]

class Plant(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._fire_rate = 30
        self._actual_fire = self._fire_rate
        self._bullet_speed = 3
        self._direction = -1
        self._shoot = False
        self._points = 200
        self._sprite_start, self._sprite_end = IDDLE_ANIMATION_LEFT[0]

    def move(self, arena: Arena):
        n = randrange(100)
        if n == 0 and self._actual_fire==self._fire_rate:
            self.shoot(arena)
            self._actual_fire = 0
        
        self._actual_fire = min(self._actual_fire + 1, self._fire_rate)

        
        

    def hit(self, arena: Arena):
        arena.add_score(self._points)
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y
    
    def end(self) -> Point:
        x, y = self.pos()
        w, h = self.size()
        return x+w, y+h
    
    def center(self) -> Point:
        sx, sy = self.size()
        return self._x + sx/2, self._y + sy/2

    def size(self) -> Point:
        iw, ih = self._sprite_start
        ew, eh = self._sprite_end
        dw = ew-iw
        dh = eh-ih
        return dw, dh

    def shoot(self, arena: Arena):
        from model.Arthur import Arthur
        for other in arena.actors():
            if isinstance(other, Arthur):
                x, y =  other.center()
                delta_x = x - self._x
                delta_y = y - self._y
                angle  = atan2(delta_y, delta_x)
                dx = cos(angle) * self._bullet_speed
                dy = sin(angle) * self._bullet_speed
                arena.spawn(Eyeball((self._x-15, self._y-11), dx, dy))




    def sprite(self) -> Point:
        return self._sprite_start