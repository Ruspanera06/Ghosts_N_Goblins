import unittest
from model.Arthur import Arthur
from model.Zombie import Zombie
from actor import Arena

class TestTorch(unittest.TestCase):

    def test_collision_zombie(self):
        a = Arena((3585, 239))
        a.spawn(a)
        a.spawn(Zombie((100, 150)))
        






if __name__ == "__main__":
    unittest.main()



