import unittest
from model.Torch import Torch
from actor import Arena

class TestTorch(unittest.TestCase):
    def test_move(self):
        start_x, start_y = 50, 50
        dx = 1
        speed = 3
        t = Torch((start_x, start_y), dx)
        t.move(Arena((3585, 239)))
        self.assertTrue(t.pos() == (start_x + speed*dx, start_y + 0.3))
    
    def test_collision_ground(self):
        dx = 1
        speed = 3
        a = Arena((3585, 239))
        aw, ah = a.size()
        ah -= 30
        start_x, start_y = 50, ah - 0.3
        t = Torch((start_x, start_y), dx)
        t._y += 0.3
        self.assertTrue(ah - t._h == t._y - t._h)





if __name__ == "__main__":
    unittest.main()
