from unittest import TestCase
from bibles.esv import ESV


class TestESV(TestCase):
    def setUp(self) -> None:
        with open("../esv-api-key.txt", "r") as key_in:
            key = key_in.read()
        self.esv_obj = ESV((True, key))

    def test_get_passage(self):
        passage = self.esv_obj.get_passage("Isaiah", 13)
        self.assertEqual(1, len(passage['verses']))
        passage2 = self.esv_obj.get_passage("Matthew", 5)
        self.assertEqual(10, len(passage2['verses']))
        passage3 = self.esv_obj.get_passage("John", 12)
        self.assertEqual(7, len(passage3['verses']))
