import time
import os
import sys
import typer
from typing import Annotated
from typing import Any
from pathlib import Path
from dataclasses import dataclass
from urllib.parse import urlparse
from .sideroxylon_forge import SideroxylonForge
from .sideroxylon_github import SideroxylonGitHub
from .sideroxylon_unknown_forge import SideroxylonUnknownForge
from .sideroxylon_sourcehut import SideroxylonSourceHut


@dataclass
class SideroxylonArgs:
    """
    Dataclass that contains all the arguments of sideroxylon.
    """

    env_file: str
    repository_url_file: str
    languages_directory: str
    file_extension: str
    sleep_time: float


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
        with open(env_file, "r") as file:
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

    except PermissionError as p:
        sys.exit(f"You do not have the necessary permissions to read this file: {p}")

    except OSError as e:
        print(f"Error reading {env_file}: {e}")


def assign_sideroxylon_variables(args_list: list) -> SideroxylonArgs:
    """
    Assign values to the arguments depending on whether the user
    explicitly passed them or if they exist as environment variables.
    If sideroxylon finds neither arguments nor environment variables,
    a default value is used.
    """

    # If equal to default, it may or may not mean the user skipped the flag, so the default value is being used.
    # Before assigning defaults, sideroxylon checks other sources where values could be found (ex. a dotenv file).

    if args_list[0] == f"{SIDEROXYLON_DATA_HOME_DIR}/repository_urls.org":
        args_list[0] = (
            # This may seem redundant, but keep in mind environment variables can be set even before running sideroxylon
            os.path.expanduser(os.environ.get("SIDEROXYLON_ENV_FILE", ""))
            or args_list[0]
        )
    if args_list[1] == f"{SIDEROXYLON_DATA_HOME_DIR}/repository_urls.org":
        args_list[1] = (
            os.path.expanduser(os.environ.get("SIDEROXYLON_REPOSITORY_URL_FILE", ""))
            or args_list[1]
        )
    if args_list[2] == f"{SIDEROXYLON_DATA_HOME_DIR}/languages/":
        args_list[2] = (
            os.path.expanduser(os.environ.get("SIDEROXYLON_LANGUAGES_DIRECTORY", ""))
            or args_list[2]
        )
    if args_list[3] == "org":
        args_list[3] = (
            os.path.expanduser(os.environ.get("SIDEROXYLON_FILE_EXTENSION", ""))
            or args_list[3]
        )
    if args_list[4] == 2.0:
        args_list[4] = (
            check_if_float(
                os.path.expanduser(os.environ.get("SIDEROXYLON_SLEEP_TIME", ""))
            )
            or args_list[4]
        )

    return SideroxylonArgs(*args_list)


def check_if_float(float_num: str | float) -> float | None:
    """
    Check if the parameter passed is a float or can be converted to float.
    """

    try:
        if float_num == "" or float_num is None:
            return None
        else:
            return float(float_num)

    except (TypeError, ValueError):
        print("Error: Not a float. Falling back to argument value.")
        return None


def check_if_boolean(bool_value: str | bool) -> bool:
    """
    Check if the parameter passed is a boolean or can be converted to boolean.
    """

    return bool_value is True or str(bool_value).lower() == "true"


def get_urls_inside_repository_url_file(repository_url_file: str) -> list[str]:
    """
    Read URLs inside repository_url_file.
    """

    try:
        with open(repository_url_file, "r") as file:
            urls: list[str] = [line.strip() for line in file if line.strip()]

    except PermissionError as p:
        sys.exit(f"You do not have the necessary permissions to read this file: {p}")

    except OSError as e:
        print(f"Error reading {repository_url_file}: {e}")
        return []

    return urls


def store_batches_in_memory(full_path_filename: str, url: str, repository_url_dict: dict[str, list[str]]) -> None:
    """
    Store the URL inside the dictionary REPOSITORY_URL_DICT.
    """

    if full_path_filename not in repository_url_dict:
        repository_url_dict[full_path_filename] = []

    repository_url_dict[full_path_filename].append(url)


def write_batches_into_files(repository_url_dict: dict[str, list[str]]) -> None:
    """
    Write all the URLs in their respective files.
    """

    try:
        for key, value in repository_url_dict.items():
            with open(key, "a") as file:
                file.write("\n".join(value) + "\n")

    except PermissionError as p:
        sys.exit(
            f"You do not have the necessary permissions to write in this file: {p}"
        )

    except OSError as e:
        print(f"Error reading {key}: {e}")
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


def delay_api_calls(sleep_time: float) -> None:
    """
    Put a delay on the amount of times the API is called.
    """

    # This puts a delay on the amount of times the API is called.
    time.sleep(sleep_time)


def print_sideroxylon_output(url: str, language: str) -> None:
    """
    Print the repository URL and the main programming language of said repository.
    """

    print(f"{url} -> {language}")


def clean_programming_language_name(language: str) -> str:
    """
    Clean the provided programming language name, replacing
    certain characters with new ones depending of the context.
    """

    language: str = language.replace(" ", "_")
    language: str = language.replace(".", "-")
    language: str = language.replace("'", "-")
    language: str = language.replace("#", "Sharp")
    language: str = language.replace("+", "P")

    # Note: decide whether to lowercase the names or deal with
    # discrepancies on a case-by-case basis.

    return language


