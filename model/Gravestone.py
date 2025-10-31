from actor import Actor, Arena, Point
IDLE = [ 
    ((50,186),(65,201)), 
    ((242,186),(257,201)),
    ((418,188),(433,201)), #diffrent 
    ((530,186),(545,201)), 
    ((754,186),(769,201)), 
    ((770,108),(785,121)), #platform grave diffrent 
    ((866,106),(881,121)), #platform grave 
    ((962,108),(977,121)), #platforn grave diffrent 
    ((962,186),(977,201)), 
    ((1106,186),(1121,201)), 
    ((1266,188),(1281,201)), 
    ((1522,186),(1537,201)) 
]

class Gravestone(Actor):
    def __init__(self, pos, pos_end):
        self._x, self._y = pos
        self._end_x, self._end_y = pos_end
    
    def pos(self) -> Point:
        return self._x, self._y
    
    def pos_end(self) -> Point:
        return self._end_x, self._end_y

    def size(self) -> Point:
        x, y = self.pos()
        end_x, end_y = self.pos_end()
        dx = abs(x, end_x)
        dy = abs(y, end_y)
        return dx, dy

    def sprite(self) -> Point:
        return None