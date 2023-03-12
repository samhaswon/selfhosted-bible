from unittest import TestCase
from bibles.bible import Bible


class BibleTest(Bible):
    def __init__(self):
        super().__init__()

    def get_passage(self, book, chapter):
        pass


class TestBible(TestCase):
    def setUp(self) -> None:
        self.bible = BibleTest()

    def test_previous_passage(self):
        self.assertEqual(self.bible.previous_passage("John", 3), ("John", "2"))
        self.assertEqual(self.bible.previous_passage("John", 1), ("Luke", "24"))
        self.assertEqual(self.bible.previous_passage("Genesis", 1), ("Revelation", "22"))

    def test_next_passage(self):
        self.assertEqual(self.bible.next_passage("John", 4), ("John", "5"))
        self.assertEqual(self.bible.next_passage("Luke", 24), ("John", "1"))
        self.assertEqual(self.bible.next_passage("Revelation", 22), ("Genesis", "1"))

    def test_has_passage(self):
        self.assertTrue(self.bible.has_passage("Genesis", 50))
        self.assertFalse(self.bible.has_passage("Genesis", 51))
