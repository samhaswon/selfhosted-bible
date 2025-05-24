"""
Class for the BSB
"""
from bibles.bible import Bible
from bibles.passage import PassageInvalid
from bibles.compresscache import CompressCache


class BSB(Bible):
    """
    Class for the BSB
    """
    def __init__(self) -> None:
        """
        Class instantiation for the ACV
        """
        super().__init__()
        self.__compress_cache = CompressCache("bsb")
        self.__bsb = self.__compress_cache.load()

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Returns a dictionary
        (Format: {book: "", chapter: 0, verses: ["1 content..."]})
        of the chapter.
        :param book: Name of the book.
        :param chapter: Chapter number.
        :return:
        """
        if super().has_passage(book, chapter):
            return {
                "book": book,
                "chapter": chapter,
                "verses": {
                    'none': self.__bsb[book][str(chapter)]
                }
            }
        raise PassageInvalid
