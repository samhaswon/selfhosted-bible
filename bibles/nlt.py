from bibles.passage import PassageInvalid, PassageNotFound
from typing import List
from bibles.bible import Bible
from bibles.bolls_translate import translate
import requests
import json
import re

class NLT(Bible):
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an NLT passage
        """
        super().__init__()

        # Caching
        try:
            with open('bibles/json_bibles/nlt.json', 'r') as cache_in:
                self.__cache: dict = json.load(cache_in)
        except FileNotFoundError:
            # Initialize empty cache
            self.__cache: dict = {book.name: {str(chapter): [] for chapter in range(1, book.chapter_count + 1)} for
                                  book in super().books}

        self.__API_URL: str = "https://bolls.life/get-chapter/NLT/"

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Gets a chapter of the NLT
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

    def __api_return(self, book: str, chapter: int) -> None:
        """
        Gets a passage from the API
        :param book: Name of the book to get (pre-validated)
        :param chapter: chapter number to get (pre-validated)
        :return: None
        """
        tag_remover: re.Pattern = re.compile(r'<.*?>')
        try:
            response = requests.get(f"{self.__API_URL}{translate(book)}/{chapter}/")
            response.raise_for_status()
            response = response.json()
            tmp_verses: List[str] = []
            for verse in response:
                tmp_verses.append(str(verse['verse']) + " " + tag_remover.sub('', verse['text']))
            self.__cache[book][str(chapter)] = tmp_verses
        except KeyError:
            raise PassageInvalid(book + " " + str(chapter))
        except requests.HTTPError:
            raise PassageNotFound(book + " " + str(chapter))

        # Save for every even chapter query
        if chapter % 2 == 0:
            try:
                # Normal save
                with open("bibles/json_bibles/nlt.json", "w") as bible_save:
                    json.dump(self.__cache, bible_save)
            except FileNotFoundError:
                # Testing save
                with open("../bibles/json_bibles/nlt.json", "w") as bible_save:
                    json.dump(self.__cache, bible_save)
