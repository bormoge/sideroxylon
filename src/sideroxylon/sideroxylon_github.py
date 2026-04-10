from .sideroxylon_forge import SideroxylonForge
from typing import Any
import requests


class SideroxylonGitHub(SideroxylonForge):

    forge_headers: dict[str, Any] = {}

    def assign_token_to_headers(self, token_file) -> None:
        """
        Get forge headers.
        """

        # Get contents of token file and store them on forge_token
        try:
            with open(token_file, "r") as file:
                forge_token: str = file.read().replace("\n", "")  # Example: 'ghp_xxx'

        except OSError as e:
            print(f"Error reading {token_file}: {e}")
            return

        # If it exists, pass token to forge
        headers: dict[str, Any] = {}
        if forge_token:
            headers["Authorization"] = f"token {forge_token}"

        SideroxylonGitHub.forge_headers: dict[str, Any] = headers

    def get_forge_user_and_repository_name(self, repository_url: str) -> dict[str, str] | None:
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

        user_and_repo: dict[str, str] | None = self.get_forge_user_and_repository_name(repository_url)

        if user_and_repo is None:
            return None

        user: str = user_and_repo["user"]
        repo: str = user_and_repo["repo"]

        return f"https://github.com/{user}/{repo}"

    def convert_forge_url_to_api_url(self, repository_url: str) -> str | None:
        """
        Convert forge URL to forge API URL.
        """

        user_and_repo: dict[str, str] | None = self.get_forge_user_and_repository_name(repository_url)

        if user_and_repo is None:
            return None

        user: str = user_and_repo["user"]
        repo: str = user_and_repo["repo"]

        return f"https://api.github.com/repos/{user}/{repo}/languages"

    def fetch_forge_repository_data(
        self, api_url: str
    ) -> dict[str, Any] | None:
        """
        Fetch the necessary data from GitHub.
        """

        # Try to use the token.
        try:
            response: requests.models.Response = requests.get(
                url=api_url, headers=SideroxylonGitHub.forge_headers
            )

            if response.status_code != 200:
                print(f"Status code: {response.status_code}")

                # If there is no language then default to None
                return None

            return response.json()

        except Exception as e:
            # If there is an exception then default to None
            print(f"Error fetching {api_url}: {e}")
            return None

    def get_repository_programming_language(
        self, repository_url: str
    ) -> str:
        """
        Get the main programming language of the provided repository URL.
        """

        # Convert normal URL to api URL
        api_url: str | None = self.convert_forge_url_to_api_url(repository_url)

        # Check if api URL exists, and if not return Unknown
        if not api_url:
            return "Not_A_GitHub_Repository"

        data: dict[str, Any] | None = self.fetch_forge_repository_data(
            api_url
        )

        if (isinstance(data, dict) and ((len(data) == 0) or (data == {}))):
            return "No_Programming_Language"

        if not data:
            return "Not_A_GitHub_Repository"

        # Get the most used language in the repository.
        main_language: str | Any = max(data, key=lambda k: data[k])

        return (
            main_language or "Unknown"
        )  # There is a chance this 'or' may never be used.

    def get_forge_name(self):
        """
        Return the string "github".
        """

        return "GitHub"

    def __init__(self, token_file: str):
        self.assign_token_to_headers(token_file)
