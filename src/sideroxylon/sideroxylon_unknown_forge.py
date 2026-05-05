import requests
from typing import Any
from .sideroxylon_forge import SideroxylonForge


class SideroxylonUnknownForge(SideroxylonForge):

    def convert_forge_url_to_api_url(self, repository_url: str) -> str | None:
        """
        This is a dummy function that returns repository_url.
        """

        return repository_url

    def fetch_forge_repository_data(self, api_url: str) -> requests.models.Response | None:
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
        self, api_url: str, fetched_data: dict[str, Any] | None
    ) -> str | Any:
        """
        This is a dummy function that returns 'Unknown'
        """

        return "Unknown"

    def get_forge_name(self) -> str:
        """
        This is a dummy function that returns "Unknown".
        """

        return "Unknown"

    def __init__(self):
        pass
