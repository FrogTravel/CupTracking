from script1 import get_center_from_box
import unittest


class TestTracker(unittest.TestCase):
    def test_center_from_box(self):
        box = [[0, 10], [10, 10], [10, 0], [0, 0]]
        self.assertEqual(get_center_from_box(box), [5, 5])
