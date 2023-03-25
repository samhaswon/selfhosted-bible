from bibles.json_bible import JSONBible
from bibles.passage import PassageInvalid
import json


class ASV(JSONBible):
    def __init__(self) -> None:
        super().__init__()
        self.__asv = self.read_file()

    def read_file(self) -> dict:
        with open("bibles/json_bibles/asv.json", "r") as data_file:
            return json.load(data_file)

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Returns a dictionary (Format: {book: "", chapter: 0, verses: ["1 content..."]}) of the chapter
        :param book: Name of the book
        :param chapter: chapter number
        :return:
        """
        if super().has_passage(book, chapter):
            return {"book": book, "chapter": chapter, "verses": {'none': self.__asv[book][str(chapter)]}}
        else:
            raise PassageInvalid


if __name__ == '__main__':
    """
    Only used for conversion of source text from @bibleapi on github: https://github.com/bibleapi/bibleapi-bibles-json
    """
    bible = {book.name: {chapter: [] for chapter in range(1, book.chapter_count + 1)} for book in ASV().books}
    with open("json_bibles/asv.json", "r") as data_file_c:
        verses = data_file_c.readlines()
        temp_json = [json.loads(verse) for verse in verses]
        for verse in temp_json:
            if verse['book_name'] != 'Acts of the Apostles':
                bible[verse['book_name']][verse['chapter']].append(str(verse['verse']) + ' ' + verse['text'])
            else:
                bible['Acts'][verse['chapter']].append(str(verse['verse']) + ' ' + verse['text'])
    with open("asv.json", "w") as bible_save:
        json.dump(bible, bible_save)
