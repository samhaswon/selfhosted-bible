"""
Class for the ACV
"""
from bibles.bible import Bible
from bibles.passage import PassageInvalid
from bibles.compresscache import CompressCache


class ACV(Bible):
    """
    Class for the ACV
    """
    def __init__(self) -> None:
        super().__init__()
        self.__compress_cache = CompressCache('acv')
        self.__acv = self.__compress_cache.load()

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
                    'none': self.__acv[book][str(chapter)]
                }
            }
        raise PassageInvalid
