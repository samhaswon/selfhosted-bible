"""
RSV
"""
from bibles.bolls_bible import BollsBible


class RSV(BollsBible):
    """RSV"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an RSV passage
        """
        super().__init__(cache_name="rsv", api_name="RSV")
