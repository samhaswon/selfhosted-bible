from bibles.passage import PassageInvalid, PassageNotFound
from typing import Dict
from bibles.bible import Bible
from requests import get, HTTPError
import requests_cache   # TODO: Remove
import json
import re
import time # TODO: Remove


class CSB(Bible):
    def __init__(self):
        super().__init__()
        requests_cache.install_cache('verses', expire_after=999999999**99)  # TODO: Remove

        # Used to work with the "API" while validating input
        self.__file_aliases: Dict[str, str] = {
            'Genesis': '01-Gen.xml',
            'Exodus': '02-Ex.xml',
            'Leviticus': '03-Lev.xml',
            'Numbers': '04-Num.xml',
            'Deuteronomy': '05-Deut.xml',
            'Joshua': '06-Josh.xml',
            'Judges': '07-Jdg.xml',
            'Ruth': '08-Ruth.xml',
            '1 Samuel': '09-1Sam.xml',
            '2 Samuel': '10-2Sam.xml',
            '1 Kings': '11-1Ki.xml',
            '2 Kings': '12-2Ki.xml',
            '1 Chronicles': '13-1Chr.xml',
            '2 Chronicles': '14-2Chr.xml',
            'Ezra': '15-Ezra.xml',
            'Nehemiah': '16-Neh.xml',
            'Esther': '17-Esth.xml',
            'Job': '18-Job.xml',
            'Psalms': '19-Ps.xml',
            'Proverbs': '20-Prov.xml',
            'Ecclesiastes': '21-Eccl.xml',
            'Song of Solomon': '22-Song.xml',
            'Isaiah': '23-Isa.xml',
            'Jeremiah': '24-Jer.xml',
            'Lamentations': '25-Lam.xml',
            'Ezekiel': '26-Ezek.xml',
            'Daniel': '27-Dan.xml',
            'Hosea': '28-Hos.xml',
            'Joel': '29-Joel.xml',
            'Amos': '30-Amos.xml',
            'Obadiah': '31-Ob.xml',
            'Jonah': '32-Jonah.xml',
            'Micah': '33-Mic.xml',
            'Nahum': '34-Nah.xml',
            'Habakkuk': '35-Hab.xml',
            'Zephaniah': '36-Zeph.xml',
            'Haggai': '37-Hag.xml',
            'Zechariah': '38-Zech.xml',
            'Malachi': '39-Mal.xml',
            'Matthew': '40-Matt.xml',
            'Mark': '41-Mark.xml',
            'Luke': '42-Luke.xml',
            'John': '43-John.xml',
            'Acts': '44-Acts.xml',
            'Romans': '45-Rom.xml',
            '1 Corinthians': '46-1Cor.xml',
            '2 Corinthians': '47-2Cor.xml',
            'Galatians': '48-Gal.xml',
            'Ephesians': '49-Eph.xml',
            'Philippians': '50-Phil.xml',
            'Colossians': '51-Col.xml',
            '1 Thessalonians': '52-1Thes.xml',
            '2 Thessalonians': '53-2Thes.xml',
            '1 Timothy': '54-1Tim.xml',
            '2 Timothy': '55-2Tim.xml',
            'Titus': '56-Titus.xml',
            'Philemon': '57-Phlm.xml',
            'Hebrews': '58-Heb.xml',
            'James': '59-Jas.xml',
            '1 Peter': '60-1Pet.xml',
            '2 Peter': '61-2Pet.xml',
            '1 John': '62-1John.xml',
            '2 John': '63-2John.xml',
            '3 John': '64-3John.xml',
            'Jude': '65-Jude.xml',
            'Revelation': '66-Rev.xml',
        }
        # Caching
        try:
            with open('bibles/json_bibles/csb.json', 'r') as cache_in:
                self.__cache: dict = json.load(cache_in)
        except FileNotFoundError:
            # Initialize empty cache
            self.__cache: dict = {book.name: {str(chapter): {} for chapter in range(1, book.chapter_count + 1)} for
                                  book in super().books}

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Gets a given passage of the CSB. Note: this is slow as it gets the whole book.
        :param book: Book to get
        :param chapter: Chapter of the book
        :return: dictionary of the passage
        """
        if not super().has_passage(book, chapter):
            raise PassageInvalid(f"{book} {chapter}")
        if not len(self.__cache[book][str(chapter)]):
            self.__get_book(book)
            try:
                with open("bibles/json_bibles/csb.json", "w") as bible_save:
                    json.dump(self.__cache, bible_save)
            # For testing:
            except FileNotFoundError:
                with open("../bibles/json_bibles/csb.json", "w") as bible_save:
                    json.dump(self.__cache, bible_save)
        return {'book': book, 'chapter': chapter, 'verses': self.__cache[book][str(chapter)]['verses']}

    def __get_book(self, book: str) -> None:
        """
        So, I'm not a fan of doing this how I am. The API only has the full books afaik. Their search method gets all
        66, so this was not made to be the most efficient. Though, this does cache it, which is efficient (~175ns access
        times on my dev machine).
        :param book: Book to get, pre validated
        :return: The full book as a dictionary
        """
        try:
            # The pseudo API. This is pretty much just grabbing and parsing XML files.
            uri = "https://read.csbible.com/wp-content/themes/lwcsbread/CSB_XML//"

            # Hey website! I'm a browser!
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
                'Accept': 'application/xml, text/xml, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.5',
                'X-Requested-With': 'XMLHttpRequest',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            }
            passage = self.__file_aliases[book]
            response = get(f"{uri}{passage}", headers=headers, cookies={'credentials': 'include'})
            response.raise_for_status()

            start = time.perf_counter() # TODO: Remove
            self.__parse(response.text)
            end = time.perf_counter()   # TODO: Remove
            print(f"Total time parsing {book}: {end - start}")
        except HTTPError as ex:
            raise PassageNotFound(f"Error getting {book}: {ex.__str__()}")

    def __parse(self, xml_in: str) -> None:
        """
        Splits then parses the given XML into the cache
        :param xml_in: Full XML document in string form
        :return: None
        """
        book_name_position: int = xml_in.find("<bookname>") + 10
        book_name_end: int = xml_in.find("</bookname>")
        book_name: str = xml_in[book_name_position:book_name_end]
        if book_name == "Song of Songs":
            book_name = "Song of Solomon"

        chapter_positions = []
        i, j = book_name_end, 0
        while i < len(xml_in):
            i = xml_in.find("<chapter", i)
            j = xml_in.find("</chapter>", i) + 10
            if i != -1:
                chapter_positions.append((i, j))
                i = j
            else:
                break

        for chapter_start, chapter_end in chapter_positions:
            display_pos = xml_in.find("display=\"", chapter_start) + 9
            chapter_num = xml_in[display_pos:xml_in.find("\"", display_pos)]
            self.__cache[book_name][chapter_num]['verses'] = self.__parse_chapter(xml_in, chapter_start, chapter_end)

    @staticmethod
    def __parse_chapter(xml_in: str, chapter_start: int, chapter_end: int) -> dict:
        """
        Parses the chapter from the given range
        :param xml_in: The full XML document
        :param chapter_start: Start position of the chapter to parse
        :param chapter_end: End position of the chapter to parse
        :return: Parsed chapter in the form {heading: ["1...", "2...",...]}
        """
        # Regex's
        condense = re.compile(r'\s\s+|\n')
        head_tag_regex = re.compile(r'<head1>|</head1>')
        ignore_sup_block_start_regex = re.compile(
            r'^\s*<sup class=\"translate-note|^\s*<sup class=\"cross-ref\">|^\s*<sup class=\"alt-reading-note\"|'
            r'^\s*<sup class=\"help-note\">|^\s*<sup class=\"clarifying-note\">|^\s*<sup class="ot-quote')
        ignoring: bool = False
        ignore_sup_block_end_regex = re.compile(r'\s+</sup>$|</a></sup>$|</sup></verse>$')
        ignore_sup_block_end_content_regex = re.compile(r'\s+</sup>(\s|&)|</a></sup>')
        ignore_tag_regex = re.compile(
            r'<p type="noind">$|^\s*</p>$|<list|</list|\s+</item>$|<poetryblock|(?!</verse>)</poetryblock|\s+</poem>|'
            r'<chapter|</chapter>|<dynprose>|</dynprose>|<blockindent>|</blockindent>|\s+<psalm>|<p>$|'
            r'^\s*<redletter-end/>$|^\s*<otdynprose>$|^\s*</otdynprose>$|^\s*<redletter-start/>$|^\s+<item>$')
        item_end_regex = re.compile(r'</item>')
        fix_lord_regex = re.compile(r'<span.*class=\"smallcaps\">?.*Lord.*</span>')
        lazy_tag_removal_regex = re.compile(
            r'<item>|</p>|</sup>|<redletter-start/>|<redletter-end/>?|</sup|</sub>|</poemright>|</item>|'
            r'<item type="noind">|</poem>|<poem|<.*>|</.*>')
        ot_quote_regex = re.compile(r'<otquote>')
        p_no_ind_regex = re.compile(r'<p type=\"noind\">')
        poem_start_regex = re.compile(r'<poem.*>')
        poem_end_regex = re.compile(r'</poem>')
        poem_right_selah_regex = re.compile(r'<poemright>')
        poem_verse_ref = re.compile(r'<sup class="verse-ref"')
        rare_mixed_verse_ref_regex = re.compile(r'^[\w\s.]+<sup class=\"verse-ref\"')
        rare_p_right_regex = re.compile(r'<p type="right">')
        verse_start_tag_regex = re.compile(r'<verse')
        verse_end_tag_regex = re.compile(r'^\s*</verse')
        verse_content_end_tag_regex = re.compile(r'</verse>')
        verse_inline_ref_regex = re.compile(r'<sup class=\"cross-ref\"|[;:.,a-zA-Z]<sup')
        verse_verse_ref_regex = re.compile(r'</sup>')

        heading: str = "none"
        heading_end_search = False
        verses: dict = {}
        verse: str = ""
        lines = xml_in[chapter_start:chapter_end].splitlines()
        for line in lines:
            if ignoring:
                if ignore_sup_block_end_regex.search(line):
                    ignoring = False
                elif ignore_sup_block_end_content_regex.search(line):
                    ignoring = False
                    verse += line[line.find("</sup>") + 6:]
                continue
            elif ignore_tag_regex.search(line) or line == "":
                continue
            elif ignore_sup_block_start_regex.search(line):
                ignoring = verse_verse_ref_regex.search(line) is None
            elif head_tag_regex.search(line) or heading_end_search:
                if re.search(r"\s+</head1>", line):
                    heading_end_search = False
                elif "</head1>" in line:
                    heading = fix_lord_regex.sub('Lord', line[line.find("<head1>") + 7:line.find("</head1>")])
                    verses[heading] = []
                    heading_end_search = False
                elif "<head1>" in line:
                    heading = fix_lord_regex.sub('Lord', line[line.find("<head1>") + 7:])
                    heading_end_search = True
                else:
                    heading += " " + fix_lord_regex.sub('Lord', condense.sub(' ', line))
            elif rare_mixed_verse_ref_regex.search(line):
                ref_start = line.find("<")
                verse += " " + line[:ref_start]
                verse = condense.sub(' ', lazy_tag_removal_regex.sub(' ', item_end_regex.sub(' ',
                                                                                             fix_lord_regex.sub('Lord',
                                                                                                                verse))))
                if len(verse) <= 4:
                    pass
                elif heading in verses and len(verses[heading]):
                    if verses[heading][-1][0:verses[heading][-1].find(" ")] == verse[0:verse.find(" ")]:
                        verses[heading][-1] += " " + verse[verse.find(" ") + 1:]
                    else:
                        verses[heading].append(verse)
                else:
                    verses[heading] = [verse]
                display_number_pos = line.find(".", line.find(".", ref_start) + 1) + 1
                verse_number: str = line[display_number_pos:line.find("\"", display_number_pos)]
                verse = f"{verse_number} "
                ignoring = "</sup>" not in line and "<sup>" in line
            elif poem_start_regex.search(line):
                if poem_verse_ref.search(line):
                    poem_start_position = line.find("</sup>") + 7
                else:
                    poem_start_position = line.find(">") + 1
                if poem_end_regex.search(line):
                    verse += " " + line[poem_start_position:line.find("</poem>", poem_start_position)]
                elif verse_inline_ref_regex.search(line):
                    verse += " " + line[poem_start_position:line.find("<sup", poem_start_position)]
                    if not line.find("</sup>", poem_start_position) > -1:
                        ignoring = True
                else:
                    verse += " " + line[poem_start_position:]
            elif verse_start_tag_regex.search(line):
                if len(verse):
                    verse = condense.sub(' ', lazy_tag_removal_regex.sub(' ', item_end_regex.sub(' ',
                                                                                                 fix_lord_regex.sub(
                                                                                                     'Lord', verse))))
                if len(verse) <= 1 or heading not in verses or len(verses[heading]) == 0:
                    pass
                elif int(verses[heading][-1][0:verses[heading][-1].find(" ")]) != int(verse[0:verse.find(" ")]) - 1 and \
                        verses[heading][-1] != verse:
                    verses[heading][-1] += " " + verse[verse.find(" ") + 1:]
                if "display-number" in line:
                    display_number_pos = line.find("display-number=\"") + 16
                else:
                    display_number_pos = line.find(".", line.find(".") + 1) + 1
                verse_number: str = line[display_number_pos:line.find("\"", display_number_pos)]
                verse = f"{verse_number} "
                if verse_inline_ref_regex.search(line):
                    verse += line[line.find("</sup>") + 7:line.rfind("<sup")]
                    ignoring = line.rfind("</sup>") - line.find("</sup>") == 0
                elif verse_content_end_tag_regex.search(line):
                    verse += line[line.find("</sup>") + 7:line.find("</verse>")]
                    verse = condense.sub(' ', lazy_tag_removal_regex.sub(' ', item_end_regex.sub(' ', fix_lord_regex.sub('Lord', verse))))
                    if heading in verses and len(verses[heading]):
                        if verses[heading][-1][0:verses[heading][-1].find(" ")] == verse[0:verse.find(" ")]:
                            verses[heading][-1] += " " + verse[verse.find(" ") + 1:]
                        else:
                            verses[heading].append(verse)
                    else:
                        verses[heading] = [verse]
                elif "</sup>" in line and len(line) - line.find("</sup>") - 6:
                    verse += line[line.find("</sup>") + 7:]
                elif "<sup" not in line and len(line) - display_number_pos > 5:
                    verse += " " + line[line.find("\"", display_number_pos) + 2:]
            elif len(verse) > 3 and verse_end_tag_regex.search(line):
                verse = condense.sub(' ', lazy_tag_removal_regex.sub(' ', item_end_regex.sub(' ', fix_lord_regex.sub('Lord', verse))))
                if heading not in verses or len(verses[heading]) == 0:
                    verses[heading] = [verse]
                elif verses[heading][-1][0:verses[heading][-1].find(" ")] == verse[0:verse.find(" ")]:
                    verses[heading][-1] += " " + verse[verse.find(" ") + 1:]
                else:
                    verses[heading].append(verse)
                verse = ""
            elif ot_quote_regex.search(line):
                ot_quote_start = line.find("<otquote>") + 9
                verse += line[:ot_quote_start - 9]
                verse += " " + line[ot_quote_start:line.find("</otquote", ot_quote_start)]
            elif p_no_ind_regex.search(line):
                verse_start = line.find("<p type=\"noind\">") + 16
                if "<sup" in line:
                    verse_end = line.find("<sup")
                    ignoring = line.find("</sup") > -1
                    verse += " " + line[verse_start:verse_end]
                else:
                    verse += " " + line[verse_start:]
                    ignoring = line.find("</sup>") == line.rfind("</sup>")
            elif rare_p_right_regex.search(line):
                verse += line[line.find("<p type=\"right\">") + 16:]
            elif "<p>" in line:
                verse_start = line.find(">") + 1
                if "<sup" in line:
                    verse_end = line.find("<sup")
                    if "</sup" not in line:
                        ignoring = True
                elif "</p>" in line:
                    verse_end = line.find("</p>")
                else:
                    verse_end = len(line) - 1
                verse += " " + line[verse_start:verse_end]
            elif "<item><sup class=\"verse-ref\"" in line:
                verse += line[line.find("</sup>") + 6:]
            elif verse_inline_ref_regex.search(line):
                verse += line[0:line.find("<sup")]
                if not line.find("</sup>") > -1:
                    ignoring = True
                elif len(line) - line.find("</sup>") - 6 > 1:
                    verse += line[line.find("</sup>") + 6:]
            elif verse_verse_ref_regex.search(line):
                sup_pos = line.find("</sup>") + 7
                verse += line[sup_pos:]
            elif poem_right_selah_regex.search(line):
                verse += " Selah"
            elif verse_content_end_tag_regex.search(line) and len(condense.sub(' ', verse)) > 10:
                verse += line[:line.find("</verse")]
                if heading in verses and len(verses[heading]):
                    if verses[heading][-1][0:verses[heading][-1].find(" ")] == verse[0:verse.find(" ")]:
                        verses[heading][-1] += " " + lazy_tag_removal_regex.sub(' ', condense.sub(' ', fix_lord_regex.sub('Lord', verse))[verse.find(" ") + 1:])
                    else:
                        verses[heading].append(lazy_tag_removal_regex.sub(' ', condense.sub(' ', fix_lord_regex.sub('Lord', verse))))
                else:
                    verses[heading] = [lazy_tag_removal_regex.sub(' ', condense.sub(' ', fix_lord_regex.sub('Lord', verse)))]
                verse = ""
            else:
                verse += " " + line

        return verses