from unittest import TestCase
from bibles.nkjv import NKJV


class TestNKJV(TestCase):
    def setUp(self) -> None:
        self.nkjv = NKJV()
    def test_get_passage(self):
        exodus_3 = self.nkjv.get_passage("Exodus", 3)
        self.assertEqual("1 Now Moses was tending the flock of Jethro his father-in-law, the priest of Midian. And he "
                         "led the flock to the back of the desert, and came to Horeb, the mountain of God.",
                         exodus_3['verses']['none'][0])
