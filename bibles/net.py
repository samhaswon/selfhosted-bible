from bibles.passage import PassageInvalid, PassageNotFound
from typing import List
from bibles.bible import Bible
from requests import get, HTTPError
# (testing cache) import requests_cache
import json
import re


class NET(Bible):
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an NET passage
        """
        super().__init__()
        # (testing cache) requests_cache.install_cache('verses', expire_after=999999999)

        # Caching
        try:
            with open('bibles/json_bibles/net.json', 'r') as cache_in:
                self.__cache: dict = json.load(cache_in)
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
                return self.__api_return(book, chapter)
        else:
            raise PassageInvalid(book + " " + str(chapter))

    def __api_return(self, book: str, chapter: int) -> dict:
        """
        Gets a passage from the API
        :param book: Name of the book to get (pre-validated)
        :param chapter: chapter number to get (pre-validated)
        :return: dict of the chapter in the format {"book": bookname, "chapter": chapter_number, "verses":
            {'none': ["1 ...", "2 ..."]}}
        """
        tag_remover = re.compile(r'<.*?>')
        passage: dict = {"book": book, "chapter": chapter, "verses": {'none': []}}
        try:
            response = get(f"{self.__API_URL}{book} {chapter}&type=json")
            response.raise_for_status()
            response = response.json()
            tmp_verses: List[str] = []
            for verse in response:
                tmp_verses.append(verse['verse'] + " " + tag_remover.sub('', verse['text']))
            passage['verses']['none'] = tmp_verses
            self.__cache[book][str(chapter)] = tmp_verses
        except KeyError:
            return {"API Overloaded": "If this keeps happening, the app could be heavily throttled"}
        except HTTPError:
            return {"Issue connecting to the NET API":
                     "Try checking the status of the NET API and the server's network connection"}

        # Save for every even chapter query
        if chapter % 2 == 0:
            try:
                # Normal save
                with open("bibles/json_bibles/net.json", "w") as bible_save:
                    json.dump(self.__cache, bible_save)
            except FileNotFoundError:
                # Testing save
                with open("../bibles/json_bibles/net.json", "w") as bible_save:
                    json.dump(self.__cache, bible_save)

        if not passage:
            raise PassageNotFound(f"{book} {chapter}")
