from .sideroxylon_forge import SideroxylonForge
from typing import Any
import requests
import os


class SideroxylonGitHub(SideroxylonForge):

    def assign_token_to_headers(self) -> dict[str, Any]:
        """
        Get forge headers.
        """

        # Get the GitHub token
        github_token: str = os.environ.get("SIDEROXYLON_GITHUB_TOKEN", "")

        # By default the headers are empty
        github_headers: dict[str, Any] = {}

        # If a token exists create the headers
        if github_token:
            github_headers["Authorization"] = f"token {github_token}"

        return github_headers

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

        return f"https://github.com/{user}/{repo}"

    def convert_forge_url_to_api_url(self, repository_url: str) -> str | None:
        """
        Convert forge URL to forge API URL.
        """

        user_and_repo: dict[str, str] | None = self.get_forge_user_and_repository_name(
            repository_url
        )

        if user_and_repo is None:
            return None

        user: str = user_and_repo["user"]
        repo: str = user_and_repo["repo"]

        return f"https://api.github.com/repos/{user}/{repo}/languages"

    def fetch_forge_repository_data(self, api_url: str) -> dict[str, Any] | None:
        """
        Fetch the necessary data from GitHub.
        """

        # Try to use the token.
        try:
            response: requests.models.Response = requests.get(
                url=api_url, headers=self.assign_token_to_headers()
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

    def get_repository_programming_language(self, repository_url: str) -> str:
        """
        Get the main programming language of the provided repository URL.
        """

        # Convert normal URL to api URL
        api_url: str | None = self.convert_forge_url_to_api_url(repository_url)

        # Check if api URL exists, and if not return Unknown
        if not api_url:
            return "GitHub_URL"

        data: dict[str, Any] | None = self.fetch_forge_repository_data(api_url)

        if isinstance(data, dict) and ((len(data) == 0) or (data == {})):
            return "No_Programming_Language"

        if not data:
            return "GitHub_URL"

        # Get the most used language in the repository.
        main_language: str | Any = max(data, key=lambda k: data[k])

        return (
            main_language or "Unknown"
        )  # There is a chance this 'or' may never be used.

    def get_forge_name(self):
        """
        Return the string "GitHub".
        """

        return "GitHub"

    def __init__(self):
        pass
