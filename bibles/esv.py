from bibles.passage import Passage, PassageInvalid
from bibles.book import Book
from typing import List
from bibles.bible import Bible


class ESV(Bible):
    def __init__(self, key_in=(False, "")):
        """
        Gets a JSON formatted dictionary of an ESV passage
        :param key_in: (True, "API key"), with the default (False, "") being reading from the file api-key.txt
        """
        super().__init__()
        self.__passage: Passage = Passage(open("api-key.txt", "r").read() if not key_in[0] else key_in[1])

    @property
    def books(self) -> List[Book]:
        return super().books

    def get_passage(self, book: str, chapter: int):
        """
        Gets a book of the ESV
        :param book: Name of the book to get from
        :param chapter: chapter to get
        :return: dictionary of the chapter
        :raises: PassageInvalid for invalid passages
        """
        if Book(book, chapter) in super().books:
            return self.__passage.get_chapter_esv_json(book + " " + str(chapter))
        else:
            raise PassageInvalid(book + " " + str(chapter))
