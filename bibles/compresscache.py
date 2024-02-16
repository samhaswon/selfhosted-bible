import json
import bz2


class CompressCache(object):
    """
    For saving and loading compressed JSON of the Bible.
    """
    def __init__(self, name: str) -> None:
        """
        :param name: Name of the version to save (i.e. KJV)
        :returns: None
        """
        self.__name = name

    def save(self, data: dict) -> None:
        """
        Saves the given data with the given version name
        :param data:
        :return:
        """
        # Normal save
        try:
            with bz2.open(f"bibles/json-bibles/{self.__name}.json.pbz2", "wb") as data_file:
                data_file.write(json.dumps(data, separators=(',', ':')).encode('utf-8'))
        # Testing save
        except FileNotFoundError:
            with bz2.open(f"../bibles/json-bibles/{self.__name}.json.pbz2", "wb") as data_file:
                data_file.write(json.dumps(data, separators=(',', ':')).encode('utf-8'))

    def load(self) -> dict:
        """
        Loads the compressed JSON of the Bible
        :return: dictionary version of the loaded JSON
        """
        with bz2.open(f"bibles/json-bibles/{self.__name}.json.pbz2", "rt", encoding='utf-8') as data_file:
            return json.load(data_file)
