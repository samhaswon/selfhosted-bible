from unittest import TestCase
from passage import Passage


class TestPassage(TestCase):

    def setUp(self) -> None:
        self.passage = Passage(open("../api-key.txt", "r").read())

    def test_get_passage_esv(self):
        # Test single passages
        self.assertEqual(self.passage.get_passage_esv("John 11:35")[0], "[35] Jesus wept.")
        self.assertEqual(self.passage.get_passage_esv("jn11.35")[0], "[35] Jesus wept.")
        self.assertEqual(self.passage.get_passage_esv("43011035")[0], "[35] Jesus wept.")
        # Test multiple passage queries
        self.assertListEqual(self.passage.get_passage_esv("John1.1;Genesis1.1"), ["[1] In the beginning was the Word, "
                                                                                  "and the Word was with God, "
                                                                                  "and the Word was God.",
                                                                                  "[1] In the beginning, God created "
                                                                                  "the heavens and the earth."])
        self.assertEqual(self.passage.get_passage_esv("Psalm 117")[0], "[1] Praise the LORD, all nations!\n"
                                                                       "        Extol him, all peoples!\n"
                                                                       "    [2] For great is his steadfast love toward us,\n"
                                                                       "        and the faithfulness of the LORD endures forever.\n"
                                                                       "    Praise the LORD!")
