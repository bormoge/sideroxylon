from typing import Any
from .sideroxylon_forge import SideroxylonForge

class SideroxylonSourceHut(SideroxylonForge):

    def fetch_forge_repository_data(
        self, api_url: str
    ) -> dict[str, Any] | None:
        """
        This is a dummy function that returns 'None'.
        """

        return None

    def get_repository_programming_language(
        self, repository_url: str
    ) -> str | Any:
        """
        This is a dummy function that returns 'SourceHut'
        """

        # The thing is, as far as I saw their API offered no way of getting the
        # main programming language of a repository.  Basically, we just have to
        # wait until / if they implement it.

        return "SourceHut"

    def get_forge_name(self):
        """
        This is a dummy function that returns "SourceHut".
        """

        return "SourceHut"

    def __init__(self, token_file: str):
        pass
