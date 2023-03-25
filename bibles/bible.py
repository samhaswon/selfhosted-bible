from bibles.book import Book
from typing import List
from abc import ABC, abstractmethod
from multipledispatch import dispatch
from typing import Tuple


class Bible(ABC):
    """
    Abstract class for future implementation of other versions
    """

    def __init__(self) -> None:
        books_of_the_bible: List[Tuple[str, int]] = [("Genesis", 50),
                                                     ("Exodus", 40),
                                                     ("Leviticus", 27),
                                                     ("Numbers", 36),
                                                     ("Deuteronomy", 34),
                                                     ("Joshua", 24),
                                                     ("Judges", 21),
                                                     ("Ruth", 4),
                                                     ("1 Samuel", 31),
                                                     ("2 Samuel", 24),
                                                     ("1 Kings", 22),
                                                     ("2 Kings", 25),
                                                     ("1 Chronicles", 29),
                                                     ("2 Chronicles", 36),
                                                     ("Ezra", 10),
                                                     ("Nehemiah", 13),
                                                     ("Esther", 10),
                                                     ("Job", 42),
                                                     ("Psalms", 150),
                                                     ("Proverbs", 31),
                                                     ("Ecclesiastes", 12),
                                                     ("Song of Solomon", 8),
                                                     ("Isaiah", 66),
                                                     ("Jeremiah", 52),
                                                     ("Lamentations", 5),
                                                     ("Ezekiel", 48),
                                                     ("Daniel", 12),
                                                     ("Hosea", 14),
                                                     ("Joel", 3),
                                                     ("Amos", 9),
                                                     ("Obadiah", 1),
                                                     ("Jonah", 4),
                                                     ("Micah", 7),
                                                     ("Nahum", 3),
                                                     ("Habakkuk", 3),
                                                     ("Zephaniah", 3),
                                                     ("Haggai", 2),
                                                     ("Zechariah", 14),
                                                     ("Malachi", 4),
                                                     ("Matthew", 28),
                                                     ("Mark", 16),
                                                     ("Luke", 24),
                                                     ("John", 21),
                                                     ("Acts", 28),
                                                     ("Romans", 16),
                                                     ("1 Corinthians", 16),
                                                     ("2 Corinthians", 13),
                                                     ("Galatians", 6),
                                                     ("Ephesians", 6),
                                                     ("Philippians", 4),
                                                     ("Colossians", 4),
                                                     ("1 Thessalonians", 5),
                                                     ("2 Thessalonians", 3),
                                                     ("1 Timothy", 6),
                                                     ("2 Timothy", 4),
                                                     ("Titus", 3),
                                                     ("Philemon", 1),
                                                     ("Hebrews", 13),
                                                     ("James", 5),
                                                     ("1 Peter", 5),
                                                     ("2 Peter", 3),
                                                     ("1 John", 5),
                                                     ("2 John", 1),
                                                     ("3 John", 1),
                                                     ("Jude", 1),
                                                     ("Revelation", 22)]
        self.__books: List[Book] = [Book(title, chapters) for title, chapters in books_of_the_bible]
        self.__books_of_the_bible: dict = dict(books_of_the_bible)

    @property
    def books(self) -> List[Book]:
        return self.__books

    @property
    def books_of_the_bible(self) -> dict:
        return self.__books_of_the_bible

    @abstractmethod
    def get_passage(self, book, chapter) -> dict:
        raise NotImplementedError

    @dispatch(str, str)
    def next_passage(self, book: str, chapter: str) -> Tuple[str, str]:
        return self.next_passage(book, int(chapter))

    @dispatch(str, int)
    def next_passage(self, book: str, chapter: int) -> Tuple[str, str]:
        it_books = iter(self.__books_of_the_bible)
        for key in it_books:
            if key == book:
                if chapter == self.__books_of_the_bible[key]:
                    return next(it_books, "Genesis"), "1"
                else:
                    return book, str(chapter + 1)

    @dispatch(str, str)
    def previous_passage(self, book: str, chapter: str) -> Tuple[str, str]:
        return self.previous_passage(book, int(chapter))

    @dispatch(str, int)
    def previous_passage(self, book: str, chapter: int) -> Tuple[str, str]:
        it_books = iter(self.__books_of_the_bible)
        previous_key = "Revelation"
        for key in it_books:
            if key == book:
                if chapter == 1:
                    return previous_key, str(self.__books_of_the_bible[previous_key])
                else:
                    return book, str(chapter - 1)
            else:
                previous_key = key

    def has_passage(self, book_name: str, chapter: int) -> bool:
        """
        Finds out if a passage is valid
        :param book_name: Name of the book to try
        :param chapter: Chapter of the book to try
        :return: True if passage is valid, False if passage is invalid
        """
        try:
            return 0 < chapter <= self.__books_of_the_bible[book_name]
        except KeyError:
            return False

    def chapter_count(self, book_name: str) -> int:
        """
        Gets the chapter count of a given book
        :param book_name: Name of the book to get the chapter of
        :return: Number of chapters in the book or 0 if invalid
        """
        try:
            return self.__books_of_the_bible[book_name]
        except KeyError:
            return 0
