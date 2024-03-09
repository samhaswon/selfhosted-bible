from bibles.bible import Bible
from bibles.passage import PassageInvalid
from bibles.compresscache import CompressCache


class Darby(Bible):
    def __init__(self) -> None:
        super().__init__()
        self.__compress_cache = CompressCache('darby')
        self.__darby = self.__compress_cache.load()

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Returns a dictionary (Format: {book: "", chapter: 0, verses: ["1 content..."]}) of the chapter
        :param book: Name of the book
        :param chapter: chapter number
        :return:
        """
        if super().has_passage(book, chapter):
            book = book if book != "Psalms" else "Psalm"
            return {"book": book, "chapter": chapter, "verses": {'none': self.__darby[book][str(chapter)]}}
        else:
            raise PassageInvalid
