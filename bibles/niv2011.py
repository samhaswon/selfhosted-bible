"""
NIV (2011)
"""
from bibles.bolls_bible import BollsBible


class NIV2011(BollsBible):
    """NIV (2011)"""
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of a NIV (2011) passage
        """
        super().__init__(cache_name="niv2011", api_name="NIV2011")
