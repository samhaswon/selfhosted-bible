"""
MSG
"""
from bibles.bolls_bible import BollsBible

class MSG(BollsBible):
    """MSG"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of an MSG passage
        """
        super().__init__(cache_name="msg", api_name="MSG")
