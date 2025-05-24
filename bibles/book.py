"""
Base class representing a book of the Bible
"""

class Book:
    """
    Defines a book of the Bible. Used for safety constraints
    """
    def __init__(self, title: str, chapter_count: int) -> None:
        """
        :param title: The title of the book.
        :param chapter_count: The number of chapters in the book.
        """
        self.__name: str = title
        self.__chapter_count: int = chapter_count

    @property
    def name(self) -> str:
        """
        The name of the book.
        """
        return self.__name

    @property
    def chapter_count(self) -> int:
        """
        The number of chapters in the book.
        """
        return self.__chapter_count

    def __eq__(self, other) -> bool:
        return other.name == self.__name
