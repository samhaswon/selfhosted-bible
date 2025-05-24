"""
Translation layer from established code to the bolls API
"""

rbooks = {
        1: 'Genesis', 2: 'Exodus', 3: 'Leviticus', 4: 'Numbers', 5: 'Deuteronomy', 6: 'Joshua',
        7: 'Judges', 8: 'Ruth', 9: '1 Samuel', 10: '2 Samuel', 11: '1 Kings', 12: '2 Kings',
        13: '1 Chronicles', 14: '2 Chronicles', 15: 'Ezra', 16: 'Nehemiah', 17: 'Esther',
        18: 'Job', 19: 'Psalms', 20: 'Proverbs', 21: 'Ecclesiastes', 22: 'Song of Solomon',
        23: 'Isaiah', 24: 'Jeremiah', 25: 'Lamentations', 26: 'Ezekiel', 27: 'Daniel', 28: 'Hosea',
        29: 'Joel', 30: 'Amos', 31: 'Obadiah', 32: 'Jonah', 33: 'Micah', 34: 'Nahum',
        35: 'Habakkuk', 36: 'Zephaniah', 37: 'Haggai', 38: 'Zechariah', 39: 'Malachi',
        40: 'Matthew', 41: 'Mark', 42: 'Luke', 43: 'John', 44: 'Acts', 45: 'Romans',
        46: '1 Corinthians', 47: '2 Corinthians', 48: 'Galatians', 49: 'Ephesians',
        50: 'Philippians', 51: 'Colossians', 52: '1 Thessalonians', 53: '2 Thessalonians',
        54: '1 Timothy', 55: '2 Timothy', 56: 'Titus', 57: 'Philemon', 58: 'Hebrews', 59: 'James',
        60: '1 Peter', 61: '2 Peter', 62: '1 John', 63: '2 John', 64: '3 John', 65: 'Jude',
        66: 'Revelation'
    }

books = {
        'Genesis': 1, 'Exodus': 2, 'Leviticus': 3, 'Numbers': 4, 'Deuteronomy': 5, 'Joshua': 6,
        'Judges': 7, 'Ruth': 8, '1 Samuel': 9, '2 Samuel': 10, '1 Kings': 11, '2 Kings': 12,
        '1 Chronicles': 13, '2 Chronicles': 14, 'Ezra': 15, 'Nehemiah': 16, 'Esther': 17,
        'Job': 18, 'Psalms': 19, 'Proverbs': 20, 'Ecclesiastes': 21, 'Song of Solomon': 22,
        'Isaiah': 23, 'Jeremiah': 24, 'Lamentations': 25, 'Ezekiel': 26, 'Daniel': 27, 'Hosea': 28,
        'Joel': 29, 'Amos': 30, 'Obadiah': 31, 'Jonah': 32, 'Micah': 33, 'Nahum': 34,
        'Habakkuk': 35, 'Zephaniah': 36, 'Haggai': 37, 'Zechariah': 38, 'Malachi': 39,
        'Matthew': 40, 'Mark': 41, 'Luke': 42, 'John': 43, 'Acts': 44, 'Romans': 45,
        '1 Corinthians': 46, '2 Corinthians': 47, 'Galatians': 48, 'Ephesians': 49,
        'Philippians': 50, 'Colossians': 51, '1 Thessalonians': 52, '2 Thessalonians': 53,
        '1 Timothy': 54, '2 Timothy': 55, 'Titus': 56, 'Philemon': 57, 'Hebrews': 58, 'James': 59,
        '1 Peter': 60, '2 Peter': 61, '1 John': 62, '2 John': 63, '3 John': 64, 'Jude': 65,
        'Revelation': 66
    }

def translate(book: str) -> int:
    """
    Get the (from 1) index of a book of the Bible.
    :param book: book name.
    :return: index of the book.
    """
    return books[book]

def rtranslate(book: int) -> str:
    """
    Gets the name of a book based on its index. Opposite of translate()
    :param book: index of book name to find.
    :return: book name.
    """
    return rbooks[book]
