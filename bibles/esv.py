# from passage import Passage, PassageInvalid
from cache_access import CacheAccess
from bibles.book import Book
from typing import List
from bibles.bible import Bible
# For Passage
from datetime import timedelta
from requests import get
import requests_cache
from re import split as resplit
from re import sub, search


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


class PassageNotFound(Exception):
    """
    Exception to be thrown whenever a query results in a passage not being found
    """

    def __init__(self, verse: str):
        super().__init__(str)
        self.__verse = verse

    def __str__(self):
        return "Passage not found {}".format(self.__verse)


class PassageInvalid(Exception):
    """
    Exception to be thrown whenever a query results in a passage not being found
    """

    def __init__(self, verse: str):
        super().__init__(str)
        self.__verse = verse

    def __str__(self):
        return "Passage Invalid {}".format(self.__verse)


class Passage(object):
    """
    Gets a passage of scripture from the ESV API
    """

    def __init__(self, key: str):
        """
        :param key: API key for requests
        """
        self.__API_KEY = key
        self.__API_URL: str = 'https://api.esv.org/v3/passage/text/'
        # Caching
        requests_cache.install_cache('verses', expire_after=timedelta(days=777), stale_if_error=True)

    def __get_passage_esv(self, passage_name: str) -> str:
        """
        Gets individual passages given an identifier
        :param passage_name:
        :return: passage text
        """
        params = {
            'q': passage_name,
            'include-headings': False,
            'include-footnotes': False,
            'include-verse-numbers': True,
            'include-short-copyright': False,
            'include-passage-references': False
        }

        headers = {'Authorization': 'Token %s' % self.__API_KEY}

        response = get(self.__API_URL, params=params, headers=headers)

        passages = response.json()['passages']

        if passages:
            return passages[0].strip()
        else:
            raise PassageNotFound(passage_name)

    def get_passage_esv(self, passage_name: str) -> List[str]:
        """
        Gets a given passage from the API
        :param passage_name: Examples of valid queries include "John 1:1", "jn11.35", "Genesis 1-3", "43011035",
                "John1.1;Genesis1.1", "19001001-19001006,19003001-19003008"
                (from https://api.esv.org/docs/passage-text/)
        :return: List of passage(s) from api.esv.org
        """
        passage_number = passage_name.count(';')
        if passage_number:
            return [self.__get_passage_esv(x) for x in passage_name.split(';')]
        else:
            return [self.__get_passage_esv(passage_name)]

    def get_chapter_esv(self, chapter_in) -> tuple:
        """
        Gets a full chapter of the ESV
        :param chapter_in: Chapter to be queried
        :return: The chapter
        """
        params = {
            'q': chapter_in,
            'include-headings': True,
            'include-footnotes': True,
            'include-footnote-body': True,
            'include-verse-numbers': True,
            'include-short-copyright': False,
            'include-passage-references': False
        }

        headers = {'Authorization': 'Token %s' % self.__API_KEY}

        response = get(self.__API_URL, params=params, headers=headers).json()

        try:
            loc_footnotes = str(response['passages']).find('Footnotes')
            footnotes = self.parse_footnotes(str(response['passages'])[loc_footnotes:-2]) if loc_footnotes != -1 else ""

            passage = response['canonical'], self.parse_headings(
                ''.join(str(x) for x in response['passages'])), footnotes

        except KeyError:
            return "API Overloaded", \
                   {"try again later": "If this keeps happening, the app could be heavily throttled or your key is "
                                       "invalid"}, " "

        if passage:
            return passage
        else:
            raise PassageNotFound

    def get_chapter_esv_json(self, chapter_in: str):
        """
        Returns a dictionary (Format: {book: "", chapter: 0, verses: ["1 content..."], footnotes: ""}) for JSON-ish
        usage for MongoDB or a similar database
        :param chapter_in: The chapter to get from the API
        :return: Dictionary of the chapter
        """
        # Check for 1 chapter books which the API returns (by name with 1) as only the first verse.
        single_chapter_check = chapter_in[0:chapter_in.rfind(' ')]
        if single_chapter_check in ["Obadiah", "Philemon", "2 John", "3 John", "Jude"]:
            if single_chapter_check == "Obadiah":
                chapter_pre = self.get_chapter_esv("Obadiah 1-21")
                return {"book": "Obadiah",
                        "chapter": "1",
                        "verses": {heading: self.split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "Philemon":
                chapter_pre = self.get_chapter_esv("Philemon 1-25")
                return {"book": "Philemon",
                        "chapter": "1",
                        "verses": {heading: self.split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "2 John":
                chapter_pre = self.get_chapter_esv("2 John 1-13")
                return {"book": "2 John",
                        "chapter": "1",
                        "verses": {heading: self.split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "3 John":
                chapter_pre = self.get_chapter_esv("3 John 1-15")
                return {"book": "3 John",
                        "chapter": "1",
                        "verses": {heading: self.split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "Jude":
                chapter_pre = self.get_chapter_esv("Jude 1-25")
                return {"book": "Jude",
                        "chapter": "1",
                        "verses": {heading: self.split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
        chapter_pre = self.get_chapter_esv(chapter_in)
        return {"book": chapter_pre[0][0:chapter_pre[0].rfind(' ')],
                "chapter": chapter_pre[0][chapter_pre[0].rfind(' ') + 1:],
                "verses": {heading: self.split_verses(chapter_pre[1][heading]) for heading in chapter_pre[1].keys()},
                "footnotes": chapter_pre[2]}

    @staticmethod
    def parse_headings(passage: str) -> dict:
        """
        Parses headings from a text based on leading spaces
        :param passage: raw API passage output of a chapter
        :return: parsed passage. Inserts "none" for sections without a heading
        """
        parsed: dict = {}
        heading = "none"
        for line in passage.splitlines():
            is_not_end: bool = False
            for char in line:
                if char.isalnum():
                    is_not_end = True
                    break
            # Add lines
            if search(r"^\s{4}[A-Z][a-zA-Z’\s]+$", line):
                heading = sub(r"^\s+", "", sub(r"\s+$", "", line))
            elif line[0:1].isspace() and is_not_end:
                if heading in parsed.keys():
                    parsed[heading] = parsed[heading] + line + '\n'
                else:
                    parsed.update({heading: line + '\n'})
            elif len(line):
                heading = sub(r"^\s+", "", sub(r"\s+$", "", line))

        return parsed

    @staticmethod
    def parse_footnotes(passage: str) -> str:
        """
        Parses footnotes from a text based on leading parenthesis
        :param passage: raw API passage output of footnotes
        :return: parsed footnotes
        """
        return passage[passage.find('('):].replace("\\n\\n", "\n").replace("\\n", "\n")

    def split_verses(self, verses_in: str) -> List[str]:
        pre = resplit('\[', sub(']', "", verses_in))
        return list(filter(None, [sub(r"\s+$", "", verse) for verse in pre]))
