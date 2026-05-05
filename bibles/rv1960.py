"""
RV 1960
"""
from bibles.bolls_bible import BollsBible


class RV1960(BollsBible):
    """RV 1960"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of a Reina-Valera (1960) passage
        """
        super().__init__(cache_name="rv1960", api_name="RV1960")
