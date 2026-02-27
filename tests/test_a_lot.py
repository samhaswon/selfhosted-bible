"""
Test a lot of queries
"""
import unittest
# pylint: disable=unused-wildcard-import
from bibles import *


class ManyBibleTest(unittest.TestCase):
    """
    Get ever chapter possible
    """
    def test_all(self):
        """Get passages from everything"""
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
            'ESV': ESV(debug=True),
            'GNV': GNV(),
            'KJV': KJV(),
            'KJV 1611': KJV1611(),
            'LSB': LSB(),
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
            'YLT': YLT(),
            'BTX3': BTX3(),
            'RV1960': RV1960(),
            'RV2004': RV2004(),
        }

        for version_string, version_object in bibles.items():
            for book in version_object.books_of_the_bible.keys():
                for chapter in range(1, version_object.books_of_the_bible[book] + 1):
                    passage_result = version_object.get_passage(book, chapter)['verses']
                    if version_string == 'ESV' and book == 'Song of Solomon':
                        continue
                    for heading in passage_result.keys():
                        # Tokenize each verse, adding its reference
                        for passage_r in passage_result[heading]:
                            self.assertTrue(
                                len(passage_r) >= 1,
                                msg=f"{version_string}; {book} {chapter}"
                            )


if __name__ == '__main__':
    unittest.main()
