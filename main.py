#!/usr/bin/env python

from requests import get


class Passage:
    def __init__(self, key: str):
        """
        :param key: API key for requests
        """
        self.__API_KEY = key
        self.__API_URL: str = 'https://api.esv.org/v3/passage/text/'

    def get_passage_esv(self, passage: str):
        params = {
            'q': passage,
            'include-headings': False,
            'include-footnotes': False,
            'include-verse-numbers': False,
            'include-short-copyright': False,
            'include-passage-references': False
        }

        headers = {
            'Authorization': 'Token %s' % self.__API_KEY
        }

        response = get(self.__API_URL, params=params, headers=headers)

        passages = response.json()['passages']

        return passages[0].strip() if passages else 'Error: Passage not found'


if __name__ == '__main__':
    passage = Passage(open("api-key.txt", "r").read())
    print(passage.get_passage_esv("John 11:35"))
