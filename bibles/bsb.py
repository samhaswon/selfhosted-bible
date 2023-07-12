from bibles.json_bible import JSONBible
from bibles.passage import PassageInvalid
import json


class BSB(JSONBible):
    def __init__(self) -> None:
        super().__init__()
        self.__bsb = self.read_file()

    def read_file(self) -> dict:
        try:
            with open("bibles/json_bibles/bsb.json", "r") as data_file:
                return json.load(data_file)
            # For testing:
        except FileNotFoundError:
            with open("../bibles/json_bibles/bsb.json", "r") as data_file:
                return json.load(data_file)

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Returns a dictionary (Format: {book: "", chapter: 0, verses: ["1 content..."]}) of the chapter
        :param book: Name of the book
        :param chapter: chapter number
        :return:
        """
        if super().has_passage(book, chapter):
            return {"book": book, "chapter": chapter, "verses": {'none': self.__bsb[book][str(chapter)]}}
        else:
            raise PassageInvalid
