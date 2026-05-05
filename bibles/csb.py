"""
Class for the CSB version
"""

from typing import Dict, Any
import re

from xml.etree import ElementTree
from requests import get, HTTPError

# pylint: disable=import-error
from bibles.api_bible import APIBible
from bibles.passage import PassageNotFound


# You get a lot from the ABC, so there is no need for more.
# pylint: disable=too-few-public-methods
class CSB(APIBible):
    """
    Class for the CSB version
    """
    def __init__(self):
        """
        Create an instance of the CSB
        """
        super().__init__(cache_name="csb")

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

    def api_return(self, book: str, chapter: Any) -> None:
        """
        So, I'm not a fan of doing this how I am. The API only has the full books afaik.
        Their search method gets all 66, so it was not made to be the most efficient.
        Though, this does cache it, which is efficient (~5µs access times on my dev machine).
        :param book: Book to get, pre validated
        :param chapter: Anything, just for APIBible compatability.
        :return: The full book as a dictionary
        """
        print(f"[CSB] Getting {book} ({chapter})")
        try:
            # The pseudo API. This is pretty much just grabbing and parsing XML files.
            uri = "https://read.csbible.com/wp-content/themes/lwcsbread/CSB_XML//"

            # Hey website! I'm a browser!
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 '
                              'Firefox/112.0',
                'Accept': 'application/xml, text/xml, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.5',
                'X-Requested-With': 'XMLHttpRequest',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            }
            passage = self.__file_aliases[book]
            response = get(
                f"{uri}{passage}",
                headers=headers,
                cookies={'credentials': 'include'},
                timeout=30
            )
            response.raise_for_status()

            self.__parse(response.text)
        except HTTPError as ex:
            raise PassageNotFound(f"Error getting {book}: {str(ex)}") from ex

    # pylint: disable=consider-using-in,too-many-locals,too-many-branches,too-many-nested-blocks,too-many-statements
    def __parse(self, xml_in: str) -> None:
        """
        Parses the given XML into the cache
        :param xml_in: Full XML document in string form
        :return: None
        """
        condense = re.compile(r'\s\s+|\n\s*')
        root = ElementTree.fromstring(xml_in)

        result = {}
        bookname = root.find('bookname').text if (
                root.find('bookname').text != "Song of Songs") \
            else "Song of Solomon"
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
                        verse_text = condense.sub(
                            ' ', re.sub(r'^\s*\d+\s*',
                                        '',
                                        verse_text)
                        )
                        if (len(chapter_dict[current_heading]) > 0 and
                                chapter_dict[current_heading][-1][
                                0:chapter_dict[current_heading][-1].find(" ")] != verse_number
                        ):
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
                        verse_text = condense.sub(
                            ' ',
                            re.sub(
                                r'^\s*\d+\s*',
                                '',
                                verse_text
                            )
                        )
                        if (len(chapter_dict[current_heading]) > 0 and
                                chapter_dict[current_heading][-1][
                                0:chapter_dict[current_heading][-1].find(" ")] != verse_number
                        ):
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
                        verse_text = condense.sub(
                            ' ',
                            re.sub(
                                r'^\s*\d+\s*',
                                '',
                                verse_text
                            )
                        )
                        if (len(chapter_dict[current_heading]) > 0 and
                                chapter_dict[current_heading][-1][
                                0:chapter_dict[current_heading][-1].find(" ")] != verse_number
                        ):
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
                        verse_text = condense.sub(
                            ' ',
                            re.sub(
                                r'^\s*\d+\s*',
                                '',
                                verse_text
                            )
                        )
                        if (len(chapter_dict[current_heading]) > 0 and
                                chapter_dict[current_heading][-1][
                                0:chapter_dict[current_heading][-1].find(" ")] != verse_number
                        ):
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
                        verse_text = condense.sub(
                            ' ',
                            re.sub(
                                r'^\s*\d+\s*',
                                '',
                                verse_text
                            )
                        )
                        if (len(chapter_dict[current_heading]) > 0 and
                                chapter_dict[current_heading][-1][
                                0:chapter_dict[current_heading][-1].find(" ")] != verse_number
                        ):
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
                        new_text = ''.join(verse.itertext())
                        verse_text += new_text if new_text not in verse_text else ""
                        verse_text = condense.sub(
                            ' ',
                            re.sub(
                                r'^\s*\d+\s*',
                                '',
                                verse_text
                            )
                        )
                    for verse in element.findall('p'):
                        verse_number = element.get('display-number')
                        new_text = ''.join(verse.itertext())
                        verse_text += new_text if new_text not in verse_text else ""
                        verse_text = condense.sub(
                            ' ',
                            re.sub(
                                r'^\s*\d+\s*',
                                '',
                                verse_text
                            )
                        )
                    for verse in element.findall('.//p'):
                        verse_number = element.get('display-number')
                        new_text = ''.join(verse.itertext())
                        verse_text += new_text if new_text not in verse_text else ""
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                    for verse in element.findall('poetryblock'):
                        verse_number = element.get('display-number')
                        new_text = ''.join(verse.itertext())
                        verse_text += new_text if new_text not in verse_text else ""
                        verse_text = condense.sub(' ', re.sub(r'^\s*\d+\s*', '', verse_text))
                    if (len(chapter_dict[current_heading]) > 0 and
                            chapter_dict[current_heading][-1][
                            0:chapter_dict[current_heading][-1].find(" ")
                            ] != verse_number
                    ):
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
                        verse_number = verse.get('display-number') \
                            if verse.get('display-number') else \
                            verse.get('reference')[verse.get('reference').rfind('.') + 1:] \
                                if verse.get('reference') \
                                else verse.get('id')[verse.get('id').rfind('.') + 1:]
                        verse_text = ''.join(verse.itertext())
                        verse_text = condense.sub(
                            ' ',
                            re.sub(
                                r'^\s*\d+\s*',
                                '',
                                verse_text
                            )
                        )
                        if len(chapter_dict[current_heading]) > 0 and \
                                chapter_dict[current_heading][-1][
                                0:chapter_dict[current_heading][-1].find(" ")] !=\
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
                            verse_text = (
                                    ''.join(
                                        cells[0].itertext()
                                    ) + " " +
                                    ''.join(
                                        cells[1].itertext()
                                    )
                            )
                            verse_text = condense.sub(
                                ' ',
                                re.sub(r'^\s*\d+\s*',
                                       '',
                                       verse_text
                                       )
                            )
                            if (len(chapter_dict[current_heading]) > 0 and
                                    chapter_dict[current_heading][-1][
                                    0:chapter_dict[current_heading][-1].find(" ")] != verse_number
                            ):
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
                        verse_text = condense.sub(
                            ' ',
                            re.sub(
                                r'^\s*\d+\s*',
                                '',
                                verse_text
                            )
                        )
                        if (len(chapter_dict[current_heading]) > 0 and
                                chapter_dict[current_heading][-1][
                                0:chapter_dict[current_heading][-1].find(" ")] != verse_number
                        ):
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
                        elif len(chapter_dict[current_heading]) > 0:
                            chapter_dict[current_heading][-1] += verse_text
                        else:
                            chapter_dict[current_heading].append(f"{verse_number} {verse_text}")
            result[bookname][chapter_number] = chapter_dict

        # Split verses that are not separated by a unique verse tag
        if bookname == 'Genesis':
            result[bookname]['3']['Sin’s Consequences'][9] = \
                result[bookname]['3']['Sin’s Consequences'][9][135:]
            result[bookname]['4']['Cain Murders Abel'][8] = \
                result[bookname]['4']['Cain Murders Abel'][8][:120]
            result[bookname]['22']['The Sacrifice of Isaac'][6] = \
                result[bookname]['22']['The Sacrifice of Isaac'][6][:193]
            result[bookname]['27']['The Stolen Blessing'][38] += \
                "Look, your dwelling place will be away from the " \
                "richness of the land, away from the dew of the sky " \
                "above."
            result[bookname]['30']['none'][14] = result[bookname]['30']['none'][14][:221]
            result[bookname]['37']['Joseph’s Dreams'][1] = \
                result[bookname]['37']['Joseph’s Dreams'][1][:245]

            split_location = result[bookname]['9']['God’s Covenant with Noah'][14].find('16')
            tmp_split = result[bookname]['9']['God’s Covenant with Noah'][14][0:split_location], \
                result[bookname]['9']['God’s Covenant with Noah'][14][split_location:]
            result[bookname]['9']['God’s Covenant with Noah'][14] = tmp_split[0]
            result[bookname]['9']['God’s Covenant with Noah'].insert(15, tmp_split[1])

            split_location = result[bookname]['39']['Joseph in Potiphar’s House'][12].find('14')
            tmp_split = \
                result[bookname]['39']['Joseph in Potiphar’s House'][12][0:split_location], \
                result[bookname]['39']['Joseph in Potiphar’s House'][12][split_location:]
            result[bookname]['39']['Joseph in Potiphar’s House'][12] = tmp_split[0]
            result[bookname]['39']['Joseph in Potiphar’s House'].insert(13, tmp_split[1])

        elif bookname == 'Exodus':
            result[bookname]['32']['The Gold Calf'][17] += \
                "It’s not the sound of a victory cry and not the sound of " \
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
            result[bookname]['15']['Samson’s Revenge'][5] = \
                result[bookname]['15']['Samson’s Revenge'][5][:238]
            result[bookname]['17']['Micah’s Priest'][8] = \
                result[bookname]['17']['Micah’s Priest'][8][:155]

        elif bookname == 'Ruth':
            result[bookname]['2']['Ruth and Boaz Meet'][18] = \
                result[bookname]['2']['Ruth and Boaz Meet'][18][:252]

        elif bookname == '1 Samuel':
            # Once again, duplicated data
            result[bookname]['3']['Samuel’s Call'][4] = \
                result[bookname]['3']['Samuel’s Call'][4][:133]
            result[bookname]['3']['Samuel’s Call'][5] = \
                result[bookname]['3']['Samuel’s Call'][5][:167]
            result[bookname]['3']['Samuel’s Call'][9] = \
                result[bookname]['3']['Samuel’s Call'][9][:130]
            result[bookname]['3']['Samuel’s Call'][15] = \
                result[bookname]['3']['Samuel’s Call'][15][:80]

            result[bookname]['27']['David Flees to Ziklag'][9] = \
                result[bookname]['27']['David Flees to Ziklag'][9][:172]

            result[bookname]['28']['Saul and the Medium'][1] = \
                result[bookname]['28']['Saul and the Medium'][1][:163]
            result[bookname]['28']['Saul and the Medium'][6] = \
                result[bookname]['28']['Saul and the Medium'][6][:166]
            result[bookname]['28']['Saul and the Medium'][10] = \
                result[bookname]['28']['Saul and the Medium'][10][:110]
            result[bookname]['28']['Saul and the Medium'][12] = \
                result[bookname]['28']['Saul and the Medium'][12][:136]
            result[bookname]['28']['Saul and the Medium'][13] = \
                result[bookname]['28']['Saul and the Medium'][13][:211]
            result[bookname]['28']['Saul and the Medium'][14] = \
                result[bookname]['28']['Saul and the Medium'][14][:308]

            result[bookname]['29']['Philistines Reject David'][2] = \
                result[bookname]['29']['Philistines Reject David'][2][:289]

            result[bookname]['30']['David’s Defeat of the Amalekites'][7] = \
                result[bookname]['30']['David’s Defeat of the Amalekites'][7][:184]
            result[bookname]['30']['David’s Defeat of the Amalekites'][14] = \
                result[bookname]['30']['David’s Defeat of the Amalekites'][14][:175]

        elif bookname == '2 Samuel':
            # Once again, duplicated data
            result[bookname]['1']['Responses to Saul’s Death'][2] = \
                result[bookname]['1']['Responses to Saul’s Death'][2][:107]
            result[bookname]['1']['Responses to Saul’s Death'][3] = \
                result[bookname]['1']['Responses to Saul’s Death'][3][:189]
            result[bookname]['1']['Responses to Saul’s Death'][12] = \
                result[bookname]['1']['Responses to Saul’s Death'][12][:154]

            result[bookname]['16']['Ziba Helps David'][1] = \
                result[bookname]['16']['Ziba Helps David'][1][:250]
            result[bookname]['16']['Ziba Helps David'][2] = \
                result[bookname]['16']['Ziba Helps David'][2][:204]
            result[bookname]['16']['Ziba Helps David'][3] = \
                result[bookname]['16']['Ziba Helps David'][3][:154]

            result[bookname]['17']['David Informed of Absalom’s Plans'][5] = \
                result[bookname]['17']['David Informed of Absalom’s Plans'][5][:232]
            result[bookname]['17']['David Informed of Absalom’s Plans'][14] = \
                result[bookname]['17']['David Informed of Absalom’s Plans'][14][:42] + \
                result[bookname]['17']['David Informed of Absalom’s Plans'][14][51:]

            result[bookname]['18']['Absalom’s Death'][13] = \
                result[bookname]['18']['Absalom’s Death'][13][:201]
            result[bookname]['18']['Absalom’s Death'][18] = \
                result[bookname]['18']['Absalom’s Death'][18][:170]
            result[bookname]['18']['Absalom’s Death'][20] = \
                result[bookname]['18']['Absalom’s Death'][20][:184]
            result[bookname]['18']['Absalom’s Death'][23] = \
                result[bookname]['18']['Absalom’s Death'][23][:229]

            # This one is messed up in the XML to the extent it's messed up on their site too
            result[bookname]['24']['David’s Punishment'][5] = \
                result[bookname]['24']['David’s Punishment'][5][:270] + " the Jebusite."

            result[bookname]['24']['David’s Altar'][3] = \
                result[bookname]['24']['David’s Altar'][3][:202]

        elif bookname == "1 Kings":
            # The whole verse is in this one twice. Weird
            result[bookname]['2']['Joab’s Execution'][1] = \
                result[bookname]['2']['Joab’s Execution'][1][:187]
            result[bookname]['3']['Solomon’s Wisdom'][6] = \
                result[bookname]['3']['Solomon’s Wisdom'][6][:197]

            result[bookname]['8']['Solomon’s Dedication of the Temple'][17] = \
                result[bookname]['8']['Solomon’s Dedication of the Temple'][16][104:]
            result[bookname]['8']['Solomon’s Dedication of the Temple'][16] = \
                result[bookname]['8']['Solomon’s Dedication of the Temple'][16][:104]

            result[bookname]['20']['Victory over Ben-hadad'][13] = \
                result[bookname]['20']['Victory over Ben-hadad'][13][:188]
            result[bookname]['20']['Victory over Ben-hadad'][33] = \
                result[bookname]['20']['Victory over Ben-hadad'][33][:300]
            result[bookname]['20']['Ahab Rebuked by theLord'][5] = \
                result[bookname]['20']['Ahab Rebuked by theLord'][5][:160]

            split_location = \
                result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'][3].find('5')
            tmp_split = \
                result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'][3][0:split_location], \
                result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'][3][split_location:278]
            result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'][3] = tmp_split[0]
            result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'].insert(4, tmp_split[1])
            result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'][5] = \
                result[bookname]['22']['Jehoshaphat’s Alliance with Ahab'][5][:223]
            result[bookname]['22']['Micaiah’s Message of Defeat'][2] = \
                result[bookname]['22']['Micaiah’s Message of Defeat'][2][:206]
            result[bookname]['22']['Micaiah’s Message of Defeat'][9] = \
                result[bookname]['22']['Micaiah’s Message of Defeat'][9][:190]

        elif bookname == "2 Kings":
            result[bookname]['3']['Moab’s Rebellion against Israel'][3] = \
                result[bookname]['3']['Moab’s Rebellion against Israel'][3][:243]
            result[bookname]['3']['Moab’s Rebellion against Israel'][7] = \
                result[bookname]['3']['Moab’s Rebellion against Israel'][7][:234]
            result[bookname]['3']['Moab’s Rebellion against Israel'][9] = \
                result[bookname]['3']['Moab’s Rebellion against Israel'][9][:253]

            result[bookname]['7']['none'][1] = result[bookname]['7']['none'][1][:253]

            result[bookname]['8']['Aram’s King Hazael'][5] = \
                result[bookname]['8']['Aram’s King Hazael'][5][:288]

            result[bookname]['9']['Jehu Anointed as Israel’s King'][11] = \
                result[bookname]['9']['Jehu Anointed as Israel’s King'][11][:172]
            result[bookname]['9']['Jehu Kills Joram and Ahaziah'][1] = \
                result[bookname]['9']['Jehu Kills Joram and Ahaziah'][1][:221]
            result[bookname]['9']['Jehu Kills Joram and Ahaziah'][6] =\
                "22 " + result[bookname]['9']['Jehu Kills Joram and Ahaziah'][1][3:183]

            result[bookname]['20']['Hezekiah’s Folly'][3] = \
                result[bookname]['20']['Hezekiah’s Folly'][3][:180]

            result[bookname]['23']['Josiah’s Reforms'][13] = \
                result[bookname]['23']['Josiah’s Reforms'][13][:205]

        elif bookname == "1 Chronicles":
            result[bookname]['11']['Exploits of David’s Warriors'][1] = \
                result[bookname]['11']['Exploits of David’s Warriors'][1][:90] + \
                result[bookname]['11']['Exploits of David’s Warriors'][1][344:]

            result[bookname]['29']['David’s Prayer'][12] = \
                "22 " + result[bookname]['29']['David’s Prayer'][12][3:]
            result[bookname]['29']['The Enthronement of Solomon'][0] = \
                "22 " + result[bookname]['29']['The Enthronement of Solomon'][0][4:]

        elif bookname == "2 Chronicles":
            result[bookname]['11']['Rehoboam in Jerusalem'][3] = \
                result[bookname]['11']['Rehoboam in Jerusalem'][3][:236]

            result[bookname]['25']['Amaziah’s Campaign against Edom'][11] = \
                result[bookname]['25']['Amaziah’s Campaign against Edom'][11][:276]

        elif bookname == "Ezra":
            result[bookname]['2']['The Exiles Who Returned'][35] += \
                "Jedaiah’s descendants of the house of Jeshua 973"
            result[bookname]['2']['The Exiles Who Returned'][39] += \
                "Jeshua’s and Kadmiel’s descendants from Hodaviah’s" \
                " descendants 74"
            result[bookname]['2']['The Exiles Who Returned'][40] += \
                "Asaph’s descendants 128"
            result[bookname]['2']['The Exiles Who Returned'][41] += \
                "Shallum’s descendants, Ater’s descendants, " \
                "Talmon’s descendants, Akkub’s descendants, " \
                "Hatita’s descendants, Shobai’s descendants, " \
                "in all 139"
            result[bookname]['2']['The Exiles Who Returned'][43] += \
                " Siaha’s descendants, Padon’s descendants,"
            result[bookname]['2']['The Exiles Who Returned'][44] += \
                "Akkub’s descendants,"
            result[bookname]['2']['The Exiles Who Returned'][44] = \
                result[bookname]['2']['The Exiles Who Returned'][44][3:]

        elif bookname == "Nehemiah":
            result[bookname]['5']['Social Injustice'][12] = \
                result[bookname]['5']['Social Injustice'][12][:283]
            result[bookname]['13']['Nehemiah’s Further Reforms'][21] = \
                result[bookname]['13']['Nehemiah’s Further Reforms'][21][:234]
            result[bookname]['13']['Nehemiah’s Further Reforms'][30] = \
                result[bookname]['13']['Nehemiah’s Further Reforms'][30][:125]

        elif bookname == "Isaiah":
            result[bookname]['31']['The Lord, the Only Help'][8] = \
                result[bookname]['31']['The Lord, the Only Help'][8][:195]
            result[bookname]['39']['Hezekiah’s Folly'][3] = \
                result[bookname]['39']['Hezekiah’s Folly'][3][:239]

        elif bookname == "Jeremiah":
            split_location = \
                result[bookname]['49']['Prophecies against Kedar and Hazor'][0].find('29')
            tmp_split = \
                result[bookname]['49']['Prophecies against Kedar and Hazor'][0][0:split_location], \
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
            result[bookname]['1']['A Plea for Repentance'][5] = \
                result[bookname]['1']['A Plea for Repentance'][5][:243]
            result[bookname]['1']['Second Vision: Four Horns and Craftsmen'][3] = \
                result[bookname]['1']['Second Vision: Four Horns and Craftsmen'][3][:269]

        elif bookname == "Malachi":
            result[bookname]['2']['Judgment at the Lord’s Coming'][0] = \
                result[bookname]['2']['Judgment at the Lord’s Coming'][0][:231]

        elif bookname == "Matthew":
            split_location = result[bookname]['4']['Ministry in Galilee'][3].find('16')
            tmp_split = result[bookname]['4']['Ministry in Galilee'][3][0:split_location], \
                result[bookname]['4']['Ministry in Galilee'][3][split_location:]
            result[bookname]['4']['Ministry in Galilee'][3] = tmp_split[0]
            result[bookname]['4']['Ministry in Galilee'][4] = tmp_split[1]

            # Verses 3-9 of Matthew 5 get grabbed at the same time for whatever reason, so yeah.
            result[bookname]['5']['The Beatitudes'][1] = \
                result[bookname]['5']['The Beatitudes'][0][73:132]
            result[bookname]['5']['The Beatitudes'][2] = \
                result[bookname]['5']['The Beatitudes'][0][132:191]
            result[bookname]['5']['The Beatitudes'][3] = \
                result[bookname]['5']['The Beatitudes'][0][191:277]
            result[bookname]['5']['The Beatitudes'][4] = \
                result[bookname]['5']['The Beatitudes'][0][277:335]
            result[bookname]['5']['The Beatitudes'][5] = \
                result[bookname]['5']['The Beatitudes'][0][335:391]
            result[bookname]['5']['The Beatitudes'][6] = \
                result[bookname]['5']['The Beatitudes'][0][391:]
            result[bookname]['5']['The Beatitudes'][0] = \
                result[bookname]['5']['The Beatitudes'][0][:73]

            # Same thing for 6:9-13
            result[bookname]['6']['The Lord’s Prayer'][1] = \
                result[bookname]['6']['The Lord’s Prayer'][0][94:163]
            result[bookname]['6']['The Lord’s Prayer'][2] = \
                result[bookname]['6']['The Lord’s Prayer'][0][163:197]
            result[bookname]['6']['The Lord’s Prayer'][3] = \
                result[bookname]['6']['The Lord’s Prayer'][0][197:264]
            result[bookname]['6']['The Lord’s Prayer'][4] = \
                result[bookname]['6']['The Lord’s Prayer'][0][264:]
            result[bookname]['6']['The Lord’s Prayer'][0] = \
                result[bookname]['6']['The Lord’s Prayer'][0][:94]

            # Odd one
            split_location = \
                result[bookname]['11']['An Unresponsive Generation'][0].find(':') + 1
            tmp_split = \
                result[bookname]['11']['An Unresponsive Generation'][0][0:split_location], \
                "17" + result[bookname]['11']['An Unresponsive Generation'][0][split_location:]
            result[bookname]['11']['An Unresponsive Generation'][0] = tmp_split[0]
            result[bookname]['11']['An Unresponsive Generation'].insert(1, tmp_split[1])

            result[bookname]['20']['Suffering and Service'][1] = \
                result[bookname]['20']['Suffering and Service'][1][:168]

        elif bookname == "Mark":
            result[bookname]['6']['Feeding of the Five Thousand'][7] = \
                result[bookname]['6']['Feeding of the Five Thousand'][7][:160]

        elif bookname == "Luke":
            result[bookname]['3']['The Messiah’s Herald'][13] = \
                result[bookname]['3']['The Messiah’s Herald'][13][:172]

            split_location = result[bookname]['6']['Woe to the Self-Satisfied'][0].find('25')
            tmp_split = result[bookname]['6']['Woe to the Self-Satisfied'][0][0:split_location], \
                result[bookname]['6']['Woe to the Self-Satisfied'][0][split_location:]
            result[bookname]['6']['Woe to the Self-Satisfied'][0] = tmp_split[0]
            result[bookname]['6']['Woe to the Self-Satisfied'][1] = tmp_split[1]

            result[bookname]['8']['Wind and Waves Obey Jesus'][3] = \
                result[bookname]['8']['Wind and Waves Obey Jesus'][3][:177]

            tmp_split = result[bookname]['20']['The Parable of the Vineyard Owner'][6][0:111], \
                result[bookname]['20']['The Parable of the Vineyard Owner'][6][111:301]
            result[bookname]['20']['The Parable of the Vineyard Owner'][6] = tmp_split[0]
            result[bookname]['20']['The Parable of the Vineyard Owner'].insert(7, tmp_split[1])

        elif bookname == "John":
            result[bookname]['1']['John the Baptist’s Testimony'][2] = \
                result[bookname]['1']['John the Baptist’s Testimony'][2][:115]
            result[bookname]['1']['The Lamb of God'][9] = \
                result[bookname]['1']['The Lamb of God'][9][:173]
            result[bookname]['1']['The Lamb of God'][13] = \
                result[bookname]['1']['The Lamb of God'][13][:151]
            result[bookname]['1']['Philip and Nathanael'][5] = \
                result[bookname]['1']['Philip and Nathanael'][5][:132]

            result[bookname]['20']['Mary Magdalene Sees the Risen Lord'][2] = \
                result[bookname]['20']['Mary Magdalene Sees the Risen Lord'][2][:146]
            result[bookname]['20']['Mary Magdalene Sees the Risen Lord'][4] = \
                result[bookname]['20']['Mary Magdalene Sees the Risen Lord'][4][:219]
            result[bookname]['20']['Mary Magdalene Sees the Risen Lord'][5] = \
                result[bookname]['20']['Mary Magdalene Sees the Risen Lord'][5][:115]
            result[bookname]['20']['Thomas Sees and Believes'][1] = \
                result[bookname]['20']['Thomas Sees and Believes'][1][:237]

            result[bookname]['21']['Jesus’s Third Appearance to the Disciples'][2] = \
                result[bookname]['21']['Jesus’s Third Appearance to the Disciples'][2][:162]
            result[bookname]['21']['Jesus’s Threefold Restoration of Peter'][1] = \
                result[bookname]['21']['Jesus’s Threefold Restoration of Peter'][1][:159]
            result[bookname]['21']['Jesus’s Threefold Restoration of Peter'][1] = \
                result[bookname]['21']['Jesus’s Threefold Restoration of Peter'][1][:205] + \
                " “Feed my sheep,” Jesus said."

        elif bookname == "Acts":
            result[bookname]['16']['Paul and Silas in Prison'][2] = \
                result[bookname]['16']['Paul and Silas in Prison'][2][:182]

            result[bookname]['17']['Paul in Athens'][2] = \
                result[bookname]['17']['Paul in Athens'][2][:269]

            result[bookname]['22']['Paul’s Testimony'][4] = \
                result[bookname]['22']['Paul’s Testimony'][4][:161]

            tmp = "8 " + result[bookname]['24']['The Accusation against Paul'][5][68:]
            result[bookname]['24']['The Accusation against Paul'][5] = \
                result[bookname]['24']['The Accusation against Paul'][5][:68]
            result[bookname]['24']['The Accusation against Paul'].insert(6, tmp)

        elif bookname == "Romans":
            result[bookname]['15']['Glorifying God Together'][4] += \
                result[bookname]['15']['Glorifying God Together'][5][4:]
            result[bookname]['15']['Glorifying God Together'].pop(5)

        elif bookname == "2 Peter":
            result[bookname]['1']['Greeting'][0] = result[bookname]['1']['Greeting'][0][:169]

        elif bookname == "Revelation":
            result[bookname]['7']['A Multitude from the Great Tribulation'][5] = \
                result[bookname]['7']['A Multitude from the Great Tribulation'][5][:178]

        for chapter in result[bookname]:
            self.cache[bookname][str(chapter)] = {}
            self.cache[bookname][str(chapter)]['verses'] = result[bookname][str(chapter)]
