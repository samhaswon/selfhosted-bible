#!/usr/bin/env python

from multipledispatch import dispatch
from pymongo.errors import ServerSelectionTimeoutError
import pymongo


class CacheAccess:
    @dispatch(str, str, str)
    def __init__(self, uri: str, db: str, col: str):
        self.__mongoClient = pymongo.MongoClient(uri)
        self.__myCollection = self.__mongoClient[db][col]

    @dispatch()
    def __init__(self):
        self.__mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.__myCollection = self.__mongoClient["ESV"]["Cached"]

    def get_chapter(self):
        pass
