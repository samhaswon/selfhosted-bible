from bibles.passage import PassageInvalid, PassageNotFound
from typing import Dict
from bibles.bible import Bible
import xml.etree.ElementTree as ElementTree
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
        return {'book': book, 'chapter': chapter, 'verses': self.__cache[book][str(chapter)]}

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
        Parses the given XML into the cache
        :param xml_in: Full XML document in string form
        :return: None
        """
        condense = re.compile(r'\s\s+|\n\s*')
        root = ElementTree.fromstring(xml_in)

        result = {}
        bookname = root.find('bookname').text if root.find('bookname').text != "Song of Songs" else "Song of Solomon"
        result[bookname] = {}

        for chapter in root.findall('chapter'):
            chapter_number = chapter.get('display')
            result[bookname][chapter_number] = {}
            chapter_dict = {}
            current_heading = 'none'
            for element in chapter:
                if element.tag == 'head1' or element.tag == 'head2' or element.tag == 'supertitle':
                    current_heading = condense.sub('', ''.join(element.itertext()))
                    chapter_dict[current_heading] = []
                elif element.tag == 'blockindent':
                    if current_heading not in chapter_dict:
                        chapter_dict[current_heading] = []
                    for verse in element.findall('.//verse'):
                        verse_number = verse.get('display-number')
                        verse_text = ''.join(verse.itertext())
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                        if len(chapter_dict[current_heading]) > 0 and chapter_dict[current_heading][-1][
                                                                      0:chapter_dict[current_heading][-1].find(
                                                                              " ")] != verse_number:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                        elif len(chapter_dict[current_heading]) > 0:
                            chapter_dict[current_heading][-1] += verse_text
                        else:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                elif element.tag == 'listtenwords':
                    if current_heading not in chapter_dict:
                        chapter_dict[current_heading] = []
                    for verse in element.findall('.//verse'):
                        verse_number = verse.get('display-number')
                        verse_text = ''.join(verse.itertext())
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                        if len(chapter_dict[current_heading]) > 0 and chapter_dict[current_heading][-1][
                                                                      0:chapter_dict[current_heading][-1].find(
                                                                              " ")] != verse_number:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                        elif len(chapter_dict[current_heading]) > 0:
                            chapter_dict[current_heading][-1] += verse_text
                        else:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                elif element.tag == 'p':
                    if current_heading not in chapter_dict:
                        chapter_dict[current_heading] = []
                    for verse in element.findall('verse'):
                        verse_number = verse.get('display-number')
                        verse_text = ''.join(verse.itertext())
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                        if len(chapter_dict[current_heading]) > 0 and chapter_dict[current_heading][-1][
                                                                      0:chapter_dict[current_heading][-1].find(
                                                                              " ")] != verse_number:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                        elif len(chapter_dict[current_heading]) > 0:
                            chapter_dict[current_heading][-1] += verse_text
                        else:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                elif element.tag == 'poetryblock':
                    if current_heading not in chapter_dict:
                        chapter_dict[current_heading] = []
                    for verse in element.findall('verse'):
                        verse_number = verse.get('display-number')
                        verse_text = ''.join(verse.itertext())
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                        if len(chapter_dict[current_heading]) > 0 and chapter_dict[current_heading][-1][
                                                                      0:chapter_dict[current_heading][-1].find(
                                                                              " ")] != verse_number:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                        elif len(chapter_dict[current_heading]) > 0:
                            chapter_dict[current_heading][-1] += verse_text
                        else:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                elif element.tag == 'dynprose' or element.tag == 'otdynprose':
                    if current_heading not in chapter_dict:
                        chapter_dict[current_heading] = []
                    for verse in element.findall('.//verse'):
                        verse_number = verse.get('display-number')
                        verse_text = ''.join(verse.itertext())
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                        if len(chapter_dict[current_heading]) > 0 and chapter_dict[current_heading][-1][
                                                                      0:chapter_dict[current_heading][-1].find(
                                                                              " ")] != verse_number:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                        elif len(chapter_dict[current_heading]) > 0:
                            chapter_dict[current_heading][-1] += verse_text
                        else:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                elif element.tag == 'verse':
                    if x := element.findall('head1'):
                        current_heading = ''.join(head.text for head in x)
                    if current_heading not in chapter_dict:
                        chapter_dict[current_heading] = []
                    verse_text = ""
                    verse_number = ""
                    for verse in element.findall('.//item'):
                        verse_number = element.get('display-number')
                        verse_text += ''.join(verse.itertext())
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                    for verse in element.findall('p'):
                        verse_number = element.get('display-number')
                        verse_text += ''.join(verse.itertext())
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                    for verse in element.findall('.//p'):
                        verse_number = element.get('display-number')
                        verse_text += ''.join(verse.itertext())
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                    for verse in element.findall('poetryblock'):
                        verse_number = element.get('display-number')
                        verse_text += ''.join(verse.itertext())
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                    if len(chapter_dict[current_heading]) > 0 and chapter_dict[current_heading][-1][
                                                                  0:chapter_dict[current_heading][-1].find(
                                                                          " ")] != verse_number:
                        chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                    elif len(chapter_dict[current_heading]) > 0:
                        chapter_dict[current_heading][-1] = \
                            condense.sub(' ', chapter_dict[current_heading][-1] + " " + verse_text)
                    else:
                        chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                # Lots of list variations for some reason
                elif element.tag == 'list' or element.tag == 'listblockindent':
                    if current_heading not in chapter_dict:
                        chapter_dict[current_heading] = []
                    for verse in element.findall('.//verse'):
                        verse_number = verse.get('display-number') if verse.get('display-number') else \
                            verse.get('reference')[verse.get('reference').rfind('.') + 1:] if verse.get('reference') \
                                else verse.get('id')[verse.get('id').rfind('.') + 1:]
                        verse_text = ''.join(verse.itertext())
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                        if len(chapter_dict[current_heading]) > 0 and \
                                chapter_dict[current_heading][-1][0:chapter_dict[current_heading][-1].find(" ")] !=\
                                verse_number:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                        elif len(chapter_dict[current_heading]) > 0:
                            chapter_dict[current_heading][-1] += verse_text
                        else:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                elif element.tag == 'listtable' and bookname == "Joshua":
                    if current_heading not in chapter_dict:
                        chapter_dict[current_heading] = []
                    for row in element.findall('row'):
                        cells = row.findall('cell')
                        verse = cells[0].find('.//verse')

                        if verse is not None:
                            verse_number = verse.get('display')
                            verse_text = ''.join(cells[0].itertext()) + " " + ''.join(cells[1].itertext())
                            verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                            if len(chapter_dict[current_heading]) > 0 and chapter_dict[current_heading][-1][
                                                                          0:chapter_dict[current_heading][-1].find(
                                                                                  " ")] != verse_number:
                                chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                            elif len(chapter_dict[current_heading]) > 0:
                                chapter_dict[current_heading][-1] += verse_text
                            else:
                                chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                        else:
                            chapter_dict[current_heading][-1] +=\
                                ', ' + condense.sub(' ', ''.join(cells[0].itertext()) +
                                                    " " + ''.join(cells[1].itertext()))
                elif element.tag == 'listtable':
                    if current_heading not in chapter_dict:
                        chapter_dict[current_heading] = []
                    for verse in element.findall('verse'):
                        verse_number = verse.get('display-number')
                        verse_text = ''.join(verse.itertext())
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                        if len(chapter_dict[current_heading]) > 0 and chapter_dict[current_heading][-1][
                                                                      0:chapter_dict[current_heading][-1].find(
                                                                          " ")] != verse_number:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                        elif len(chapter_dict[current_heading]) > 0:
                            chapter_dict[current_heading][-1] += verse_text
                        else:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
            result[bookname][chapter_number] = chapter_dict

        # Split verses that are not separated by a unique verse tag
        if bookname == 'Genesis':
            result[bookname]['3']['Sin’s Consequences'][9] = result[bookname]['3']['Sin’s Consequences'][9][135:]
            result[bookname]['4']['Cain Murders Abel'][8] = result[bookname]['4']['Cain Murders Abel'][8][:120]
            result[bookname]['22']['The Sacrifice of Isaac'][6] = \
                result[bookname]['22']['The Sacrifice of Isaac'][6][:193]
            result[bookname]['27']['The Stolen Blessing'][38] += "Look, your dwelling place will be away from the " \
                                                                 "richness of the land, away from the dew of the sky " \
                                                                 "above."
            result[bookname]['30']['none'][14] = result[bookname]['30']['none'][14][:221]
            result[bookname]['37']['Joseph’s Dreams'][1] = result[bookname]['37']['Joseph’s Dreams'][1][:245]

            split_location = result[bookname]['9']['God’s Covenant with Noah'][14].find('16')
            tmp_split = result[bookname]['9']['God’s Covenant with Noah'][14][0:split_location], \
                result[bookname]['9']['God’s Covenant with Noah'][14][split_location:]
            result[bookname]['9']['God’s Covenant with Noah'][14] = tmp_split[0]
            result[bookname]['9']['God’s Covenant with Noah'].insert(15, tmp_split[1])

            split_location = result[bookname]['39']['Joseph in Potiphar’s House'][12].find('14')
            tmp_split = result[bookname]['39']['Joseph in Potiphar’s House'][12][0:split_location], \
                result[bookname]['39']['Joseph in Potiphar’s House'][12][split_location:]
            result[bookname]['39']['Joseph in Potiphar’s House'][12] = tmp_split[0]
            result[bookname]['39']['Joseph in Potiphar’s House'].insert(13, tmp_split[1])

        elif bookname == 'Exodus':
            result[bookname]['32']['The Gold Calf'][17] += "It’s not the sound of a victory cry and not the sound of " \
                                                           "a cry of defeat; I hear the sound of singing!"

        elif bookname == 'Numbers':
            split_location = result[bookname]['1']['The Census of Israel'][31].find('33')
            tmp_split = result[bookname]['1']['The Census of Israel'][31][0:split_location], \
                result[bookname]['1']['The Census of Israel'][31][split_location:]
            result[bookname]['1']['The Census of Israel'][31] = tmp_split[0]
            result[bookname]['1']['The Census of Israel'].insert(32, tmp_split[1])

            # This one grabs data twice for some reason, so here's this
            split_location = result[bookname]['12']['Miriam and Aaron Rebel'][6].find('8')
            tmp_split = result[bookname]['12']['Miriam and Aaron Rebel'][6][0:split_location], \
                result[bookname]['12']['Miriam and Aaron Rebel'][6][split_location:]
            result[bookname]['12']['Miriam and Aaron Rebel'][6] = tmp_split[0]
            result[bookname]['12']['Miriam and Aaron Rebel'][7] = \
                tmp_split[1] + result[bookname]['12']['Miriam and Aaron Rebel'][8][1:]
            result[bookname]['12']['Miriam and Aaron Rebel'].pop(8)

        elif bookname == "Joshua":
            result[bookname]['5']['Commander of the Lord’s Army'][1] = \
                result[bookname]['5']['Commander of the Lord’s Army'][1][:196]

        elif bookname == 'Judges':
            # Once again, duplicated data
            result[bookname]['15']['Samson’s Revenge'][5] = result[bookname]['15']['Samson’s Revenge'][5][:238]
            result[bookname]['17']['Micah’s Priest'][8] = result[bookname]['17']['Micah’s Priest'][8][:155]

        elif bookname == 'Ruth':
            result[bookname]['2']['Ruth and Boaz Meet'][18] = result[bookname]['2']['Ruth and Boaz Meet'][18][:252]

        elif bookname == '1 Samuel':
            # Once again, duplicated data
            result[bookname]['28']['Saul and the Medium'][14] = result[bookname]['28']['Saul and the Medium'][14][:308]
            result[bookname]['29']['Philistines Reject David'][2] = \
                result[bookname]['29']['Philistines Reject David'][2][:289]

        elif bookname == '2 Samuel':
            # Once again, duplicated data
            result[bookname]['16']['Ziba Helps David'][1] = result[bookname]['16']['Ziba Helps David'][1][:250]
            result[bookname]['18']['Absalom’s Death'][23] = result[bookname]['18']['Absalom’s Death'][23][:229]

        elif bookname == "1 Kings":
            split_location = result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'][3].find('5')
            tmp_split = result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'][3][0:split_location], \
                result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'][3][split_location:393]
            result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'][3] = tmp_split[0]
            result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'].insert(4, tmp_split[1])

        elif bookname == "2 Kings":
            result[bookname]['8']['Aram’s King Hazael'][5] = result[bookname]['8']['Aram’s King Hazael'][5][:288]

        elif bookname == "1 Chronicles":
            result[bookname]['29']['David’s Prayer'][12] = "22 " + result[bookname]['29']['David’s Prayer'][12][3:]
            result[bookname]['29']['The Enthronement of Solomon'][0] = \
                "22 " + result[bookname]['29']['The Enthronement of Solomon'][0][4:]

        elif bookname == "Jeremiah":
            split_location = result[bookname]['49']['Prophecies against Kedar and Hazor'][0].find('29')
            tmp_split = result[bookname]['49']['Prophecies against Kedar and Hazor'][0][0:split_location], \
                result[bookname]['49']['Prophecies against Kedar and Hazor'][0][split_location:]
            result[bookname]['49']['Prophecies against Kedar and Hazor'][0] = tmp_split[0]
            result[bookname]['49']['Prophecies against Kedar and Hazor'].insert(1, tmp_split[1])

        elif bookname == "Ezekiel":
            split_location = result[bookname]['27']['The Sinking of Tyre'][2].find('4')
            tmp_split = result[bookname]['27']['The Sinking of Tyre'][2][0:split_location], \
                result[bookname]['27']['The Sinking of Tyre'][2][split_location:]
            result[bookname]['27']['The Sinking of Tyre'][2] = tmp_split[0]
            result[bookname]['27']['The Sinking of Tyre'].insert(3, tmp_split[1])

        elif bookname == "Amos":
            # Weird one. It uses the wrong verse number from somewhere.
            result[bookname]["7"]['Third Vision: A Plumb Line'][1] += \
                result[bookname]["7"]['Third Vision: A Plumb Line'][2][1:]
            result[bookname]["7"]['Third Vision: A Plumb Line'].pop(2)

        elif bookname == "Zechariah":
            result[bookname]['1']['Second Vision: Four Horns and Craftsmen'][3] = \
                result[bookname]['1']['Second Vision: Four Horns and Craftsmen'][3][:269]

        elif bookname == "Malachi":
            result[bookname]['2']['Judgment at the Lord’s Coming'][0] = \
                result[bookname]['2']['Judgment at the Lord’s Coming'][0][:231]

        elif bookname == "Matthew":
            # Verses 3-9 of Matthew 5 get grabbed at the same time for whatever reason, so yeah.
            result[bookname]['5']['The Beatitudes'][1] = result[bookname]['5']['The Beatitudes'][0][73:132]
            result[bookname]['5']['The Beatitudes'][2] = result[bookname]['5']['The Beatitudes'][0][132:191]
            result[bookname]['5']['The Beatitudes'][3] = result[bookname]['5']['The Beatitudes'][0][191:277]
            result[bookname]['5']['The Beatitudes'][4] = result[bookname]['5']['The Beatitudes'][0][277:335]
            result[bookname]['5']['The Beatitudes'][5] = result[bookname]['5']['The Beatitudes'][0][335:391]
            result[bookname]['5']['The Beatitudes'][6] = result[bookname]['5']['The Beatitudes'][0][391:]
            result[bookname]['5']['The Beatitudes'][0] = result[bookname]['5']['The Beatitudes'][0][:73]

            # Same thing for 6:9-13
            result[bookname]['6']['The Lord’s Prayer'][1] = result[bookname]['6']['The Lord’s Prayer'][0][94:163]
            result[bookname]['6']['The Lord’s Prayer'][2] = result[bookname]['6']['The Lord’s Prayer'][0][163:197]
            result[bookname]['6']['The Lord’s Prayer'][3] = result[bookname]['6']['The Lord’s Prayer'][0][197:264]
            result[bookname]['6']['The Lord’s Prayer'][4] = result[bookname]['6']['The Lord’s Prayer'][0][264:]
            result[bookname]['6']['The Lord’s Prayer'][0] = result[bookname]['6']['The Lord’s Prayer'][0][:94]

            # Odd one
            split_location = result[bookname]['11']['An Unresponsive Generation'][0].find(':') + 1
            tmp_split = result[bookname]['11']['An Unresponsive Generation'][0][0:split_location], \
                "17" + result[bookname]['11']['An Unresponsive Generation'][0][split_location:]
            result[bookname]['11']['An Unresponsive Generation'][0] = tmp_split[0]
            result[bookname]['11']['An Unresponsive Generation'].insert(1, tmp_split[1])

        elif bookname == "Luke":
            tmp_split = result[bookname]['20']['The Parable of the Vineyard Owner'][6][0:111], \
                result[bookname]['20']['The Parable of the Vineyard Owner'][6][111:301]
            result[bookname]['20']['The Parable of the Vineyard Owner'][6] = tmp_split[0]
            result[bookname]['20']['The Parable of the Vineyard Owner'].insert(7, tmp_split[1])
        elif bookname == "Acts":
            tmp = "8 " + result[bookname]['24']['The Accusation against Paul'][5][68:]
            result[bookname]['24']['The Accusation against Paul'][5] = \
                result[bookname]['24']['The Accusation against Paul'][5][:68]
            result[bookname]['24']['The Accusation against Paul'].insert(6, tmp)

        elif bookname == "Romans":
            result[bookname]['15']['Glorifying God Together'][4] += result[bookname]['15']['Glorifying God Together'][5][4:]
            result[bookname]['15']['Glorifying God Together'].pop(5)

        self.__cache[bookname] = result[bookname]
