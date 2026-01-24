"""
NIV (1984)
"""
import re
from typing import List
from bs4 import BeautifulSoup
import requests
from bibles.passage import PassageInvalid, PassageNotFound
from bibles.bible import Bible
from bibles.compresscache import CompressCache


class NIV1984(Bible):
    """NIV (1984)"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of a NIV (1984) passage
        """
        super().__init__()
        self.__compress_cache = CompressCache('niv1984')

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

        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) '
                          'Gecko/20100101 Firefox/112.0',
            'Accept': 'application/xml, text/xml, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Gets a chapter of the NIV (1984)
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
        raise PassageInvalid(book + " " + str(chapter))

    def __api_return(self, book: str, chapter: int) -> None:
        """
        Gets a passage from the API
        :param book: Name of the book to get (pre-validated)
        :param chapter: chapter number to get (pre-validated)
        :return: None
        """
        try:
            book_url_name = f"{re.sub(r' ', '-', book.lower())}"
            content_url = (
                f"https://www.studylight.org/bible/eng/n84/"
                f"{book_url_name}/{chapter}.html"
            )
            html_content = requests.get(
                content_url,
                headers=self.__headers,
                timeout=20
            ).text
            verses = self.__parse(html_content)
            self.__cache[book][str(chapter)] = verses
        except KeyError as exc:
            raise PassageInvalid(book + " " + str(chapter)) from exc
        except requests.HTTPError as exc:
            raise PassageNotFound(book + " " + str(chapter)) from exc

        # Save for every even chapter query
        if chapter % 2 == 0:
            self.__compress_cache.save(self.__cache)

    @staticmethod
    def __parse(content: str) -> List[str]:
        # Parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')

        body = soup.body
        body_div = [x for x in body.find_all("div") if len(x.attrs) == 0][0]

        spans = body_div.find_all("span")

        verses = []
        for span in spans:
            span_text = span.text
            if len(span_text) > 1000:
                continue
            if len(verses) > 0 and verses[-1][:3] == span_text[:3]:
                continue
            verses.append(span_text)

        verses = [
            re.sub(
                r"\s\s+| ",
                " ",
                re.sub(
                    r"\(F\d+\)|\s$",
                    "",
                    text
                )
            ) for text in verses
        ]
        return verses
