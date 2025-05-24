"""
For saving and loading compressed JSON of the Bible.
"""
import bz2
import json
import os


class CompressCache:
    """
    For saving and loading compressed JSON of the Bible.
    """
    def __init__(self, name: str) -> None:
        """
        :param name: Name of the version to save (i.e. KJV)
        :returns: None
        """
        self.__name = name
        self.__base_path = os.path.dirname(os.path.abspath(__file__))

    def save(self, data: dict) -> None:
        """
        Saves the given data with the given version name.
        :param data: the Dictionary data to save.
        :return: None
        """
        with bz2.open(f"{self.__base_path}/json-bibles/{self.__name}.json.pbz2", "wb") as data_file:
            data_file.write(json.dumps(data, separators=(',', ':')).encode('utf-8'))


    def load(self) -> dict:
        """
        Loads the compressed JSON of the Bible.
        :return: The dictionary version of the loaded JSON
        """
        with bz2.open(
                f"{self.__base_path}/json-bibles/{self.__name}.json.pbz2",
                "rt",
                encoding='utf-8'
        ) as data_file:
            return json.load(data_file)
