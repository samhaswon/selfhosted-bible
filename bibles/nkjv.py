"""
NKJV
"""
from bibles.bolls_bible import BollsBible

class NKJV(BollsBible):
    """NKJV"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an NKJV passage
        """
        super().__init__(cache_name="nkjv", api_name="NKJV")
