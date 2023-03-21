from bibles.passage import PassageInvalid, PassageNotFound
from bibles.book import Book
from typing import List
from bibles.bible import Bible
from datetime import timedelta
from requests import get
import requests_cache
from re import split as resplit
from re import sub, search


class ESV(Bible):
    def __init__(self, key_in=(False, "")):
        """
        Gets a JSON formatted dictionary of an ESV passage
        :param key_in: (True, "API key"), with the default (False, "") being reading from the file api-key.txt
        """
        super().__init__()
        # API Setup
        self.__API_KEY = open("esv-api-key.txt", "r").read() if not key_in[0] else key_in[1]
        self.__API_URL: str = 'https://api.esv.org/v3/passage/text/'
        # Caching
        requests_cache.install_cache('verses', expire_after=timedelta(days=777), stale_if_error=True)

    def get_passage(self, book: str, chapter: int):
        """
        Gets a book of the ESV
        :param book: Name of the book to get from
        :param chapter: chapter to get
        :return: dictionary of the chapter
        :raises: PassageInvalid for invalid passages
        """
        if super().has_passage(book, chapter):
            return self.__get_chapter_esv_json(book + " " + str(chapter))
        else:
            raise PassageInvalid(book + " " + str(chapter))

    def __get_chapter_esv(self, chapter_in) -> tuple:
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
            footnotes = self.__parse_footnotes(str(response['passages'])[loc_footnotes:-2]) if \
                loc_footnotes != -1 else ""

            passage = response['canonical'], self.__parse_headings(
                ''.join(str(x) for x in response['passages'])), footnotes

        except KeyError:
            return "API Overloaded", \
                   {"try again later": "If this keeps happening, the app could be heavily throttled"}, ""

        if passage:
            return passage
        else:
            raise PassageNotFound

    def __get_chapter_esv_json(self, chapter_in: str):
        """
        Returns a dictionary (Format: {book: "", chapter: 0, verses: {'heading': ["1 content..."]}, footnotes: ""})
        for JSON-ish usage for MongoDB or a similar database
        :param chapter_in: The chapter to get from the API
        :return: Dictionary of the chapter
        """
        # Check for 1 chapter books which the API returns (by name with 1) as only the first verse.
        single_chapter_check = chapter_in[0:chapter_in.rfind(' ')]
        if single_chapter_check in ["Obadiah", "Philemon", "2 John", "3 John", "Jude"]:
            if single_chapter_check == "Obadiah":
                chapter_pre = self.__get_chapter_esv("Obadiah 1-21")
                return {"book": "Obadiah",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "Philemon":
                chapter_pre = self.__get_chapter_esv("Philemon 1-25")
                return {"book": "Philemon",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "2 John":
                chapter_pre = self.__get_chapter_esv("2 John 1-13")
                return {"book": "2 John",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "3 John":
                chapter_pre = self.__get_chapter_esv("3 John 1-15")
                return {"book": "3 John",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "Jude":
                chapter_pre = self.__get_chapter_esv("Jude 1-25")
                return {"book": "Jude",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
        chapter_pre = self.__get_chapter_esv(chapter_in)
        return {"book": chapter_pre[0][0:chapter_pre[0].rfind(' ')],
                "chapter": chapter_pre[0][chapter_pre[0].rfind(' ') + 1:],
                "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in chapter_pre[1].keys()},
                "footnotes": chapter_pre[2]}

    @staticmethod
    def __parse_headings(passage: str) -> dict:
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
            if search(r"^\s{4}[A-Z][a-zA-Z’\s]+\n\n$", line):
                heading = sub(r"^\s+", "", sub(r"\s+$", "", line))
            elif line[0:1].isspace() and is_not_end:
                if heading in parsed.keys():
                    parsed[heading] = parsed[heading] + line + '\n'
                else:
                    parsed.update({heading: line + '\n'})
            elif len(line) and is_not_end:
                heading = sub(r"^\s+", "", sub(r"\s+$", "", line))

        return parsed

    @staticmethod
    def __parse_footnotes(passage: str) -> str:
        """
        Parses footnotes from a text based on leading parenthesis
        :param passage: raw API passage output of footnotes
        :return: parsed footnotes
        """
        return passage[passage.find('('):].replace("\\n\\n", "\n").replace("\\n", "\n")

    @staticmethod
    def __split_verses(verses_in: str) -> List[str]:
        pre = resplit(r'\[', sub(']', "", verses_in))
        return list(filter(None, [sub(r"\s+$", "", verse) for verse in pre]))
