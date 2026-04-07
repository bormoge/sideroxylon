import requests
import time
import os
import typer
from typing import Annotated
from typing import Any
from pathlib import Path

HOME_DIR: str = os.environ.get("HOME", os.path.expanduser("~"))
XDG_DATA_HOME_DIR: str = os.environ.get(
    "XDG_DATA_HOME", os.path.expanduser(f"{HOME_DIR}/.local/share")
)
SIDEROXYLON_DIR: str = f"{XDG_DATA_HOME_DIR}/sideroxylon"


def initialize_directories_and_files(
    directories_and_files: dict[str, list[str]],
) -> None:
    """
    Initialize the directories and files that sideroxylon requires.
    """

    for directory in directories_and_files.get("directories", []):
        Path(directory).mkdir(parents=True, exist_ok=True)

    for file in directories_and_files.get("files", []):
        Path(file).touch(exist_ok=True)


def assign_token_to_headers(token_file: str) -> dict[str, Any]:
    """
    Get forge headers.
    """

    # Get contents of token file and store them on forge_token
    with open(token_file, "r") as file:
        forge_token: str = file.read().replace("\n", "")  # Example: 'ghp_xxx'

    # If it exists, pass token to forge
    forge_headers: dict[str, Any] = {}
    if forge_token:
        forge_headers["Authorization"] = f"token {forge_token}"

    return forge_headers


def convert_forge_url_to_api_url(repository_url: str) -> str:
    """
    Convert forge URL to forge API URL.
    """

    # Check if we are at the correct position of the URL, store user and
    # repository names, and return the converted URL
    parts: list[str] = repository_url.strip().split("/")

    if len(parts) < 5:
        return None

    user: str = parts[3]
    repo: str = parts[4]

    return f"https://api.github.com/repos/{user}/{repo}"


def get_urls_inside_repository_url_file(repository_url_file: str) -> list[str]:
    """
    Read URLs inside repository_url_file.
    """

    with open(repository_url_file, "r") as file:
        urls: list[str] = [line.strip() for line in file if line.strip()]

    return urls


def fetch_forge_repository_data(
    api_url: str, forge_headers: dict[str, Any]
) -> dict[str, Any] | None:
    """
    Fetch the necessary data from the forge.
    """

    # Try to use the token. If the token fails send the URL to Unknown.
    try:
        response: requests.models.Response = requests.get(
            url=api_url, headers=forge_headers
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
    repository_url: str, forge_headers: dict[str, Any]
) -> str:
    """
    Get the main programming language of the provided repository URL.
    """

    # Convert normal URL to api URL
    api_url: str = convert_forge_url_to_api_url(repository_url)

    # Check if api URL exists, and if not return Unknown
    if not api_url:
        return "Unknown"

    data: dict[str, Any] | None = fetch_forge_repository_data(api_url, forge_headers)

    if not data:
        return "Unknown"

    return (
        data.get("language") or "Unknown"
    )  # There is a change this 'or' may never be used.


def write_into_file(full_path_filename: str, url: str) -> None:
    with open(full_path_filename, "a") as file:
        file.write(url + "\n")


def store_repository_urls_in_corresponding_files(
    repository_urls: list[str],
    forge_headers: dict[str, Any],
    languages_directory: str,
    file_extension: str,
    sleep_time: int,
) -> None:
    """
    Store each repository URL in the file with the name of its main programming language.
    """
    for url in repository_urls:
        language: dict[str, Any] | str = get_repository_programming_language(
            url, forge_headers
        )

        filename = f"{language}.{file_extension}"  # Note: I might want to replace spaces with hyphens

        full_path_filename: str = os.path.join(languages_directory, filename)

        write_into_file(full_path_filename, url)

        print(f"{url} -> {language}")

        # This line is here to avoid hitting rate limits
        time.sleep(sleep_time)


def clean_repository_url_file(repository_url_file: str) -> None:
    """
    Clean the file with the repository URLs.
    """
    open(repository_url_file, "w").close()


def sideroxylon(
    # File that cotains the token.
    token_file: Annotated[
        str, typer.Option(help="Path to the forge token file.")
    ] = f"{SIDEROXYLON_DIR}/token.org",
    # File that contains the repository urls.
    repository_url_file: Annotated[
        str, typer.Option(help="Path to the repository URLs file.")
    ] = f"{SIDEROXYLON_DIR}/repository_urls.org",
    # Directory with all the programming language files.
    languages_directory: Annotated[
        str, typer.Option(help="Path to the directory where URLs are stored.")
    ] = f"{SIDEROXYLON_DIR}/languages/",
    # File extension for languages_directory generated files.
    file_extension: Annotated[
        str,
        typer.Option(
            help="File extension for files generated inside languages-directory."
        ),
    ] = "org",
    # Seconds to wait until the next API call.
    sleep_time: Annotated[
        int, typer.Option(help="Seconds to wait until the next API call.")
    ] = 2,
) -> None:
    """
    Entry point of the sideroxylon cli.
    """

    directories_and_files: dict[str, list[str]] = {
        "directories": [languages_directory],
        "files": [token_file, repository_url_file],
    }

    initialize_directories_and_files(directories_and_files)

    forge_headers: dict[str, Any] = assign_token_to_headers(token_file)

    # Get each link in the repository URL file
    repository_urls: list[str] = get_urls_inside_repository_url_file(
        repository_url_file
    )

    # Once we get the main programming language, put the link in a file with the
    # same name as the language
    store_repository_urls_in_corresponding_files(
        repository_urls, forge_headers, languages_directory, file_extension, sleep_time
    )

    # Clear the repository URL file after going through each link
    # At some point I will change this so at the beginning of the program it clears all files
    clean_repository_url_file(repository_url_file)


if __name__ == "__main__":
    sideroxylon()
