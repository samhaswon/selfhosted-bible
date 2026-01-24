"""
Test NET passage retrieval
"""
import time
from unittest import TestCase
from bibles.net import NET


class TestNET(TestCase):
    """Test the NET"""
    def setUp(self) -> None:
        self.net = NET()

    def test_get_passage(self):
        """Test passage retrieval for the NET"""
        john_3 = self.net.get_passage("John", 3)
        self.assertEqual(36, len(john_3['verses']['none']))

        for book, chapter_count in self.net.books_of_the_bible.items():
            for chapter in range(1, chapter_count + 1):
                self.net.get_passage(book, chapter)
                print(f"Got {book} {chapter}")
                time.sleep(2)
