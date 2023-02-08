#!/usr/bin/env python

from unittest import TestCase
from passage import Passage


class TestPassage(TestCase):

    def setUp(self) -> None:
        self.passage = Passage(open("../api-key.txt", "r").read())
        self.maxDiff = None

    def test_get_passage_esv(self):
        """
        Test material comes from the English Standard Version
        :return: None
        """
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
        self.assertEqual(self.passage.get_passage_esv("Psalm 117")[0],
                         "[1] Praise the LORD, all nations!\n"
                         "        Extol him, all peoples!\n"
                         "    [2] For great is his steadfast love toward us,\n"
                         "        and the faithfulness of the LORD endures forever.\n"
                         "    Praise the LORD!")

    def test_get_chapter_esv(self):
        """
        Test material comes from the English Standard Version
        :return: None
        """
        # Basic test for heading at the beginning
        self.assertTupleEqual(self.passage.get_chapter_esv("Psalm 117"),
                              ('Psalm 117',
                               {'The LORD’s Faithfulness Endures Forever':
                                    '    [1] Praise the LORD, all nations!\n'
                                    '        Extol him, all peoples!\n'
                                    '    [2] For great is his steadfast love toward us,\n'
                                    '        and the faithfulness of the LORD endures forever.\n'
                                    '    Praise the LORD!\n'}, ""))
        # Test of multiple headings
        self.assertTupleEqual(self.passage.get_chapter_esv("Philippians 3"),
                              ('Philippians 3',
                               {'Righteousness Through Faith in Christ':
                                    '  [1] Finally, my brothers,(1) rejoice in the Lord. To write the same things to '
                                    'you is no trouble to me and is safe for you.\n  [2] Look out for the dogs, '
                                    'look out for the evildoers, look out for those who mutilate the flesh. [3] For '
                                    'we are the circumcision, who worship by the Spirit of God(2) and glory in Christ '
                                    'Jesus and put no confidence in the flesh—[4] though I myself have reason for '
                                    'confidence in the flesh also. If anyone else thinks he has reason for confidence '
                                    'in the flesh, I have more: [5] circumcised on the eighth day, of the people of '
                                    'Israel, of the tribe of Benjamin, a Hebrew of Hebrews; as to the law, '
                                    'a Pharisee; [6] as to zeal, a persecutor of the church; as to righteousness '
                                    'under the law,(3) blameless. [7] But whatever gain I had, I counted as loss for '
                                    'the sake of Christ. [8] Indeed, I count everything as loss because of the '
                                    'surpassing worth of knowing Christ Jesus my Lord. For his sake I have suffered '
                                    'the loss of all things and count them as rubbish, in order that I may gain '
                                    'Christ [9] and be found in him, not having a righteousness of my own that comes '
                                    'from the law, but that which comes through faith in Christ, the righteousness '
                                    'from God that depends on faith—[10] that I may know him and the power of his '
                                    'resurrection, and may share his sufferings, becoming like him in his death, '
                                    '[11] that by any means possible I may attain the resurrection from the dead.\n',
                                'Straining Toward the Goal':
                                    '  [12] Not that I have already obtained this or am '
                                    'already perfect, but I press on to make it my own, '
                                    'because Christ Jesus has made me his own. [13] '
                                    'Brothers, I do not consider that I have made it my own. '
                                    'But one thing I do: forgetting what lies behind and '
                                    'straining forward to what lies ahead, [14] I press on '
                                    'toward the goal for the prize of the upward call of God '
                                    'in Christ Jesus. [15] Let those of us who are mature '
                                    'think this way, and if in anything you think otherwise, '
                                    'God will reveal that also to you. [16] Only let us hold '
                                    'true to what we have attained.\n  [17] Brothers, '
                                    'join in imitating me, and keep your eyes on those who '
                                    'walk according to the example you have in us. [18] For '
                                    'many, of whom I have often told you and now tell you '
                                    'even with tears, walk as enemies of the cross of '
                                    'Christ. [19] Their end is destruction, their god is '
                                    'their belly, and they glory in their shame, with minds '
                                    'set on earthly things. [20] But our citizenship is in '
                                    'heaven, and from it we await a Savior, the Lord Jesus '
                                    'Christ, [21] who will transform our lowly body to be '
                                    'like his glorious body, by the power that enables him '
                                    'even to subject all things to himself.\n'},
                               '(1) 3:1 Or *brothers and sisters*; also verses 13, 17\n(2) 3:3 Some manuscripts *God '
                               'in spirit*\n(3) 3:6 Greek *in the law*\n'))

    def test_get_chapter_esv_json(self):
        pass

    def test_parse_headings(self):
        """
        Test material comes from the English Standard Version
        :return: None
        """
        self.assertEqual(self.passage.parse_headings('The LORD’s Faithfulness Endures Forever\n\n'
                                                     '    [1] Praise the LORD, all nations!\n'
                                                     '        Extol him, all peoples!\n'
                                                     '    [2] For great is his steadfast love toward us,\n'
                                                     '        and the faithfulness of the LORD endures forever.\n'
                                                     '    Praise the LORD!\n    \n\n'),
                         {"The LORD’s Faithfulness Endures Forever":
                              "    [1] Praise the LORD, all nations!\n"
                              "        Extol him, all peoples!\n"
                              "    [2] For great is his steadfast love toward us,\n"
                              "        and the faithfulness of the LORD endures forever.\n"
                              "    Praise the LORD!\n"}
                         )

    def test_split_verses(self):
        self.assertEqual(self.passage.split_verses("[1] Praise the LORD, all nations!\n"
                                                   "        Extol him, all peoples!\n"
                                                   "    [2] For great is his steadfast love toward us,\n"
                                                   "        and the faithfulness of the LORD endures forever.\n"
                                                   "    Praise the LORD!"),
                         ["1 Praise the LORD, all nations!\n"
                          "        Extol him, all peoples!",
                          "2 For great is his steadfast love toward us,\n"
                          "        and the faithfulness of the LORD endures forever.\n"
                          "    Praise the LORD!"])
