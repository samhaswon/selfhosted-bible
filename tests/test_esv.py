"""
Test ESV stuff
"""
from unittest import TestCase
from bibles.esv import ESV


class TestESV(TestCase):
    """
    Test ESV passage retrieval
    """
    def setUp(self) -> None:
        self.esv_obj = ESV()

    def test_get_passage(self):
        """Get passages from the ESV"""
        passage = self.esv_obj.get_passage("Isaiah", 13)
        self.assertEqual(1, len(passage['verses']))
        passage2 = self.esv_obj.get_passage("Matthew", 5)
        self.assertEqual(10, len(passage2['verses']))
        passage3 = self.esv_obj.get_passage("John", 12)
        self.assertEqual(7, len(passage3['verses']))
