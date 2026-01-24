"""
Passage exceptions
"""
class PassageNotFound(Exception):
    """
    Exception to be thrown whenever a query results in a passage not being found
    """

    def __init__(self, verse: str) -> None:
        super().__init__(str)
        self.__verse = verse

    def __str__(self) -> str:
        return f"Passage not found {self.__verse}"


class PassageInvalid(Exception):
    """
    Exception to be thrown whenever a query results in a passage that does not exist
    """

    def __init__(self, verse: str) -> None:
        super().__init__(str)
        self.__verse = verse

    def __str__(self) -> str:
        return f"Passage Invalid {self.__verse}"
