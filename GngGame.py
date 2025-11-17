from random import choice, randrange, randint
from actor import Actor, Arena, Point
from model.Arthur import Arthur
from math import cos, sin, radians
from model.Zombie import Zombie
from model.Gravestone import Gravestone 
from model.Platform import Platform 
from model.Flame import Flame
from model.Torch import Torch
import actor
import json
class GngGame(actor.Arena):
    def __init__(self, size=(3585, 239), time = 120*30):
        super().__init__(size)
        with open("config.json") as f:
            data = json.load(f)
        self.spawn(data["arthur"]["position"])
        for x in data["BASE1"]:
            self.spawn(Platform(tuple(x[0]), tuple(x[1])))
        
        self._time = time
    
    def spawn_zombie(self):
        n = randrange(150)
        if n == 0:
            from model.Arthur import Arthur
            for x in self.actors():
                if isinstance(x, Arthur):
                    r = randint(20, 200)
                    direction = choice([1, -1])
                    z_pos = ((x.pos()[0] + (-1*direction*r)), self.size()[1] - 69)
                    from model.Zombie import Zombie
                    self.spawn(Zombie(z_pos, direction))
                    break


    def game_over(self) -> bool:
        return self.lives() <= 0

    def game_won(self) -> bool:
        return self.time() <= 0

    def lives(self) -> int:
        from model.Arthur import Arthur
        for a in self.actors():
            if isinstance(a, Arthur):
                return a.lives()
        return 0

    def time(self) -> int:
        return self._time - self.count()
