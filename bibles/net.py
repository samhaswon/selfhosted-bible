"""
NET Bible
"""
import re
from typing import List, Optional
from requests import get, HTTPError
from bibles.api_bible import APIBible


# pylint: disable=too-few-public-methods
class NET(APIBible):
    """NET Bible"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an NET passage
        """
        super().__init__(cache_name="net")

        self.__api_url: str = "http://labs.bible.org/api/?passage="
        self.__tag_remover: re.Pattern = re.compile(r'<.*?>')

    # pylint: disable=inconsistent-return-statements
    def api_return(self, book: str, chapter: int) -> Optional[dict]:
        """
        Gets a passage from the API
        :param book: Name of the book to get (pre-validated)
        :param chapter: chapter number to get (pre-validated)
        :return: None
        """
        try:
            response = get(
                f"{self.__api_url}{book} {chapter}&type=json", timeout=20
            )
            response.raise_for_status()
            response = response.json()
            tmp_verses: List[str] = []
            for verse in response:
                tmp_verses.append(
                    verse['verse'] + " " + self.__tag_remover.sub('', verse['text'])
                )
            self.cache[book][str(chapter)] = tmp_verses
        except KeyError:
            return {
                "API Overloaded?": "If this keeps happening, the app could be heavily throttled"
            }
        except HTTPError:
            return {
                "Issue connecting to the NET API":
                "Try checking the status of the NET API and the server's network connection"
            }

        # Save for every even chapter query
        if chapter % 2 == 0:
            self.compress_cache.save(self.cache)
        return None
