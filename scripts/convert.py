"""
Converts JSON from bolls.life (https://bolls.life/api/)
"""
import json
import re
from bibles.kjv import KJV
from bibles.compresscache import CompressCache

if __name__ == '__main__':
    FILENAME = "../RV2004.json"
    ABBREVIATION = "rv2004"
    tag_remover = re.compile(r'<.*?>')
    kjv_obj = KJV()
    bible = {
        book.name: {
            str(chapter): [] for chapter in range(1, book.chapter_count + 1)
        } for book in KJV().books
    }
    with open(FILENAME, "r", encoding="utf-8") as data_file:
        input_file = json.load(data_file)
    for verse in input_file:
        # No extra books or apocrypha, WEB version
        if (verse['book'] == 19 and verse['chapter'] == 151) or verse['book'] > 66:
            continue
        book_name = kjv_obj.books[verse['book'] - 1].name
        chapter = verse['chapter']
        verse_num = verse['verse']
        content = tag_remover.sub('', verse['text'])
        bible[book_name][str(chapter)].append(f"{verse_num} {content}")
    with open(FILENAME, "w", encoding="utf-8") as bible_save:
        json.dump(bible, bible_save)
    compress_cache = CompressCache(ABBREVIATION)
    compress_cache.save(bible)
