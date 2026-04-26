import time
import os
import typer
from typing import Annotated
from typing import Any
from pathlib import Path
from urllib.parse import urlparse
from .sideroxylon_forge import SideroxylonForge
from .sideroxylon_github import SideroxylonGitHub
from .sideroxylon_unknown_forge import SideroxylonUnknownForge
from .sideroxylon_sourcehut import SideroxylonSourceHut

HOME_DIR: str = os.environ.get("HOME", os.path.expanduser("~"))
XDG_DATA_HOME_DIR: str = os.environ.get(
    "XDG_DATA_HOME", os.path.expanduser(f"{HOME_DIR}/.local/share")
)
XDG_CONFIG_HOME_DIR: str = os.environ.get(
    "XDG_CONFIG_HOME", os.path.expanduser(f"{HOME_DIR}/.config")
)
SIDEROXYLON_DATA_HOME_DIR: str = f"{XDG_DATA_HOME_DIR}/sideroxylon"
SIDEROXYLON_CONFIG_HOME_DIR: str = f"{XDG_CONFIG_HOME_DIR}/sideroxylon"


def load_sideroxylon_env_variables(env_file: str) -> None:
    """
    Export the environment variables found in env_file.
    """

    try:
        with open(env_file) as file:
            for line in file:
                line: str = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Split keys and values
                elif "=" in line:
                    key, value = line.split("=", 1)

                    # Remove quotes
                    value: str = value.strip().strip('"').strip("'")

                    os.environ[key.strip()] = value

    except OSError as e:
        print(f"Error reading {env_file}: {e}")


def assign_sideroxylon_variables(
    repository_url_file: str, languages_directory: str
) -> tuple[str, str]:
    """
    Assign values to repository_url_file and languages_directory
    depending on whether the value is passed using arguments or environment
    variables.
    If sideroxylon finds neither arguments nor environment variables,
    a default value is used.
    """

    repository_url_file: str = (
        repository_url_file
        or os.path.expanduser(os.environ.get("SIDEROXYLON_REPOSITORY_URL_FILE", ""))
        or f"{SIDEROXYLON_DATA_HOME_DIR}/repository_urls.org"
    )
    languages_directory: str = (
        languages_directory
        or os.path.expanduser(os.environ.get("SIDEROXYLON_LANGUAGES_DIRECTORY", ""))
        or f"{SIDEROXYLON_DATA_HOME_DIR}/languages/"
    )

    return repository_url_file, languages_directory


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
    """
    Write the URL in its corresponding file.
    """

    try:
        with open(full_path_filename, "a") as file:
            file.write(url + "\n")

    except OSError as e:
        print(f"Error reading {full_path_filename}: {e}")
        return


def get_repository_url_forge_object(forge_dict, repository_url):
    """
    Get the correct forge handler object according to the provided URL's domain.
    """

    # Parse the repository URL
    parsed: Any = urlparse(repository_url)
    base: str = f"{parsed.scheme}://{parsed.netloc}"

    # Loop through each key in forge_dict to compare the base URL
    for key in list(forge_dict.keys())[:-1]:  # Skip ["unknown": unknown_obj]
        if base == key:
            return forge_dict[key]

    # If there is no match, return a SideroxylonUnknownForge object.
    return forge_dict["unknown"]


def initialize_forge_dictionary() -> dict[str, Any]:
    """
    Initialize required objects from classes that inherited SideroxylonForge.
    """

    github_obj: SideroxylonGitHub = SideroxylonGitHub()
    sourcehut_obj: SideroxylonSourceHut = SideroxylonSourceHut()
    unknown_obj: SideroxylonUnknownForge = SideroxylonUnknownForge()

    forge_dict: dict[str, Any] = {
        "https://github.com": github_obj,
        # "https://gitlab.com": ,
        # "https://codeberg.org": ,
        "https://sr.ht": sourcehut_obj,
        "https://git.sr.ht": sourcehut_obj,
        "unknown": unknown_obj,
    }

    return forge_dict


def basic_url_cleaning(repository_url: str) -> str:
    """
    Return the provided URL after doing some basic cleaning.
    """

    # Each SideroxylonForge instance should do its
    # own cleaning; the main purpose of this function
    # is to avoid crashes related to URL names.

    repository_url: str = repository_url.split("?")[0]
    repository_url: str = repository_url.split("#")[0]

    return repository_url


def delay_api_calls(sleep_time: int) -> None:
    # This puts a delay on the amount of times the API is called.
    time.sleep(sleep_time)


def print_sideroxylon_output(url: str, language: str) -> None:
    print(f"{url} -> {language}")


def clean_programming_language_name(language: str) -> str:
    language: str = language.replace(" ", "_")
    language: str = language.replace(".", "-")
    language: str = language.replace("'", "-")
    language: str = language.replace("#", "Sharp")
    language: str = language.replace("+", "P")

    # Note: decide whether to lowercase the names or deal with
    # discrepancies on a case-by-case basis.

    return language


def store_repository_urls_in_corresponding_files(
    repository_urls: list[str],
    languages_directory: str,
    file_extension: str,
    sleep_time: int,
) -> None:
    """
    Store each repository URL in the file with the name of its main programming language.
    """

    forge_dict: dict[str, Any] = initialize_forge_dictionary()

    for url in repository_urls:

        url: str = basic_url_cleaning(url)

        forge_object: SideroxylonForge = get_repository_url_forge_object(
            forge_dict, url
        )

        language: str | Any = clean_programming_language_name(
            forge_object.get_repository_programming_language(url)
        )

        filename = f"{language}.{file_extension}"

        full_path_filename: str = os.path.join(languages_directory, filename)

        url: str = forge_object.clean_forge_repository_url(url)

        write_into_file(full_path_filename, url)

        print_sideroxylon_output(url, language)

        delay_api_calls(sleep_time)


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
    try:
        open(repository_url_file, "w").close()

    except OSError as e:
        print(f"Error reading {repository_url_file}: {e}")
        return


def sideroxylon(
    # File that contains the repository urls.
    repository_url_file: Annotated[
        str,
        typer.Option(help="Path to the file that contains the repository URLs file."),
    ] = "",
    # Directory with all the programming language files.
    languages_directory: Annotated[
        str, typer.Option(help="Path to the directory where the URLs are stored.")
    ] = "",
    # File that contains the environment variables.
    env_file: Annotated[
        str, typer.Option(help="Path to the dotenv (.env) file.")
    ] = f"{SIDEROXYLON_CONFIG_HOME_DIR}/.env",
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
    Entry point of the sideroxylon CLI.
    """

    load_sideroxylon_env_variables(env_file)

    repository_url_file, languages_directory = assign_sideroxylon_variables(
        repository_url_file, languages_directory
    )

    directories_and_files: dict[str, list[str]] = {
        "directories": [
            SIDEROXYLON_DATA_HOME_DIR,
            SIDEROXYLON_CONFIG_HOME_DIR,
            languages_directory,
        ],
        "files": [env_file, repository_url_file],
    }

    initialize_directories_and_files(directories_and_files)

    # Get each link in the repository URL file
    repository_urls: list[str] = get_urls_inside_repository_url_file(
        repository_url_file
    )

    # Store each URL in its corresponding file inside languages_directory
    store_repository_urls_in_corresponding_files(
        repository_urls, languages_directory, file_extension, sleep_time
    )

    # Clear the repository URL file after going through each link
    # At some point I will change this so at the beginning of the program it clears all files
    clean_repository_url_file(repository_url_file)


if __name__ == "__main__":
    sideroxylon()
