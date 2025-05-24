"""
CSB Unit testing
"""
import bz2
import time # Speed testing
from unittest import TestCase
from bibles.csb import CSB
from bibles.kjv import KJV



class TestCSB(TestCase):
    """Test the CSB class"""
    def setUp(self):
        self.csb = CSB()
        self.kjv = KJV()
    def test_get_passage(self):
        """Test CSB passage retrieval"""
        # Also test the time to make sure it's reasonably efficient
        start = time.perf_counter()
        genesis_1 = self.csb.get_passage("Genesis", 1)
        end = time.perf_counter()
        print(f"Finished parsing Genesis in {end - start} seconds")
        self.assertEqual(31, len(genesis_1['verses']['The Creation']))

        # Cache hit time:
        start = time.perf_counter()
        genesis_35 = self.csb.get_passage("Genesis", 35)
        end = time.perf_counter()
        print(
            f"Accessed Genesis 35 in {end - start} seconds ({(end - start) * 1000} milliseconds, "
            f"{(end - start) * 10 ** 6} microseconds)"
        )
        self.assertEqual(15, len(genesis_35['verses']['Return to Bethel']))
        self.assertEqual(5, len(genesis_35['verses']['Rachel’s Death']))

        psalm_1 = self.csb.get_passage("Psalms", 1)
        self.assertEqual(6, len(psalm_1['verses']['The Two Ways']))
        psalm_2 = self.csb.get_passage("Psalms", 2)
        self.assertEqual(12, len(psalm_2['verses']['Coronation of the Son']))
        psalm_3 = self.csb.get_passage("Psalms", 3)
        self.assertEqual(
            8,
            len(psalm_3['verses']['A psalm of David when he fled from his son Absalom.'])
        )
        psalm_119 = self.csb.get_passage("Psalms", 119)
        self.assertEqual(176, len(psalm_119['verses']['Delight in God’s Word']))

        obadiah = self.csb.get_passage("Obadiah", 1)
        self.assertEqual(9, len(obadiah['verses']['Edom’s Certain Judgment']))

        matthew_1 = self.csb.get_passage("Matthew", 1)
        self.assertEqual(1, len(matthew_1['verses']['The Genealogy of Jesus Christ']))
        self.assertEqual(5, len(matthew_1['verses']['From Abraham to David']))
        self.assertEqual(6, len(matthew_1['verses']['From David to the Babylonian Exile']))

        # This is slow-ish
        for book in self.csb.books_of_the_bible:
            start = time.perf_counter()
            self.csb.get_passage(book, 1)
            end = time.perf_counter()
            print(f"Total time parsing {book}: {end - start}")
        with bz2.open("../bibles/json-bibles/csb.json.pbz2", "rt", encoding='utf-8') as cache_file:
            self.assertNotIn("<", cache_file.read())

    def test_close_to_kjv(self):
        """
        This test makes up for the sparseness above
        """
        for book, chapter_count in self.csb.books_of_the_bible.items():
            for chapter in range(1, chapter_count + 1):
                csb_passage = [
                    verse
                    for heading, verses in self.csb.get_passage(book, chapter)['verses'].items()
                    for verse in verses
                ]
                kjv_passage = self.kjv.get_passage(book, chapter)['verses']['none']
                message = f"\n{book} {chapter}"

                # These passages are special (due to headings) and require manual checking.
                # Also, Matthew 17, 18, 23; Mark 7, 9 (two), 11; Luke 17, 23;
                # John 5; Acts 8, 15, 24, 28; Romans 16; 2 Corinthians 13 are all
                # missing >= 1 verse(s) compared to the KJV.
                # 3 John 1 and Revelation 12 have an extra verse in the CSB

                if f"{book} {chapter}" in [
                    "Numbers 28", "1 Samuel 4", "1 Samuel 14", "2 Samuel 12", "1 Kings 7",
                    "1 Kings 19", "2 Kings 2", "2 Kings 5", "1 Chronicles 29", "2 Chronicles 4",
                    "Nehemiah 1", "Nehemiah 7", "Ezekiel 41", "Daniel 11", "Matthew 1",
                    "Matthew 17", "Matthew 18", "Matthew 23", "Mark 7", "Mark 9", "Mark 11",
                    "Luke 9", "Luke 17", "Luke 23", "John 5", "John 18", "John 19", "Acts 5",
                    "Acts 8", "Acts 9", "Acts 15", "Acts 24", "Acts 28", "Romans 16",
                    "2 Corinthians 13", "1 Timothy 6", "3 John 1", "Revelation 12"
                ]:
                    continue
                # Check verse count first
                self.assertEqual(len(kjv_passage), len(csb_passage), msg=message)

                # Check for missing parts, with high delta due to (textual) rendering
                # differences of the translations
                for kjv_verse, csb_verse in zip(kjv_passage, csb_passage):
                    # These verses are rendered significantly shorter in the CSB and are manually
                    # verified
                    # pylint: disable=invalid-character-zero-width-space
                    if csb_verse in [
                        "22 Those registered, counting every male one month old or more, numbered "
                        "7,500. ",
                        "1 When all the Amorite kings across the Jordan to the west and all the "
                        "Canaanite kings near the sea heard how the Lord had dried up the water "
                        "of the Jordan before the Israelites until they had crossed over, they "
                        "lost heart and their courage failed because of the Israelites. ",
                        "2 So the allotment was for the rest of Manasseh’s descendants by their "
                        "clans, for the sons of Abiezer, Helek, Asriel, Shechem, Hepher, and "
                        "Shemida. These are the male descendants of Manasseh son of Joseph, by "
                        "their clans. ",
                        "9 The Reubenites, Gadites, and half the tribe of Manasseh left the "
                        "Israelites at Shiloh in the land of Canaan to return to their own land "
                        "of Gilead, which they took possession of according to the Lord’s command "
                        "through Moses. ",
                        "2 so he told him, “My father, Saul, intends to kill you. Be on your "
                        "guard in the morning and hide in a secret place and stay there. ",
                        "13 But one of his servants responded, “Please, let messengers take five "
                        "of the horses that are left in the city. Their fate is like the entire "
                        "Israelite community who will die, so let’s send them and see.” ",
                        "4 Then Joash said to the priests, “All the dedicated silver brought to "
                        "the Lord’s temple, census silver, silver from vows, and all silver "
                        "voluntarily given for the Lord’s temple ​— ​ ",
                        "9 On the twenty-third day of the third month ​— ​that is, the month "
                        "Sivan ​— ​ the royal scribes were summoned. Everything was "
                        "written exactly as Mordecai commanded for the Jews, to the satraps, the "
                        "governors, and the officials of the 127 provinces from India to Cush. "
                        "The edict was written for each province in its own script, for each "
                        "ethnic group in its own language, and to the Jews in their own script "
                        "and language. ",
                        "2 people and priest alike, servant and master, female servant and "
                        "mistress, buyer and seller, lender and borrower, creditor and debtor. ",
                        "24 Then all the trees of the field will know that I am the Lord. I "
                        "bring down the tall tree, and make the low tree tall. I cause the green "
                        "tree to wither and make the withered tree thrive. I, the Lord, have "
                        "spoken and I will do it.’ ” ",
                        "4 You have not strengthened the weak, healed the sick, bandaged the "
                        "injured, brought back the strays, or sought the lost. Instead, you have "
                        "ruled them with violence and cruelty. ",
                        "1 “When you divide the land by lot as an inheritance, set aside a "
                        "donation to the Lord, a holy portion of the land, 8 1/3 miles long "
                        "and 6 2/3 miles wide. This entire region will be holy. ",
                        "35 After crucifying him, they divided his clothes by casting lots. ",
                        "11 If any place does not welcome you or listen to you, when you leave "
                        "there, shake the dust off your feet as a testimony against them.” ",
                        "11 saying,“Write on a scroll what you see and send it to the seven "
                        "churches: Ephesus, Smyrna, Pergamum, Thyatira, Sardis, Philadelphia, "
                        "and Laodicea.” "
                    ]:
                        continue
                    self.assertAlmostEqual(
                        len(kjv_verse),
                        len(csb_verse),
                        delta=100, msg=message + f"\nCSB: {csb_verse}\nKJV: {kjv_verse}"
                    )
