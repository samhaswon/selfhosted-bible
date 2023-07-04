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
        self.assertEqual(5, len(genesis_35['verses']['Rachel&#8217;s Death']))

        psalm_1 = self.csb.get_passage("Psalms", 1)
        self.assertEqual(6, len(psalm_1['verses']['The Two Ways']))
        psalm_2 = self.csb.get_passage("Psalms", 2)
        self.assertEqual(12, len(psalm_2['verses']['Coronation of the Son']))
        psalm_3 = self.csb.get_passage("Psalms", 3)
        self.assertEqual(8, len(psalm_3['verses']['Confidence in Troubled Times']))
        psalm_119 = self.csb.get_passage("Psalms", 119)
        self.assertEqual(176, len(psalm_119['verses']['Delight in God&#8217;s Word']))

        obadiah = self.csb.get_passage("Obadiah", 1)
        self.assertEqual(9, len(obadiah['verses']['Edom&#8217;s Certain Judgment']))

        matthew_1 = self.csb.get_passage("Matthew", 1)
        self.assertEqual(1, len(matthew_1['verses']['The Genealogy of Jesus Christ']))
        self.assertEqual(5, len(matthew_1['verses']['From Abraham to David']))

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
                message = f"{book} {chapter}"

                # Check verse count first
                self.assertEqual(len(kjv_passage), len(csb_passage), msg=message)

                # Check for missing parts
                for kjv_verse, csb_verse in zip(kjv_passage, csb_passage):
                    self.assertAlmostEqual(len(kjv_verse), len(csb_verse), delta=150, msg=message)