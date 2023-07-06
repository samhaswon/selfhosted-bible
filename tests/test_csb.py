from unittest import TestCase
from bibles.csb import CSB
from bibles.kjv import KJV


class TestCSB(TestCase):
    def test_get_passage(self):
        self.csb = CSB()

        # start = time.perf_counter()
        genesis_1 = self.csb.get_passage("Genesis", 1)
        # print(f"Finished parsing Genesis in {time.perf_counter() - start} seconds")
        self.assertEqual(31, len(genesis_1['verses']['The Creation']))
        genesis_35 = self.csb.get_passage("Genesis", 35)
        self.assertEqual(15, len(genesis_35['verses']['Return to Bethel']))
        self.assertEqual(5, len(genesis_35['verses']['Rachel’s Death']))

        psalm_1 = self.csb.get_passage("Psalms", 1)
        self.assertEqual(6, len(psalm_1['verses']['The Two Ways']))
        psalm_2 = self.csb.get_passage("Psalms", 2)
        self.assertEqual(12, len(psalm_2['verses']['Coronation of the Son']))
        psalm_3 = self.csb.get_passage("Psalms", 3)
        self.assertEqual(8, len(psalm_3['verses']['Confidence in Troubled Times']))
        psalm_119 = self.csb.get_passage("Psalms", 119)
        self.assertEqual(176, len(psalm_119['verses']['Delight in God’s Word']))

        obadiah = self.csb.get_passage("Obadiah", 1)
        self.assertEqual(9, len(obadiah['verses']['Edom’s Certain Judgment']))

        matthew_1 = self.csb.get_passage("Matthew", 1)
        self.assertEqual(1, len(matthew_1['verses']['The Genealogy of Jesus Christ']))
        self.assertEqual(5, len(matthew_1['verses']['From Abraham to David']))
        self.assertEqual(6, len(matthew_1['verses']['From David to the Babylonian Exile']))

        # This is slow-ish
        for book in self.csb.books_of_the_bible.keys():
            self.csb.get_passage(book, 1)
        with open("../bibles/json_bibles/csb.json", "r") as cache_file:
            self.assertNotIn("<", cache_file.read())

    def test_close_to_kjv(self):
        """
        This test makes up for the sparseness above
        :return:
        """
        self.csb = CSB()
        self.kjv = KJV()
        for book, chapter_count in self.csb.books_of_the_bible.items():
            for chapter in range(1, chapter_count + 1):
                csb_passage = [verse
                               for heading, verses in self.csb.get_passage(book, chapter)['verses'].items()
                               for verse in verses]
                kjv_passage = self.kjv.get_passage(book, chapter)['verses']['none']
                message = f"\n{book} {chapter}"

                """ 
                These passages are special (due to headings) and require manual checking. Also, Matthew 17, 18, 23; 
                Mark 7, 9 (two), 11; Luke 17, 23; John 5; Acts 8, 15, 24, 28; Romans 16; 2 Corinthians 13 are all 
                missing >= 1 verse(s) compared to the KJV. 3 John 1 and Revelation 12 have an extra verse in the CSB
                """
                if f"{book} {chapter}" in ["Numbers 28", "1 Samuel 4", "1 Samuel 14", "2 Samuel 12", "1 Kings 7",
                                           "1 Kings 19", "2 Kings 2", "2 Kings 5", "1 Chronicles 29", "2 Chronicles 4",
                                           "Nehemiah 1", "Nehemiah 7", "Ezekiel 41", "Daniel 11", "Matthew 1",
                                           "Matthew 17", "Matthew 18", "Matthew 23", "Mark 7", "Mark 9", "Mark 11",
                                           "Luke 9", "Luke 17", "Luke 23", "John 5", "John 18", "John 19", "Acts 5",
                                           "Acts 8", "Acts 9", "Acts 15", "Acts 24", "Acts 28", "Romans 16",
                                           "2 Corinthians 13", "1 Timothy 6", "3 John 1", "Revelation 12"]:
                    continue
                # Check verse count first
                self.assertEqual(len(kjv_passage), len(csb_passage), msg=message)

                # Check for missing parts, with high delta due to (textual) rendering differences of the translations
                for kjv_verse, csb_verse in zip(kjv_passage, csb_passage):
                    if csb_verse in ["22 Those registered, counting every male one month old or more, numbered 7,500. ",
                                     "1 When all the Amorite kings across the Jordan to the west and all the Canaanite "
                                     "kings near the sea heard how the Lord had dried up the water of the Jordan before"
                                     " the Israelites until they had crossed over, they lost heart and their courage "
                                     "failed because of the Israelites. ",
                                     "2 So the allotment was for the rest of Manasseh’s descendants by their clans, for"
                                     " the sons of Abiezer, Helek, Asriel, Shechem, Hepher, and Shemida. These are the"
                                     " male descendants of Manasseh son of Joseph, by their clans. ",
                                     "9 The Reubenites, Gadites, and half the tribe of Manasseh left the Israelites at "
                                     "Shiloh in the land of Canaan to return to their own land of Gilead, which they "
                                     "took possession of according to the Lord’s command through Moses. "]:
                        continue
                    self.assertAlmostEqual(len(kjv_verse), len(csb_verse),
                                           delta=100, msg=message + f"\nCSB: {csb_verse} \nKJV: {kjv_verse}")