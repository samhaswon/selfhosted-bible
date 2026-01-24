"""
MSG
"""
import re
from typing import List
import requests
from bibles.passage import PassageInvalid, PassageNotFound
from bibles.bible import Bible
from bibles.bolls_translate import translate
from bibles.compresscache import CompressCache

class MSG(Bible):
    """MSG"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an MSG passage
        """
        super().__init__()
        self.__compress_cache = CompressCache('msg')

        # Caching
        try:
            self.__cache: dict = self.__compress_cache.load()
        except FileNotFoundError:
            # Initialize empty cache
            self.__cache: dict = {
                book.name: {
                    str(chapter): [] for chapter in range(1, book.chapter_count + 1)
                } for book in super().books
            }

        self.__api_url: str = "https://bolls.life/get-chapter/MSG/"

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Gets a chapter of the MSG
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
                if len(self.__cache[book][str(chapter)]) == 0:
                    self.__api_return(book, chapter)
                return {
                    'book': book,
                    'chapter': chapter,
                    'verses': {
                        'none': self.__cache[book][str(chapter)]
                    }
                }
            except KeyError as exc:
                raise PassageNotFound(book + " " + str(chapter)) from exc
        else:
            raise PassageInvalid(book + " " + str(chapter))

    def __api_return(self, book: str, chapter: int) -> None:
        """
        Gets a passage from the API
        :param book: Name of the book to get (pre-validated)
        :param chapter: chapter number to get (pre-validated)
        :return: None
        """
        tag_remover: re.Pattern = re.compile(r'<.*?>')
        try:
            response = requests.get(
                f"{self.__api_url}{translate(book)}/{chapter}/", timeout=20
            )
            response.raise_for_status()
            response = response.json()
            tmp_verses: List[str] = []
            for verse in response:
                tmp_verses.append(
                    str(verse['verse']) + " " + tag_remover.sub('', verse['text'])
                )
            self.__cache[book][str(chapter)] = tmp_verses
        except KeyError as exc:
            raise PassageInvalid(book + " " + str(chapter)) from exc
        except requests.HTTPError as exc:
            raise PassageNotFound(book + " " + str(chapter)) from exc

        # Save for every even chapter query
        if chapter % 2 == 0:
            self.__compress_cache.save(self.__cache)
