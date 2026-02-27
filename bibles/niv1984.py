"""
NIV (1984)
"""
from bibles.bolls_bible import BollsBible


class NIV1984(BollsBible):
    """NIV (1984)"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of a NIV (1984) passage
        """
        super().__init__(cache_name="niv1984", api_name="NIV")
