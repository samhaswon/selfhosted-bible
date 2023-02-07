#!/usr/bin/env python
from requests import get
from typing import List


class PassageNotFound(Exception):
    def __init__(self, verse: str):
        super().__init__(str)
        self.__verse = verse

    def __str__(self):
        return "VerseNotFound {}".format(self.__verse)


class Passage:
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

        headers = {
            'Authorization': 'Token %s' % self.__API_KEY
        }

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
