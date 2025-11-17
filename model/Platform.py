from actor import Actor, Arena, Point
BASE1 =[
    ((564,164),(593,154)),
    ((583,141),(593,153)),
    ((597,137),(1130,126)),
    ((1159,170),(1182,181)),
    ((1148,154),(1167,169)),
    ((1130,139),(1151,153))
]
class Platform(Actor):
    def __init__(self, pos, pos_end):
        x1, y1 = pos
        x2, y2 = pos_end
        
        # calculating the angle top-left(min(x), min(y))
        self._x = min(x1, x2)
        self._y = min(y1, y2)
        
        # calculating the width and height (min(x), min(y))
        self._w = abs(x1 - x2)
        self._h = abs(y1 - y2)
    
    def pos(self) -> Point:
        return self._x, self._y
    def move(self,arena):
        pass 
    
    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return None