def store_repository_urls_by_programming_language(
    repository_urls: list[str], sid_args: SideroxylonArgs
) -> None:
    """
    Store each repository URL in the file with the name of its main programming language.
    """

    forge_dict: dict[str, Any] = initialize_forge_dictionary()
    repository_url_dict: dict[str, list[str]] = {}

    current_line_number: int = 0

    for url in repository_urls:

        url: str = basic_url_cleaning(url)

        forge_object: SideroxylonForge = get_repository_url_forge_object(
            forge_dict, url
        )

        # If necessary, convert the URL to an api URL.
        api_url: str | None = forge_object.convert_forge_url_to_api_url(url)

        if not api_url:
            current_line_number += 1
            print(f"Skipping {url}")
            continue

        # From api_url, fetch the necessary data to get the programming language.
        fetched_data: dict[str, Any] | None = forge_object.fetch_forge_repository_data(api_url)

        language_name: str = forge_object.get_repository_programming_language(api_url, fetched_data)

        cleaned_language_name: str = clean_programming_language_name(language_name)

        filename: str = f"{cleaned_language_name}.{sid_args.file_extension}"

        full_path_filename: str = os.path.join(sid_args.languages_directory, filename)

        cleaned_url: str = forge_object.clean_forge_repository_url(url)

        store_batches_in_memory(full_path_filename, cleaned_url, repository_url_dict)

        print_sideroxylon_output(cleaned_url, cleaned_language_name)

        delay_api_calls(sid_args.sleep_time)

    # Outside of loop.
    write_batches_into_files(repository_url_dict)


def initialize_directories_and_files(
    directories_and_files: dict[str, list[str]],
) -> None:
    """
    Initialize the directories and files that sideroxylon requires.
    """

    try:
        for directory in directories_and_files.get("directories", []):
            Path(directory).mkdir(parents=True, exist_ok=True)

    except PermissionError as p:
        sys.exit()(
            f"You do not have the necessary permissions to create directory {directory}: {p}"
        )

    except OSError as e:
        print(f"Error creating {directory}: {e}")
        return

    try:
        for file in directories_and_files.get("files", []):
            Path(file).touch(exist_ok=True)

    except PermissionError as p:
        sys.exit(
            f"You do not have the necessary permissions to create file {file}: {p}"
        )

    except OSError as e:
        print(f"Error creating {file}: {e}")


def clean_repository_url_file(repository_url_file: str) -> None:
    """
    Clean the file with the repository URLs.
    """

    try:
        open(repository_url_file, "w").close()

    except PermissionError as p:
        sys.exit(
            f"You do not have the necessary permissions to write in this file: {p}"
        )

    except OSError as e:
        print(f"Error reading {repository_url_file}: {e}")
        return


def sideroxylon_workflow(args_list: list) -> None:
    """
    Main function of sideroxylon.

    Its purpose is to define the workflow of the program and
    separate the cli entry point from the rest of the functions.

    It can be used as a replacement for the sideroxylon
    function, provided you pass a list with elements that serve as
    substitutes for the cli arguments.
    """

    load_sideroxylon_env_variables(args_list[0])

    # Arguments after processing.
    sid_args: SideroxylonArgs = assign_sideroxylon_variables(args_list)

    # Required directories and files.
    directories_and_files: dict[str, list[str]] = {
        "directories": [
            SIDEROXYLON_DATA_HOME_DIR,
            SIDEROXYLON_CONFIG_HOME_DIR,
            sid_args.languages_directory,
        ],
        "files": [sid_args.env_file, sid_args.repository_url_file],
    }

    initialize_directories_and_files(directories_and_files)

    # Get each link in the repository URL file
    repository_urls: list[str] = get_urls_inside_repository_url_file(
        sid_args.repository_url_file
    )

    # Store each URL in its corresponding file inside languages_directory
    store_repository_urls_by_programming_language(repository_urls, sid_args)

    # Clear the repository URL file after going through each link
    # At some point I will change this so at the beginning of the program it clears all files
    clean_repository_url_file(sid_args.repository_url_file)


def sideroxylon(
    # File that contains the environment variables.
    env_file: Annotated[
        str, typer.Option(help="Path to the dotenv (.env) file.")
    ] = f"{SIDEROXYLON_CONFIG_HOME_DIR}/.env",
    # File that contains the repository urls.
    repository_url_file: Annotated[
        str,
        typer.Option(help="Path to the file that contains the repository URLs file."),
    ] = f"{SIDEROXYLON_DATA_HOME_DIR}/repository_urls.org",
    # Directory with all the programming language files.
    languages_directory: Annotated[
        str, typer.Option(help="Path to the directory where the URLs are stored.")
    ] = f"{SIDEROXYLON_DATA_HOME_DIR}/languages/",
    # File extension for languages_directory generated files.
    file_extension: Annotated[
        str,
        typer.Option(
            help="File extension for files generated inside languages-directory."
        ),
    ] = "org",
    # Seconds to wait until the next API call.
    sleep_time: Annotated[
        float, typer.Option(help="Seconds to wait until the next API call.")
    ] = 2.0,
) -> None:
    """
    Entry point of the sideroxylon CLI.
    """

    # Arguments before processing.
    args_list: list = [
        env_file,
        repository_url_file,
        languages_directory,
        file_extension,
        sleep_time,
    ]

    sideroxylon_workflow(args_list)


if __name__ == "__main__":
    sideroxylon()
