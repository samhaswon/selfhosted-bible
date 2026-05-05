"""
Abstract Base class for API-based Bible objects
"""
from abc import abstractmethod, ABC
from typing import Optional
from bibles.bible import Bible
from bibles.compresscache import CompressCache
from bibles.passage import PassageInvalid, PassageNotFound


class APIBible(Bible, ABC):
    """ABC API Bible Implementation."""
    def __init__(self, cache_name: str) -> None:
        """
        :param cache_name: name of the cache file.
        """
        super().__init__()
        self.compress_cache = CompressCache(cache_name)

        # Caching
        try:
            self.cache: dict = self.compress_cache.load()
        except FileNotFoundError:
            # Initialize empty cache
            self.cache: dict = {
                book.name: {
                    str(chapter): [] for chapter in range(1, book.chapter_count + 1)
                } for book in super().books
            }

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Gets a chapter of the bible version.
        :param book: Name of the book to get from
        :param chapter: the chapter to get
        :return: dict of the chapter in the format
        {"book": bookname, "chapter": chapter_number, "verses":
            {'none': ["1 ...", "2 ..."]}}
        :raises: PassageInvalid for invalid passages (According to Bible ABC validator)
        """
        if super().has_passage(book, chapter):
            try:
                # Try to use the cache to retrieve the verse
                if len(self.cache[book][str(chapter)]) == 0:
                    self.api_return(book, chapter)
                # For versions with headings
                if ('verses' in self.cache[book][str(chapter)] and
                        len(self.cache[book][str(chapter)]['verses']) > 0):
                    return {
                        'book': book,
                        'chapter': chapter,
                        'verses': self.cache[book][str(chapter)]['verses'],
                        'footnotes':
                            self.cache[book][str(chapter)]['footnotes']
                            if 'footnotes' in self.cache[book][str(chapter)]
                            else ""
                    }
                # Versions without headings
                return {
                    'book': book,
                    'chapter': chapter,
                    'verses': {
                        'none': self.cache[book][str(chapter)]
                    }
                }
            except KeyError as exc:
                raise PassageNotFound(book + " " + str(chapter)) from exc
        raise PassageInvalid(book + " " + str(chapter))
    @abstractmethod
    def api_return(self, book: str, chapter: int) -> Optional[dict]:
        """
        Gets a passage from the API
        :param book: Name of the book to get (pre-validated)
        :param chapter: chapter number to get (pre-validated)
        :return: None
        """
        raise NotImplementedError
