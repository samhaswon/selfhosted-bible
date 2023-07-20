from bibles.passage import PassageInvalid, PassageNotFound
from typing import List
from bibles.bible import Bible
from requests import get, HTTPError
import re
from bibles.compresscache import CompressCache


class NET(Bible):
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an NET passage
        """
        super().__init__()
        self.__compress_cache = CompressCache('net')

        # Caching
        try:
            self.__cache: dict = self.__compress_cache.load()
        except FileNotFoundError:
            # Initialize empty cache
            self.__cache: dict = {book.name: {str(chapter): [] for chapter in range(1, book.chapter_count + 1)} for
                                  book in super().books}

        self.__API_URL: str = "http://labs.bible.org/api/?passage="

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Gets a chapter of the NET
        :param book: Name of the book to get from
        :param chapter: the chapter to get
        :return: dict of the chapter in the format {"book": bookname, "chapter": chapter_number, "verses":
            {'none': ["1 ...", "2 ..."]}}
        :raises: PassageInvalid for invalid passages (According to Bible ABC validator)
        """
        if super().has_passage(book, chapter):
            try:
                # Try to use the cache to retrieve the verse
                if not len(self.__cache[book][str(chapter)]):
                    self.__api_return(book, chapter)
                return {'book': book, 'chapter': chapter, 'verses': {'none': self.__cache[book][str(chapter)]}}
            except KeyError:
                raise PassageNotFound(book + " " + str(chapter))
        else:
            raise PassageInvalid(book + " " + str(chapter))

    def __api_return(self, book: str, chapter: int) -> dict:
        """
        Gets a passage from the API
        :param book: Name of the book to get (pre-validated)
        :param chapter: chapter number to get (pre-validated)
        :return: None
        """
        tag_remover: re.Pattern = re.compile(r'<.*?>')
        try:
            response = get(f"{self.__API_URL}{book} {chapter}&type=json")
            response.raise_for_status()
            response = response.json()
            tmp_verses: List[str] = []
            for verse in response:
                tmp_verses.append(verse['verse'] + " " + tag_remover.sub('', verse['text']))
            self.__cache[book][str(chapter)] = tmp_verses
        except KeyError:
            return {"API Overloaded?": "If this keeps happening, the app could be heavily throttled"}
        except HTTPError:
            return {"Issue connecting to the NET API":
                     "Try checking the status of the NET API and the server's network connection"}

        # Save for every even chapter query
        if chapter % 2 == 0:
            self.__compress_cache.save(self.__cache)
