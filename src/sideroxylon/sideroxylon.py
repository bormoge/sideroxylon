from sideroxylon.sideroxylon_forge import SideroxylonForge
import time
import os
import typer
from typing import Annotated
from typing import Any
from pathlib import Path
from .sideroxylon_github import SideroxylonGitHub
from .sideroxylon_unknown_forge import SideroxylonUnknownForge
from .sideroxylon_sourcehut import SideroxylonSourceHut

HOME_DIR: str = os.environ.get("HOME", os.path.expanduser("~"))
XDG_DATA_HOME_DIR: str = os.environ.get(
    "XDG_DATA_HOME", os.path.expanduser(f"{HOME_DIR}/.local/share")
)
SIDEROXYLON_DIR: str = f"{XDG_DATA_HOME_DIR}/sideroxylon"

github_base_url = "https://github.com"
gitlab_base_url = "https://gitlab.com"
codeberg_base_url = "https://codeberg.org"
sourcehut_base_url_1 = "https://sr.ht"
sourcehut_base_url_2 = "https://git.sr.ht"


def get_urls_inside_repository_url_file(repository_url_file: str) -> list[str]:
    """
    Read URLs inside repository_url_file.
    """

    try:
        with open(repository_url_file, "r") as file:
            urls: list[str] = [line.strip() for line in file if line.strip()]

    except OSError as e:
        print(f"Error reading {repository_url_file}: {e}")
        return []

    return urls


def write_into_file(full_path_filename: str, url: str) -> None:
    try:
        with open(full_path_filename, "a") as file:
            file.write(url + "\n")

    except OSError as e:
        print(f"Error reading {full_path_filename}: {e}")
        return


def get_repository_url_forge(forge_dict, repository_url):
    if github_base_url in repository_url:
        return forge_dict[github_base_url]
    elif (sourcehut_base_url_1 in repository_url) or (sourcehut_base_url_2 in repository_url):
        return forge_dict[sourcehut_base_url_2]
    else:
        return forge_dict["unknown"]


def initialize_forge_dictionary(token_file: str) -> dict[str, Any]:
    """
    Initialize required objects from classes that inherited SideroxylonForge
    """

    forge_dict: dict[str, Any] = {
        github_base_url: SideroxylonGitHub(token_file),
        sourcehut_base_url_2: SideroxylonSourceHut(token_file),
        "unknown": SideroxylonUnknownForge(token_file)
    }

    return forge_dict


def store_repository_urls_in_corresponding_files(
    repository_urls: list[str],
    token_file: str,
    languages_directory: str,
    file_extension: str,
    sleep_time: int,
) -> None:
    """
    Store each repository URL in the file with the name of its main programming language.
    """

    forge_dict: dict[str, Any] = initialize_forge_dictionary(token_file)

    for url in repository_urls:
        forge_object: SideroxylonForge = get_repository_url_forge(forge_dict, url)

        language: str | Any = forge_object.get_repository_programming_language(url)

        filename = f"{language}.{file_extension}"  # Note: I might want to replace spaces with hyphens

        full_path_filename: str = os.path.join(languages_directory, filename)

        write_into_file(full_path_filename, url)

        print(f"{url} -> {language}")

        # This line is here to avoid hitting rate limits
        time.sleep(sleep_time)


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


def clean_repository_url_file(repository_url_file: str) -> None:
    """
    Clean the file with the repository URLs.
    """
    open(repository_url_file, "w").close()


def sideroxylon(
    # File that contains the token.
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

    # Get each link in the repository URL file
    repository_urls: list[str] = get_urls_inside_repository_url_file(
        repository_url_file
    )

    # Store each URL in its corresponding file inside languages_directory
    store_repository_urls_in_corresponding_files(
        repository_urls, token_file, languages_directory, file_extension, sleep_time
    )

    # Clear the repository URL file after going through each link
    # At some point I will change this so at the beginning of the program it clears all files
    clean_repository_url_file(repository_url_file)


if __name__ == "__main__":
    sideroxylon()
