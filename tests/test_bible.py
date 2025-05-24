"""
Test the ABC Bible methods
"""
from unittest import TestCase
from bibles.bible import Bible


class BibleTest(Bible):
    """
    Test class "implementing" the get_passage method.
    """
    def get_passage(self, book, chapter) -> None:
        """
        An "implementation" of get_passage.
        """


class TestBible(TestCase):
    """
    Test the ABC Bible methods
    """
    def setUp(self) -> None:
        self.bible = BibleTest()

    def test_previous_passage(self):
        """Make sure that previous passage does things right"""
        self.assertEqual(self.bible.previous_passage("John", 3), ("John", "2"))
        self.assertEqual(self.bible.previous_passage("John", "1"), ("Luke", "24"))
        self.assertEqual(self.bible.previous_passage("Genesis", 1), ("Revelation", "22"))

    def test_next_passage(self):
        """Make sure that next passage does things right"""
        self.assertEqual(self.bible.next_passage("John", 4), ("John", "5"))
        self.assertEqual(self.bible.next_passage("Luke", "24"), ("John", "1"))
        self.assertEqual(self.bible.next_passage("Revelation", 22), ("Genesis", "1"))

    def test_has_passage(self):
        """Make sure that has passage does things right"""
        self.assertTrue(self.bible.has_passage("Genesis", 50))
        self.assertFalse(self.bible.has_passage("Genesis", 51))
