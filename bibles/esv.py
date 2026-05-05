"""
Class for the ESV
"""
from re import split as resplit
from re import sub, search, match
from typing import List

from bs4 import BeautifulSoup, Tag, NavigableString
from requests import get, HTTPError

# pylint: disable=import-error
from bibles.api_bible import APIBible
from bibles.passage import PassageNotFound


class ESV(APIBible):
    """
    Class for the ESV
    """
    def __init__(self, key_in="", debug=False) -> None:
        """
        Gets a JSON formatted dictionary of an ESV passage
        :param key_in: (True, "API key"),
        with the default (False, "") being reading from the file api-key.txt
        """
        super().__init__(cache_name="esv")
        self.__debug = debug
        # API Setup
        try:
            if len(key_in) < 0:
                with open("esv-api-key.txt", "r", encoding="utf-8") as key_file:
                    self.__api_key = key_file.read()
            else:
                self.__api_key = key_in
        except FileNotFoundError:
            self.__api_key = ""
        self.__api_url: str = 'https://api.esv.org/v3/passage/text/'

    def __get_chapter_esv(self, chapter_in) -> tuple:
        """
        Gets a full chapter of the ESV.
        :param chapter_in: Chapter to be queried.
        :return: The chapter.
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

        headers: dict = {'Authorization': f"Token {self.__api_key}"}

        try:
            response: dict = get(
                self.__api_url,
                params=params,
                headers=headers,
                timeout=30
            ).json()
            loc_footnotes: int = str(response['passages']).find('Footnotes')
            footnotes: str = (
                self.__parse_footnotes(str(response['passages'])[loc_footnotes:-2])) if \
                loc_footnotes != -1 else ""

            passage: tuple = response['canonical'], self.__parse_headings(
                ''.join(str(x) for x in response['passages'])), footnotes

        except KeyError:
            return "API Overloaded", \
                   {"try again later":
                        "If this keeps happening, "
                        "the app could be heavily throttled"
                    }, ""
        except HTTPError:
            return "API down?", \
                {"Issue connecting to the ESV API":
                     "Try checking the status of the ESV API and "
                     "the server's network connection"}, ""

        if passage:
            return passage
        raise PassageNotFound

    def __get_chapter_esv_json(self, chapter_in: str) -> dict:
        """
        Returns a dictionary
        (Format:
        {
            book: "",
            chapter: 0,
            verses: {
                'heading':
                    ["1 content..."],
                footnotes: ""
            }
        })
        for JSON-ish usage for MongoDB or a similar database.
        :param chapter_in: The chapter to get from the API.
        :return: Dictionary of the chapter.
        """
        # Check for 1 chapter books which the API returns (by name with 1) as only the first verse.
        single_chapter_check: str = chapter_in[0:chapter_in.rfind(' ')]

        if single_chapter_check in ["Obadiah", "Philemon", "2 John", "3 John", "Jude"]:
            # pylint: disable=consider-iterating-dictionary
            if single_chapter_check == "Obadiah":
                chapter_pre = self.__get_chapter_esv("Obadiah 1-21")
                return {"book": "Obadiah",
                        "chapter": "1",
                        "verses": {
                            heading: self.__split_verses(chapter_pre[1][heading])
                            for heading in chapter_pre[1].keys()
                        },
                        "footnotes": chapter_pre[2]}
            if single_chapter_check == "Philemon":
                chapter_pre = self.__get_chapter_esv("Philemon 1-25")
                return {"book": "Philemon",
                        "chapter": "1",
                        "verses": {
                            heading: self.__split_verses(chapter_pre[1][heading])
                            for heading in chapter_pre[1].keys()
                        },
                        "footnotes": chapter_pre[2]}
            if single_chapter_check == "2 John":
                chapter_pre = self.__get_chapter_esv("2 John 1-13")
                return {"book": "2 John",
                        "chapter": "1",
                        "verses": {
                            heading: self.__split_verses(chapter_pre[1][heading])
                            for heading in chapter_pre[1].keys()
                        },
                        "footnotes": chapter_pre[2]}
            if single_chapter_check == "3 John":
                chapter_pre = self.__get_chapter_esv("3 John 1-15")
                return {"book": "3 John",
                        "chapter": "1",
                        "verses": {
                            heading: self.__split_verses(chapter_pre[1][heading])
                            for heading in chapter_pre[1].keys()
                        },
                        "footnotes": chapter_pre[2]}
            if single_chapter_check == "Jude":
                chapter_pre = self.__get_chapter_esv("Jude 1-25")
                return {"book": "Jude",
                        "chapter": "1",
                        "verses": {
                            heading: self.__split_verses(chapter_pre[1][heading])
                            for heading in chapter_pre[1].keys()
                        },
                        "footnotes": chapter_pre[2]}

        chapter_pre = self.__get_chapter_esv(chapter_in)
        # pylint: disable=consider-iterating-dictionary
        return {"book": chapter_pre[0][0:chapter_pre[0].rfind(' ')],
                "chapter": chapter_pre[0][chapter_pre[0].rfind(' ') + 1:],
                "verses": {
                    heading: self.__split_verses(chapter_pre[1][heading])
                    for heading in chapter_pre[1].keys()
                },
                "footnotes": chapter_pre[2]}

    @staticmethod
    def __parse_headings(passage: str) -> dict:
        """
        Parses headings from a text based on leading spaces.
        :param passage: The raw API passage output of a chapter.
        :return: A parsed passage. Inserts "none" for sections without a heading.
        """
        parsed: dict = {}
        heading: str = "none"
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
                # pylint: disable=consider-iterating-dictionary
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
        Parses footnotes from a text based on leading parenthesis.
        :param passage: The raw API passage output of footnotes.
        :return: Parsed footnotes.
        """
        return passage[passage.find('('):].replace("\\n\\n", "\n").replace("\\n", "\n")

    @staticmethod
    def __split_verses(verses_in: str) -> List[str]:
        """
        Splits a given string of verses by the "[]" parts of the verse marker.
        :param verses_in: string of combined verses.
        :return: A list of verses as one entry per verse.
        """
        pre = resplit(r'\[', sub(']', "", verses_in))
        return list(filter(None, [sub(r"\s+$", "", verse) for verse in pre]))

    # pylint: disable=too-many-branches
    def api_return(self, book: str, chapter: int) -> dict:
        """
        Gets the given verse from the API,
        and clears the cache in accordance with the ESV API caching limits.
        :param book: Book to retrieve from.
        :param chapter: The chapter of that book.
        :return: A dictionary formatted by book, chapter, verses, and footnotes.
        """
        if len(self.__api_key):
            passage = self.__get_chapter_esv_json(book + " " + str(chapter))
        else:
            self.__non_api_fetch(book=book, chapter=str(chapter))
            passage = self.get_passage(book, chapter)

        # This is to be able to evaluate more results at once.
        if self.__debug:
            return passage

        # Make sure the cache is within guidelines
        verse_count = 0
        for book_iter in self.cache.keys():
            for chapter_iter in self.cache[book_iter].keys():
                try:
                    for heading in self.cache[book_iter][chapter_iter]['verses'].keys():
                        verse_count += len(self.cache[book_iter][chapter_iter]['verses'][heading])
                except (KeyError, TypeError):
                    # Empty entry or unpopulated cache
                    pass

        # If the cache is outside the guidelines,
        # then remove passages until it is.
        # This also has the side benefit of keeping the cache small.
        if verse_count + len(passage['verses']) >= 500:
            verse_count_to_remove: int = verse_count + len(passage['verses']) - 500
            for book_iter in self.cache.keys():
                for chapter_iter in self.cache[book_iter].keys():
                    # Clear the entry iff it has data
                    try:
                        if size := len(self.cache[book_iter][chapter_iter]['verses']):
                            self.cache[book_iter][chapter_iter] = {}
                            verse_count_to_remove -= size
                    except (KeyError, TypeError):
                        # Empty entry or unpopulated cache
                        pass
                    # Break whenever enough has been cleared
                    if verse_count_to_remove <= 0:
                        break

            # Cache the passage and save
            self.cache[book][str(chapter)] = {
                'verses': passage['verses'],
                'footnotes': passage['footnotes']
            }
            self.compress_cache.save(self.cache)
        else:
            self.cache[book][str(chapter)] = {
                'verses': passage['verses'],
                'footnotes': passage['footnotes']
            }
        if chapter % 2 == 0:
            self.compress_cache.save(self.cache)
        return passage

    def __non_api_fetch(self, book: str, chapter: str) -> None:
        """
        Retrieves a passage when an API key is not supplied.
        :param book: Book to fetch.
        :param chapter: Chapter of the book
        :return: None
        """
        try:
            uri = "https://www.esv.org/"
            # Hey website! I'm a browser!
            headers = {
                "Accept":
                    "text/html,application/xhtml+xml,application/xml;"
                    "q=0.9,image/avif,image/webp,image/apng,"
                    "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Cookie": "csrftoken=iiNDT02hk6nnMyowYaLhOcxcegIUtydb",
                "DNT": "1",
                "Host": "www.esv.org",
                "Pragma": "no-cache",
                "Referer": "https://www.esv.org/",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36",
                "sec-ch-ua": '"Chromium";v="131", "Not(A:Brand";v="24", "Google Chrome";v="131"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"'
            }

            response = get(
                f"{uri}{book if book != 'Psalms' else 'Psalm'}+{chapter}",
                headers=headers,
                timeout=30
            )
        except HTTPError as ex:
            raise PassageNotFound(str(ex)) from ex
        result = self.parse(response.content.decode('utf-8'))
        # pylint: disable=consider-using-dict-items,consider-iterating-dictionary
        for book_ref in result.keys():
            for chapter_ref in result[book_ref].keys():
                if book_ref == 'Psalm':
                    self.cache['Psalms'][str(chapter_ref)]['verses'] = \
                        result[book_ref][chapter_ref]
                elif book_ref == 'Obadia':
                    self.cache['Obadiah']['1']['verses'] = result['Obadia']['Obadiah']
                elif book_ref == 'Philemo':
                    self.cache['Philemon']['1']['verses'] = result['Philemo']['Philemon']
                elif book_ref == '2':
                    self.cache['2 John']['1']['verses'] = result['2']['John']
                elif book_ref == '3':
                    self.cache['3 John']['1']['verses'] = result['3']['John']
                elif book_ref == 'Jud':
                    self.cache['Jude']['1']['verses'] = result['Jud']['Jude']
                else:
                    self.cache[book_ref][str(chapter_ref)]['verses'] = \
                        result[book_ref][chapter_ref]
        if int(chapter) % 2 == 0:
            self.compress_cache.save(self.cache)


    # pylint: disable=too-many-locals,too-many-statements
    @classmethod
    def parse(cls, content: str) -> dict:
        """
        Pareses the HTML into the desired format.
        :param content: HTML, converted to a string.
        :return: Dict of the same format as the memory cache.
        """
        # Get ready to parse
        soup = BeautifulSoup(content, 'html.parser')
        del content
        results = {}

        # Drill down to where the verses are
        body = soup.body.div.main.article
        body = [x for x in body if x.name == 'div'][0]
        body = [
            x for x in body.contents[1].contents
            if isinstance(x, Tag) and x.name == 'section'
        ]
        del soup

        # Go through each chapter
        # pylint: disable=too-many-nested-blocks
        for chapter in body:
            reference = chapter.attrs['data-reference']
            book = reference[:reference.rfind(" ")]
            chapter_ref = reference[reference.rfind(" ") + 1:]
            counter = 0     # For Song of Solomon

            if book not in results:
                results[book] = {}
            if chapter_ref not in results[book]:
                results[book][chapter_ref] = {}

            spans = [x for x in chapter.contents if isinstance(x, Tag)]
            current_heading = 'none'
            for child in spans:
                if child.name == 'h3':
                    current_heading = child.text
                    continue
                if child.name == 'h4':
                    if current_heading != 'none' and book != "Song of Solomon":
                        current_heading += "\n" + child.text
                    elif 'speaker' in child.attrs['class']:
                        if current_heading not in results[book][chapter_ref]:
                            results[book][chapter_ref][current_heading] = [""]
                        current_heading = child.text + " " * counter
                        counter += 1
                    continue
                verse = ""
                for elements in child:
                    if isinstance(elements, NavigableString):
                        continue
                    for verse_words in elements.contents:
                        if isinstance(verse_words, NavigableString):
                            continue
                        if (verse_words.name == 'span' and
                                'small-caps' in verse_words.attrs['class']):
                            verse += 'Lord'
                        if verse_words.name == 'span':
                            for words in verse_words.contents:
                                if (words.name == 'span' and
                                        'small-caps' in words.attrs['class']):
                                    verse += 'Lord'
                                if words.name == 'b':
                                    if len(verse) > 0:
                                        if current_heading not in results[book][chapter_ref]:
                                            results[book][chapter_ref][current_heading] = []
                                        results[book][chapter_ref][current_heading].append(verse)
                                        verse = ""
                                    if 'verse-num' in words.attrs['class']:
                                        verse += words.text
                                    else:
                                        verse += "1 "
                                elif words.name == 'u' and len(verse) == 0:
                                    if current_heading in results[book][chapter_ref]:
                                        results[
                                            book][chapter_ref][current_heading][-1
                                        ] += words.text
                                    else:
                                        verse = words.text
                                elif words.name == 'u':
                                    if not (verse[-1] == ' ' or
                                            verse[-1] == " " or verse[-1] == "“") and \
                                            not match(r'[  ,;.!?“”]', words.text):
                                        verse += " "
                                    verse += words.text
                        if verse_words.name == 'b':
                            if len(verse) > 0:
                                if current_heading not in results[book][chapter_ref]:
                                    results[book][chapter_ref][current_heading] = []
                                results[book][chapter_ref][current_heading].append(verse)
                                verse = ""
                            if 'verse-num' in verse_words.attrs['class']:
                                verse += verse_words.text
                            else:
                                verse += "1 "
                        elif verse_words.name == 'u' and len(verse) == 0:
                            if current_heading in results[book][chapter_ref]:
                                results[book][chapter_ref][current_heading][-1] += verse_words.text
                            else:
                                verse = verse_words.text
                        elif verse_words.name == 'u':
                            verse += verse_words.text
                if current_heading not in results[book][chapter_ref] and len(verse) > 0:
                    results[book][chapter_ref][current_heading] = []
                if len(verse) > 0:
                    results[book][chapter_ref][current_heading].append(verse)
        return results
