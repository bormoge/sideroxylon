from typing import Any
from .sideroxylon_forge import SideroxylonForge

class SideroxylonUnknownForge(SideroxylonForge):

    def fetch_forge_repository_data(
        self, api_url: str
    ) -> dict[str, Any] | None:
        """
        This is a dummy function that returns 'None'.
        """

        return None

    def clean_forge_repository_url(self, repository_url: str) -> str | None:
        """
        This is a dummy function that returns repository_url.
        """
        return repository_url

    def get_repository_programming_language(
        self, repository_url: str
    ) -> str | Any:
        """
        This is a dummy function that returns 'Unknown'
        """

        return "Unknown"

    def get_forge_name(self):
        """
        This is a dummy function that returns "Unknown".
        """

        return "Unknown"

    def __init__(self):
        pass
