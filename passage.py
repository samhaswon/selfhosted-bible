#!/usr/bin/env python

from requests import get
from typing import List
from re import split as resplit
from re import sub


class PassageNotFound(Exception):
    """
    Exception to be thrown whenever a query results in a passage not being found
    """
    def __init__(self, verse: str):
        super().__init__(str)
        self.__verse = verse

    def __str__(self):
        return "PassageNotFound {}".format(self.__verse)


class Passage:
    """
    Gets a passage of scripture from the ESV API
    """
    def __init__(self, key: str):
        """
        :param key: API key for requests
        """
        self.__API_KEY = key
        self.__API_URL: str = 'https://api.esv.org/v3/passage/text/'

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

        loc_footnotes = str(response['passages']).find('Footnotes')
        footnotes = self.parse_footnotes(str(response['passages'])[loc_footnotes:-2]) if loc_footnotes is not -1 else ""

        passage = response['canonical'], self.parse_headings(''.join(str(x) for x in response['passages'])), footnotes

        if passage:
            return passage
        else:
            raise PassageNotFound

    def get_chapter_esv_json(self, chapter_in: str):
        # Format: {book: "", chapter: 0, verses: [], footnotes: ""}
        chapter_pre = self.get_chapter_esv(chapter_in)
        return {"book": chapter_pre[0:chapter_pre[0].rfind(' ')],
                "chapter": chapter_pre[chapter_pre[0].rfind(' ') + 1:],
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
            if line[0:1].isspace() and is_not_end:
                if heading in parsed.keys():
                    parsed[heading] = parsed[heading] + line + '\n'
                else:
                    parsed.update({heading: line + '\n'})
            elif len(line):
                heading = line

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
