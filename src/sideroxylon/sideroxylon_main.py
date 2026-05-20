import datetime
import json
import os
import sys
import time
from dataclasses import dataclass
from http.client import HTTPResponse
from pathlib import Path
from typing import Any, cast
from urllib.error import HTTPError
from urllib.parse import urlparse

from .sideroxylon_forge import SideroxylonForge
from .sideroxylon_github import SideroxylonGitHub
from .sideroxylon_sourcehut import SideroxylonSourceHut
from .sideroxylon_unknown_forge import SideroxylonUnknownForge
from .sideroxylon_xdg import sideroxylon_xdg_object


@dataclass
class SideroxylonMainArgs:
    """
    Dataclass that contains all the arguments of sideroxylon.
    """

    env_file: str
    repository_url_file: str
    filtered_urls_file: str
    languages_directory: str
    file_extension: str
    sleep_time: float
    verbose: int
    arg_urls: str


class SideroxylonMain:

    def load_sideroxylon_env_variables(self, env_file: str) -> None:
        """
        Export the environment variables found in env_file.
        """

        if not env_file.endswith(".env"):
            sys.exit(
                "The provided env_file does not have a .env extension. Exiting sideroxylon."
            )

        # Path(os.path.dirname(env_file)).mkdir(parents=True, exist_ok=True)
        # Path(env_file).touch(exist_ok=True)

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
            sys.exit(
                f"You do not have the necessary permissions to read {env_file}: {p}"
            )

        except OSError as e:
            print(f"Error reading {env_file}: {e}")

    def read_sideroxylon_config(self, config_file: str) -> dict:
        """
        Read the values inside the config.json file.
        """

        if not config_file.endswith(".json"):
            sys.exit(
                "The provided config_file does not have a .json extension. Exiting sideroxylon."
            )

        Path(os.path.dirname(config_file)).mkdir(parents=True, exist_ok=True)
        Path(config_file).touch(exist_ok=True)

        try:
            with open(config_file) as conf:
                return json.load(conf)

        except json.decoder.JSONDecodeError:
            print("No configuration found.\n")
            # print(f"Error reading {config_file}: {jsondecerr}")
            # print("Returning empty configuration.\n")
            return {}

    def assign_sideroxylon_variables(self, args_list: dict) -> SideroxylonMainArgs:
        """
        Assign values to the arguments depending on whether the user
        explicitly passed them or if they exist in a config.json file.
        If sideroxylon finds neither arguments nor a config.json file,
        a default value is used.
        """

        # Get the user's configuration from the config_file
        config_dict: dict = self.read_sideroxylon_config(args_list["config_file"])

        if (
            args_list["env_file"]
            == f"{sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR}/.env"
        ):
            args_list["env_file"] = os.path.expanduser(
                config_dict.get("env_file", args_list["env_file"])
            )

        if (
            args_list["repository_url_file"]
            == f"{sideroxylon_xdg_object.SIDEROXYLON_DATA_HOME_DIR}/repository_urls.org"
        ):
            args_list["repository_url_file"] = os.path.expanduser(
                config_dict.get("repository_url_file", args_list["repository_url_file"])
            )

        if (
            args_list["filtered_urls_file"]
            == f"{sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR}/filtered_urls.org"
        ):
            args_list["filtered_urls_file"] = os.path.expanduser(
                config_dict.get("filtered_urls_file", args_list["filtered_urls_file"])
            )

        if (
            args_list["languages_directory"]
            == f"{sideroxylon_xdg_object.SIDEROXYLON_DATA_HOME_DIR}/languages/"
        ):
            args_list["languages_directory"] = os.path.expanduser(
                config_dict.get("languages_directory", args_list["languages_directory"])
            )

        if args_list["file_extension"] == "org":
            args_list["file_extension"] = config_dict.get(
                "file_extension", args_list["file_extension"]
            )

        args_list["sleep_time"] = self.check_if_number(args_list["sleep_time"])
        if args_list["sleep_time"] == 2.0:
            args_list["sleep_time"] = self.check_if_number(
                config_dict.get("sleep_time", args_list["sleep_time"])
            )
        args_list["sleep_time"] = cast(float, args_list["sleep_time"])

        args_list["verbose"] = self.check_if_number(args_list["verbose"])
        if args_list["verbose"] == 1:
            args_list["verbose"] = self.check_if_number(
                config_dict.get("verbose", args_list["verbose"])
            )
        args_list["verbose"] = cast(int, args_list["verbose"])

        return SideroxylonMainArgs(
            args_list["env_file"],
            args_list["repository_url_file"],
            args_list["filtered_urls_file"],
            args_list["languages_directory"],
            args_list["file_extension"],
            args_list["sleep_time"],
            args_list["verbose"],
            args_list["arg_urls"],
        )

    def check_if_number(self, float_num: str | float) -> float | None:
        """
        Check if the parameter passed is a number (float) or can be converted to a number (float).
        """

        try:
            if float_num == "" or float_num is None:
                return None
            else:
                return float(float_num)

        except (TypeError, ValueError):
            sys.exit(f"sideroxylon expected a number, but received '{float_num}'")

    def check_if_boolean(self, bool_value: str | bool) -> bool:
        """
        Check if the parameter passed is a boolean or can be converted to boolean.
        """

        return bool_value is True or str(bool_value).lower() == "true"

    def get_urls_inside_repository_url_file(
        self, repository_url_file: str
    ) -> list[str]:
        """
        Read URLs inside repository_url_file.
        """

        try:
            with open(repository_url_file, "r") as file:
                urls: list[str] = [line.strip() for line in file if line.strip()]

        except PermissionError as p:
            sys.exit(
                f"You do not have the necessary permissions to read {repository_url_file}: {p}"
            )

        except OSError as e:
            print(f"Error reading {repository_url_file}: {e}")
            return []

        return urls

    def add_pipe_urls(self, repository_urls: list[str], arg_urls: str) -> list[str]:
        """
        Split the URLS found in arg_urls by newline and add them to repository_urls.
        """

        # Add any URLs found in the pipe to the repository_urls
        if not arg_urls == "":
            repository_urls: list[str] = repository_urls + arg_urls.split("\n")

        # Remove duplicate URLs
        repository_urls: list[str] = list(set(repository_urls))

        return repository_urls

    def read_filtered_urls_file(
        self, filtered_urls_file: str
    ) -> list[str]:
        """
        Read the filtered_urls_file and store any strings found in the filtered_urls list.
        """

        try:

            with open(filtered_urls_file, "r") as file:
                filtered_urls: list[str] = [line.strip() for line in file]

        except PermissionError as p:
            sys.exit(
                f"You do not have the necessary permissions to read {filtered_urls_file}: {p}"
            )

        except OSError as e:
            print(f"Error reading {filtered_urls_file}: {e}")
            return []

        return filtered_urls

    def filter_repository_urls(
            self, repository_urls: list[str], filtered_urls: list[str]
    ) -> list[str]:
        """
        Remove any URLs that contain a substring in the filtered_urls list.
        """

        modified_repository_urls: list[str] = [
            # Put the url in modified_repository_urls
            url
            for url in repository_urls
            # If the url doesn't contain any filtered url/keyword in it.
            if not any(filtered_url in url for filtered_url in filtered_urls)
        ]

        return modified_repository_urls

    def store_batches_in_memory(
        self,
        full_path_filename: str,
        url: str,
        repository_url_dict: dict[str, list[str]],
    ) -> None:
        """
        Store the URL inside the dictionary REPOSITORY_URL_DICT.
        """

        if full_path_filename not in repository_url_dict:
            repository_url_dict[full_path_filename] = []

        repository_url_dict[full_path_filename].append(url)

    def write_batches_into_files(
        self, repository_url_dict: dict[str, list[str]]
    ) -> None:
        """
        Write all the URLs in their respective files.
        """

        try:
            for key, value in repository_url_dict.items():
                with open(key, "a") as file:
                    file.write("\n".join(value) + "\n")

        except PermissionError as p:
            sys.exit(
                f"You do not have the necessary permissions to write in {key}: {p}"
            )

        except OSError as e:
            print(f"Error reading {key}: {e}")
            return

    def get_repository_url_forge_object(self, forge_dict, repository_url):
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

    def initialize_forge_dictionary(self) -> dict[str, Any]:
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

    def basic_url_cleaning(self, repository_url: str) -> str:
        """
        Return the provided URL after doing some basic cleaning.
        """

        # Each SideroxylonForge instance should do its
        # own cleaning; the main purpose of this function
        # is to avoid crashes related to URL names.

        repository_url: str = repository_url.split("?")[0]
        repository_url: str = repository_url.split("#")[0]

        return repository_url

    def delay_api_calls(self, sleep_time: float) -> None:
        """
        Put a delay on the amount of times the API is called.
        """

        # This puts a delay on the amount of times the API is called.
        time.sleep(sleep_time)

    def print_sideroxylon_output(
        self,
        url: str,
        language: str,
        current_line_number: int,
        response: HTTPResponse | HTTPError | None = None,
        forge_name: str = "GitHub",
        verbose: int = 1,
    ) -> None:
        """
        Print the repository URL and the main programming language of said repository.
        """

        if verbose >= 1:
            if language:
                print(f"URL: {url}")
                print(f"Programming Language: {language}")
            else:
                print(f"Skipping {url}")

            if verbose >= 2:
                print(f"Current line number: {current_line_number}")

            if response is not None and (verbose >= 2):
                print(
                    f"Current rate limit ({forge_name}): {dict(response.getheaders()).get("X-RateLimit-Remaining", -1)}"
                )
                print(
                    f"Rate limit reset date ({forge_name}): {datetime.datetime.fromtimestamp(int(dict(response.getheaders()).get("X-RateLimit-Reset", -1)))}"
                )
                print(f"Status code: {response.getcode()}")

            print()

    def clean_programming_language_name(self, language: str) -> str:
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

    def store_repository_url_by_programming_language(
        self,
        sid_args: SideroxylonMainArgs,
        forge_object: SideroxylonForge,
        response: HTTPResponse | HTTPError,
        repository_url_dict: dict[str, list[str]],
        current_line_number: int,
        url: str,
        api_url: str,
    ) -> int:
        """
        Store each repository URL in the file with the name of its main programming language.
        """

        language_name: str = forge_object.get_repository_programming_language(
            api_url,
            response,
        )

        cleaned_language_name: str = self.clean_programming_language_name(language_name)

        filename: str = f"{cleaned_language_name}.{sid_args.file_extension}"

        full_path_filename: str = os.path.join(sid_args.languages_directory, filename)

        cleaned_url: str = forge_object.clean_forge_repository_url(url)

        self.store_batches_in_memory(
            full_path_filename, cleaned_url, repository_url_dict
        )

        current_line_number += 1

        self.print_sideroxylon_output(
            cleaned_url,
            cleaned_language_name,
            current_line_number,
            response,
            forge_object.get_forge_name(),
            verbose=sid_args.verbose,
        )

        return current_line_number

    def handle_repository_urls(
        self, repository_urls: list[str], sid_args: SideroxylonMainArgs
    ) -> int:
        """
        Handle each repository URL according to the classification given by the user.
        """

        forge_dict: dict[str, Any] = self.initialize_forge_dictionary()
        repository_url_dict: dict[str, list[str]] = {}

        current_line_number: int = 0

        classification_function: Any = self.store_repository_url_by_programming_language

        for url in repository_urls:

            url: str = self.basic_url_cleaning(url)

            forge_object: SideroxylonForge = self.get_repository_url_forge_object(
                forge_dict, url
            )

            # If necessary, convert the URL to an api URL.
            api_url: str | None = forge_object.convert_forge_url_to_api_url(url)

            if not api_url:
                current_line_number += 1
                self.print_sideroxylon_output(
                    url, "", current_line_number, verbose=sid_args.verbose
                )
                continue

            # From api_url, fetch the necessary data to get the programming language.
            response: HTTPResponse | HTTPError | None = (
                forge_object.fetch_forge_repository_data(api_url)
            )

            current_line_number: int = classification_function(
                sid_args,
                forge_object,
                response,
                repository_url_dict,
                current_line_number,
                url,
                api_url,
            )

            # Note: this only stops the current iteration of sideroxylon.
            # I could probably create a hard cap that checks current UNIX
            # time vs the last fetched UNIX time or something similar.

            # Another thing to note: this condition activates with all
            # forges, disregarding any rate limits other than the
            # current forge's.

            if self.check_if_rate_limit_has_been_reached(response, forge_object):
                break

            self.delay_api_calls(sid_args.sleep_time)

        # Outside of loop.
        self.write_batches_into_files(repository_url_dict)

        return current_line_number

    def check_if_rate_limit_has_been_reached(
        self, response: HTTPResponse | HTTPError | None, forge_object: SideroxylonForge
    ) -> bool:
        """
        Check the remaining rate limit ('X-RateLimit-Remaining') element of an HTTP
        response.
        """

        if response is not None and (
            (int(dict(response.getheaders()).get("X-RateLimit-Remaining", -1)) <= 0)
            or response.getcode() == 403
        ):
            print(f"\nRate limit reached for {forge_object.get_forge_name()}")
            print("Exiting sideroxylon")
            return True

        return False

    def initialize_directories_and_files(
        self,
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

    def clean_repository_url_file(
        self,
        repository_url_file: str,
        repository_urls: list[str],
        final_list_position: int,
    ) -> None:
        """
        Clean the file with the repository URLs.
        """

        try:
            with open(repository_url_file, "w") as file:
                file.write("\n".join(repository_urls[final_list_position:]) + "\n")

        except PermissionError as p:
            sys.exit(
                f"You do not have the necessary permissions to write in {repository_url_file}: {p}"
            )

        except OSError as e:
            print(f"Error reading {repository_url_file}: {e}")
            return

    def sideroxylon(
        self,
        # File that contains the configuration values.
        config_file: str = f"{sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR}/config.json",
        # File that contains the environment variables.
        env_file: str = f"{sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR}/.env",
        # File that contains the repository urls.
        repository_url_file: str = f"{sideroxylon_xdg_object.SIDEROXYLON_DATA_HOME_DIR}/repository_urls.org",
        # File that contains the filtered urls.
        filtered_urls_file: str = f"{sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR}/filtered_urls.org",
        # Directory with all the programming language files.
        languages_directory: str = f"{sideroxylon_xdg_object.SIDEROXYLON_DATA_HOME_DIR}/languages/",
        # File extension for languages_directory generated files.
        file_extension: str = "org",
        # Seconds to wait until the next API call.
        sleep_time: float = 2.0,
        # Verbose modes.
        verbose: int = 1,
        # String that contains URLs passed by the user as
        # a positional argument and/or pipe output.
        arg_urls: str = "",
    ) -> None:
        """
        Main function of sideroxylon. Its purpose is to define
        the workflow of the program.
        """

        # Arguments before processing.
        args_list: dict = {
            "config_file": config_file,
            "env_file": env_file,
            "repository_url_file": repository_url_file,
            "filtered_urls_file": filtered_urls_file,
            "languages_directory": languages_directory,
            "file_extension": file_extension,
            "sleep_time": sleep_time,
            "verbose": verbose,
            "arg_urls": arg_urls,
        }

        # Arguments after processing.
        sid_args: SideroxylonMainArgs = self.assign_sideroxylon_variables(args_list)

        # Initialize required directories and files.
        directories_and_files: dict[str, list[str]] = {
            "directories": [
                sideroxylon_xdg_object.SIDEROXYLON_DATA_HOME_DIR,
                sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR,
                sideroxylon_xdg_object.SIDEROXYLON_CACHE_HOME_DIR,
                sid_args.languages_directory,
            ],
            "files": [sid_args.env_file, sid_args.repository_url_file, sid_args.filtered_urls_file],
        }

        self.initialize_directories_and_files(directories_and_files)

        # Load the keys.
        self.load_sideroxylon_env_variables(sid_args.env_file)

        # Get each link in the repository URL file
        repository_urls: list[str] = self.get_urls_inside_repository_url_file(
            sid_args.repository_url_file
        )

        # Combine all the URLs including those found in the pipeline
        repository_urls: list[str] = self.add_pipe_urls(
            repository_urls, sid_args.arg_urls
        )

        # Read the filtered_urls_file and store any strings found in the filtered_urls list
        filtered_urls: list[str] = self.read_filtered_urls_file(sid_args.filtered_urls_file)

        # Filter all the URLs that contain a substring found in filtered_url
        repository_urls: list[str] = self.filter_repository_urls(
            repository_urls, filtered_urls
        )

        # Store each URL in its corresponding file inside languages_directory
        final_list_position: int = self.handle_repository_urls(repository_urls, sid_args)

        # Clear the repository URL file after going through each link
        # At some point I will change this so at the beginning of the program it clears all files
        self.clean_repository_url_file(
            sid_args.repository_url_file, repository_urls, final_list_position
        )


# if __name__ == "__main__":
#     sideroxylon()
