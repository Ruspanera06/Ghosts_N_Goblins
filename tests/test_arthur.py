import unittest
from model.Arthur import Arthur
from model.Zombie import Zombie
from model.Platform import Platform
from actor import Arena

class TestTorch(unittest.TestCase):
    # python -m unittest tests/test_arthur.py

    def collide(self, art: Arthur, z: Zombie):
        x, y = z.pos()
        w, h = z.size()
        if (art._x >= x and art._x <= x+h) or  (x <= art._x + art.size()[0] <= x+h) :
            if  ((y <= art._y <= y+h) or (y <= art._y + art.size()[1] <= y+h)):
                return True
        return False
    
    def test_collision_zombie(self):
        art = Arthur((100, 150))
        z1 = Zombie((100, 150), 1)
        z2 = Zombie((100 - z1.size()[0], 150), 1)
        z3 = Zombie((100 + z1.size()[0], 150), -1)
        self.assertTrue(self.collide(art, z1))
        self.assertTrue(self.collide(art, z2))
        self.assertTrue(self.collide(art, z3))
    
    def test_collision_platform(self):
        a = Arena((3585, 239))
        art = Arthur((100, 30))
        p = Platform((80, art.pos()[1]+art.size()[1]+2), (120, art.pos()[1]+art.size()[1]+21))
        a.spawn(art)
        a.spawn(p)
        art.move(a)
        self.assertAlmostEqual(art.pos()[1]+art.size()[1],  p.pos()[1])



if __name__ == "__main__":
    unittest.main()



