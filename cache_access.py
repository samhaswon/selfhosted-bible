from multipledispatch import dispatch
from pymongo.errors import ServerSelectionTimeoutError
from passage import Passage
import pymongo


class CacheAccess(object):
    """
    A more robust, persistent cache of the ESV API
    """
    @dispatch(str, str, str)
    def __init__(self, uri: str, db: str, col: str):
        self.__mongoClient = pymongo.MongoClient(uri)
        self.__collection = self.__mongoClient[db][col]
        self.__passage = Passage(open("api-key.txt", "r").read())

    @dispatch()
    def __init__(self):
        self.__mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.__collection = self.__mongoClient["ESV"]["Cached"]
        self.__passage = Passage(open("api-key.txt", "r").read())

    @dispatch(str, str)
    def get_chapter(self, book: str, chapter: str) -> dict:
        try:
            # Get passage from DB
            passage = self.__collection.find_one({'book': book, 'chapter': chapter})
            if passage:
                # Passage was cached
                return dict(passage)
            else:
                # Passage was not cached, so add it to the DB
                passage = self.__passage.get_chapter_esv_json(book + " " + chapter)
                if passage is not ("API Overloaded",
                                   {"try again later": "If this keeps happening, the app could be heavily throttled"}, ""):
                    self.add_chapter(passage)
                return passage
        except ServerSelectionTimeoutError:
            # Assuming the server is down, don't try to add to the DB
            return self.__passage.get_chapter_esv_json(book + " " + chapter)

    @dispatch(str, int)
    def get_chapter(self, book: str, chapter: int) -> dict:
        try:
            # Get passage from DB
            passage = self.__collection.find_one({'book': book, 'chapter': chapter})
            if passage:
                # Passage was cached
                return dict(passage)
            else:
                # Passage was not cached, so add it to the DB
                passage = self.__passage.get_chapter_esv_json(book + " " + str(chapter))
                self.add_chapter(passage)
                return passage
        except ServerSelectionTimeoutError:
            # Assuming the server is down, don't try to add to the DB
            return self.__passage.get_chapter_esv_json(book + " " + str(chapter))

    def add_chapter(self, chapter: dict) -> bool:
        """
        Returns true if a chapter was added successfully
        :param chapter:
        :return: bool
        """
        return self.__collection.insert_one(chapter).acknowledged
