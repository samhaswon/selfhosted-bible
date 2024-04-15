import unittest
from bibles import *


class MyTestCase(unittest.TestCase):
    def test_all(self):
        bibles = {
            'ACV': ACV(),
            'AKJV': AKJV(),
            'AMP': AMP(),
            'ASV': ASV(),
            'BBE': BBE(),
            'BSB': BSB(),
            'CSB': CSB(),
            'Darby': Darby(),
            'DRA': DRA(),
            'EBR': EBR(),
            'ESV': ESV(),
            'GNV': GNV(),
            'KJV': KJV(),
            'KJV 1611': KJV1611(),
            'LSV': LSV(),
            'MSG': MSG(),
            'NASB 1995': NASB1995(),
            'NET': NET(),
            'NIV 1984': NIV1984(),
            'NIV 2011': NIV2011(),
            'NKJV': NKJV(),
            'NLT': NLT(),
            'RSV': RSV(),
            'RWV': RWV(),
            'RNKJV': RNKJV(),
            'UKJV': UKJV(),
            'WEB': WEB(),
            'YLT': YLT()
        }

        for version in bibles.keys():
            for book in bibles[version].books_of_the_bible.keys():
                for chapter in range(1, bibles[version].books_of_the_bible[book] + 1):
                    passage_result = bibles[version].get_passage(book, chapter)['verses']
                    if version == 'ESV' and book == 'Song of Solomon':
                        continue
                    for heading in passage_result.keys():
                        # Tokenize each verse, adding its reference
                        for passage in passage_result[heading]:
                            self.assertTrue(len(passage) >= 1, msg=f"{version}; {book} {chapter}")


if __name__ == '__main__':
    unittest.main()
