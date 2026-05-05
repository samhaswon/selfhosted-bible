"""
NLT
"""
from bibles.bolls_bible import BollsBible


class NLT(BollsBible):
    """NLT"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an NLT passage
        """
        super().__init__(cache_name="nlt", api_name="NLT")
