from actor import Actor, Point

GRAVESTONE_SPRITE_POS = (250, 100)  
GRAVESTONE_SPRITE_SIZE = (10, 34) 
POSS = [ 
    ((50,186),(65,201)), 
    ((242,186),(257,201)),
    ((418,188),(433,201)),  
    ((530,186),(545,201)), 
    ((754,186),(769,201)), 
    ((770,108),(785,121)), 
    ((866,106),(881,121)),  
    ((962,108),(977,121)), 
    ((962,186),(977,201)), 
    ((1106,186),(1121,201)), 
    ((1266,188),(1281,201)), 
    ((1522,186),(1537,201)) 
]

class Gravestone(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = GRAVESTONE_SPRITE_SIZE
    
    def pos(self) -> Point:
        return self._x, self._y
    
    def size(self) -> Point:
        return self._w, self._h

    def move(self, arena):
        pass  
    
    def sprite(self) -> Point:
        return GRAVESTONE_SPRITE_POS