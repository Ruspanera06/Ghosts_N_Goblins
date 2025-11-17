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
        
        # Calcola e memorizza l'angolo in alto a sinistra (min(x), min(y))
        self._x = min(x1, x2)
        self._y = min(y1, y2)
        
        # Calcola e memorizza larghezza e altezza (sempre positive)
        self._w = abs(x1 - x2)
        self._h = abs(y1 - y2)
    
    def pos(self) -> Point:
        # Restituisce sempre l'angolo in alto a sinistra memorizzato
        return self._x, self._y
    def move(self,arena):
        pass 
    
    def size(self) -> Point:
        return self._w, self._h

    # Il metodo pos_end() non è più necessario per la logica interna,
    # ma puoi tenerlo se ti serve per altri motivi.

    def sprite(self) -> Point:
        return None