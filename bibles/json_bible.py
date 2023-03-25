from bibles.bible import Bible
from abc import abstractmethod


class JSONBible(Bible):
    """
    Base class for Bibles in a JSON format
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def read_file(self) -> dict:
        """
        Reads the JSON file of the Bible
        :return: dictionary of the Bible
        """
        raise NotImplementedError
