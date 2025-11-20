import unittest
from model.Torch import Torch
from unittest.mock import Mock
from actor import Arena

class TestTorch(unittest.TestCase):
    # python -m unittest tests/test_torch.py
    def test_move(self):
        start_x, start_y = 50, 50
        dx = 1
        speed = 3
        t = Torch((start_x, start_y), dx)

        arena = Mock()
        arena.size.return_value = (480, 500)
        arena.collisions.return_value = []

        t.move(arena)
        self.assertTrue(t.pos() == (start_x + speed*dx, start_y -4+0.3))
    
    def test_collision_ground(self):
        arena = Mock()
        arena.size.return_value = (480, 500)
        arena.collisions.return_value = []
        aw, ah = arena.size()
        ah -= 30
        dx = 1
        speed = 3
        start_x, start_y = 50, ah-1
        t = Torch((start_x, start_y), dx)
        i = 0
        t.move(arena)
        t.move(arena)
        for i in range(23):
            t.move(arena)
        # while t._y != ah-t.size()[1]+2:
        #     print(t._y, ah-t.size()[1]+2)
        #     i+=1
        #     t.move(arena)
        # print(i)
        self.assertEqual(t.pos()[1] , ah-t.size()[1]+2)





if __name__ == "__main__":
    unittest.main()
