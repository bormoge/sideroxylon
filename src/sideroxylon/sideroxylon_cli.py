import argparse
import os
import sys
from typing import cast

from .sideroxylon_main import SideroxylonMain
from .sideroxylon_xdg import sideroxylon_xdg_object


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="sideroxylon",
        description="sideroxylon CLI",
    )

    parser.add_argument(
        "urls",
        nargs="?",
        default="",
        help="Directly pass the URLs to sideroxylon. Note that URLs should be separated by a newline character.",
    )

    parser.add_argument(
        "--config-file",
        default=f"{sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR}/config.json",
        help="Path to the config.json file.",
    )

    parser.add_argument(
        "--env-file",
        default=f"{sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR}/.env",
        help="Path to the dotenv (.env) file.",
    )

    parser.add_argument(
        "--repository-url-file",
        default=f"{sideroxylon_xdg_object.SIDEROXYLON_DATA_HOME_DIR}/repository_urls.org",
        help="Path to the file that contains the repository URLs file.",
    )

    parser.add_argument(
        "--filtered-urls-file",
        default=f"{sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR}/filtered_urls.org",
        help="Path to the file that contains keywords (substrings) used to filter undesired URLs.",
    )

    parser.add_argument(
        "--sorted-repositories-directory",
        default=f"{sideroxylon_xdg_object.SIDEROXYLON_DATA_HOME_DIR}/sorted_repositories/",
        help="Path to the directory where the URLs will be stored.",
    )

    parser.add_argument(
        "--file-extension",
        default="org",
        help="File extension for files generated inside sorted_repositories_directory.",
    )

    parser.add_argument(
        "--sleep-time",
        default=2.0,
        help="Seconds to wait until the next API call.",
    )

    parser.add_argument(
        "--verbose",
        default=1,
        help=(
            "Define how descriptive you want sideroxylon to be."
            "\nZero (0) is non-descriptive."
            "\nOne (1) is minimally descriptive."
            "\nTwo (2) is fully descriptive."
        ),
    )

    args = parser.parse_args()

    arg_urls: str = get_all_urls_from_pipes_and_urls_arg(args)

    try:
        sid: SideroxylonMain = SideroxylonMain()
        sid.sideroxylon(
            # File that contains the configuration values.
            config_file=args.config_file,
            # File that contains the environment variables.
            env_file=args.env_file,
            # File that contains the repository urls.
            repository_url_file=args.repository_url_file,
            # File that contains the filtered urls.
            filtered_urls_file=args.filtered_urls_file,
            # Directory with all the repository URLs already sorted.
            sorted_repositories_directory=args.sorted_repositories_directory,
            # File extension for files generated inside sorted_repositories_directory.
            file_extension=args.file_extension,
            # Seconds to wait until the next API call.
            sleep_time=args.sleep_time,
            # Verbose modes.
            verbose=args.verbose,
            # String that contains URLs passed by the user as
            # a positional argument and/or pipe output.
            arg_urls=arg_urls,
        )

    except KeyboardInterrupt:
        sys.exit("\nsideroxylon terminated by user.")


def get_all_urls_from_pipes_and_urls_arg(args) -> str:
    piped_urls: str = ""
    arg_urls: str = ""

    if not sys.stdin.isatty():
        piped_urls: str = cast(str, sys.stdin.read())

    arg_urls: str = piped_urls + args.urls
    arg_urls: str = os.linesep.join([s for s in arg_urls.splitlines() if s])

    return arg_urls


if __name__ == "__main__":
    main()
