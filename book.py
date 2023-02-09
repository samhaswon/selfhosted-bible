class Book(object):
    """
    Defines a book of the Bible. Used for safety constraints
    """
    def __init__(self, title: str, chapter_count: int):
        self.__title = title
        self.__chapter_count = chapter_count

    @property
    def title(self) -> str:
        return self.__title

    @property
    def chapter_count(self) -> int:
        return self.__chapter_count

    def __eq__(self, other):
        return other.title == self.__title
