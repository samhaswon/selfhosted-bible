class Book(object):
    """
    Defines a book of the Bible. Used for safety constraints
    """
    def __init__(self, title: str, chapter_count: int):
        self.__name: str = title
        self.__chapter_count: int = chapter_count

    @property
    def name(self) -> str:
        return self.__name

    @property
    def chapter_count(self) -> int:
        return self.__chapter_count

    def __eq__(self, other) -> bool:
        return other.name == self.__name
