"""
Class for the BBE version
"""
from bibles.bible import Bible
from bibles.passage import PassageInvalid
from bibles.compresscache import CompressCache


class BBE(Bible):
    """
    Class for the BBE version
    """
    def __init__(self) -> None:
        super().__init__()
        self.__compress_cache = CompressCache('bbe')
        self.__bbe = self.__compress_cache.load()

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Returns a dictionary
        (Format: {book: "", chapter: 0, verses: ["1 content..."]})
        of the chapter
        :param book: Name of the book
        :param chapter: chapter number
        :return:
        """
        if super().has_passage(book, chapter):
            return {
                "book": book,
                "chapter": chapter,
                "verses": {
                    'none': self.__bbe[book][str(chapter)]
                }
            }
        raise PassageInvalid
