"""
Class for the BTX3
"""
from bibles.bolls_bible import BollsBible


class BTX3(BollsBible):
    """
    Class for the BTX3
    """
    def __init__(self) -> None:
        """
        Gets a JSON formatted dictionary of a La Biblia Textual 3ra Edicion passage.
        """
        super().__init__(cache_name="btx3", api_name="BTX3")
