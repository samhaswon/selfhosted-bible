"""
The Legacy Standard Bible (LSB)
"""
from bibles.bolls_bible import BollsBible

# pylint: disable=duplicate-code
class LSB(BollsBible):
    """LSB"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an LSB passage
        """
        super().__init__(cache_name="lsb", api_name="LSB")
