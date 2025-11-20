import unittest
from unittest.mock import Mock
from model.Arthur import Arthur
from model.Zombie import Zombie

class TestArthur(unittest.TestCase):
    # python -m unittest tests/test_arthur.py

    def collide(self, art: Arthur, z: Zombie):
        x, y = z.pos()
        w, h = z.size()
        if (art._x >= x and art._x <= x+h) or  (x <= art._x + art.size()[0] <= x+h) :
            if  ((y <= art._y <= y+h) or (y <= art._y + art.size()[1] <= y+h)):
                return True
        return False
    
    def test_collision_zombie(self):
        arthur = Arthur((100, 150))
        z1 = Mock()
        z1.pos.return_value = (100, 150)
        z1.size.return_value = (50, 50)

        z2 = Mock()
        z2.pos.return_value = (100 - 50, 150)
        z2.size.return_value = (50, 50)

        z3 = Mock()
        z3.pos.return_value = (100 + 50, 150)
        z3.size.return_value = (50, 50)

        self.assertTrue(self.collide(arthur, z1))
        self.assertTrue(self.collide(arthur, z2))
        self.assertTrue(not self.collide(arthur, z3))
    
    def test_collision_platform(self):
        arthur = Arthur((100, 315))

        arena = Mock()
        arena.size.return_value = (480, 500)
        arena.current_keys.return_value = []

        platform = Mock()
        platform.pos.return_value = (80, 317+arthur.size()[1])
        platform.size.return_value = (80, 20)

        arena.collisions.return_value = [platform]

        arthur.move(arena)

        self.assertTrue(arthur.pos()[1]+ arthur.size()[1] == platform.pos()[1])



if __name__ == "__main__":
    unittest.main()



