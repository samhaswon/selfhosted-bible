"""
NASB 1995
"""
from bibles.bolls_bible import BollsBible

class NASB1995(BollsBible):
    """NASB 1995"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an NASB (1995) passage
        """
        super().__init__(cache_name="nasb1995", api_name="NASB")
