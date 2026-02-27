"""
Class for the AMP version
"""
from bibles.bolls_bible import BollsBible


class AMP(BollsBible):
    """
    Class for the AMP version
    """
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an AMP passage
        """
        super().__init__(cache_name="amp", api_name="AMP")
