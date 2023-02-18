from passage import Passage, PassageInvalid
from cache_access import CacheAccess
from book import Book
from typing import List
from bible import Bible


class ESV(Bible):
    def __init__(self, use_cache=False, key_in=(False, "")):
        """
        Gets a JSON formatted dictionary of an ESV passage
        :param use_cache: Whether to use MongoDB for the cache or not. Requires MongoDB to be running at 127.0.0.1 on
        port 27017 (unless Cache access constructor is changed).
        :param key_in: (True, "API key"), with the default (False, "") being reading from the file api-key.txt
        """
        super().__init__()
        self.__passage: Passage = Passage(open("api-key.txt", "r").read() if not key_in[0] else key_in[1])
        self.__cache: CacheAccess = CacheAccess() if use_cache else None
        self.__use_cache: bool = use_cache

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
        if self.__use_cache and Book(book, chapter) in super().books:
            self.__cache.get_chapter(book, chapter)
        elif Book(book, chapter) in super().books:
            return self.__passage.get_chapter_esv_json(book + " " + str(chapter))
        else:
            raise PassageInvalid(book + " " + str(chapter))
