from .sideroxylon_forge import SideroxylonForge
from typing import Any
from typing import cast
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
from http.client import HTTPResponse
import os
import sys
import json
import ssl


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

    def clean_forge_repository_url(self, repository_url: str) -> str:
        """
        Clean the provided forge URL, leaving only the base URL, the user, and the repository name.
        """

        user_and_repo: dict[str, str] | None = cast(
            dict, self.get_forge_user_and_repository_name(repository_url)
        )

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

    def fetch_forge_repository_data(
        self, api_url: str
    ) -> HTTPResponse | HTTPError | None:
        """
        Fetch the necessary data from GitHub.
        """

        # Create a request.
        request: urllib.request.Request = urllib.request.Request(
            url=api_url, headers=self.assign_token_to_headers()
        )

        # Try to call the API.
        try:
            def_context: ssl.SSLContext = ssl.create_default_context()
            response: HTTPResponse = urllib.request.urlopen(url=request, context=def_context)
            return response

        except HTTPError as http_error:
            return http_error

        except URLError as url_error:
            sys.exit(f"URLError: {url_error}")

        except Exception as e:
            sys.exit(f"Error: {e}")

    def convert_response_to_dict(self, response: HTTPResponse) -> dict:
        """
        Convert an HTTP response into a dictionary.
        """
        response_bytes: bytes = response.read()
        response_dict: dict = json.loads(response_bytes.decode("utf-8"))

        return response_dict

    def get_repository_programming_language(
        self, api_url: str, response: HTTPResponse | HTTPError | None
    ) -> str | Any:
        """
        Get the main programming language of the provided repository URL.
        """

        # Check if response exists. If it doesn't, it means we know it's a GitHub
        # URL but it's not a repository.
        if response is None or isinstance(response, HTTPError):
            return "GitHub_URL"

        # Generate a dictionary using the response object.
        response_dict: dict = self.convert_response_to_dict(response)

        # If the dictionary generated is empty then we know there are no
        # programming languages in that repository.
        if (len(response_dict) == 0) or (response_dict == {}):
            return "No_Programming_Language"

        # Get the most used language in the repository.
        main_language: str | Any = max(response_dict, key=lambda k: response_dict[k])

        return main_language

    def get_forge_name(self) -> str:
        """
        Return the string "GitHub".
        """

        return "GitHub"

    def __init__(self):
        pass
