import requests
from typing import Any
from urllib.parse import urlparse
from .sideroxylon_forge import SideroxylonForge


class SideroxylonSourceHut(SideroxylonForge):

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

    def get_forge_user_and_repository_name(
        self, repository_url: str
    ) -> dict[str, str] | None:
        """
        Get the user and repository name from the provided URL.
        """

        parts: list[str] = repository_url.strip().split("/")

        if len(parts) < 5:
            return None

        user: str = parts[3]
        repo: str = parts[4]

        return {"user": user, "repo": repo}

    def clean_forge_repository_url(self, repository_url: str) -> str | None:
        """
        Clean the provided forge URL, leaving only the base URL, the user, and the repository name.
        """

        user_and_repo: dict[str, str] | None = self.get_forge_user_and_repository_name(
            repository_url
        )

        if user_and_repo is None:
            return None

        user: str = user_and_repo["user"]
        repo: str = user_and_repo["repo"]
        base_url: Any = urlparse(repository_url).netloc

        return f"https://{base_url}/{user}/{repo}"

    def get_repository_programming_language(
        self, api_url: str, fetched_data: dict[str, Any] | None
    ) -> str | Any:
        """
        This is a dummy function that returns 'SourceHut'
        """

        # The thing is, as far as I saw their API offered no way of getting the
        # main programming language of a repository.  Basically, we just have to
        # wait until / if they implement it.

        return "SourceHut"

    def get_forge_name(self) -> str:
        """
        This is a dummy function that returns "SourceHut".
        """

        return "SourceHut"

    def __init__(self):
        pass
