import argparse
import os
import sys
import time
from typing import cast

from .sideroxylon_datasets import sideroxylon_default_args_object
from .sideroxylon_main import SideroxylonMain


def main() -> None:
    start_time: float = time.perf_counter()

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="sideroxylon",
        description="sideroxylon CLI",
    )

    parser.add_argument(
        "urls",
        nargs="?",
        default=sideroxylon_default_args_object.arg_urls,
        help="Directly pass the URLs to sideroxylon. Note that URLs should be separated by a newline character.",
    )

    parser.add_argument(
        "--config-file",
        default=sideroxylon_default_args_object.config_file,
        help="Path to the config.json file.",
    )

    parser.add_argument(
        "--env-file",
        default=sideroxylon_default_args_object.env_file,
        help="Path to the dotenv (.env) file.",
    )

    parser.add_argument(
        "--repository-url-file",
        default=sideroxylon_default_args_object.repository_url_file,
        help="Path to the file that contains the repository URLs file.",
    )

    parser.add_argument(
        "--filtered-urls-file",
        default=sideroxylon_default_args_object.filtered_urls_file,
        help="Path to the file that contains keywords (substrings) used to filter undesired URLs.",
    )

    parser.add_argument(
        "--sorted-repositories-directory",
        default=sideroxylon_default_args_object.sorted_repositories_directory,
        help="Path to the directory where the URLs will be stored.",
    )

    parser.add_argument(
        "--file-extension",
        default=sideroxylon_default_args_object.file_extension,
        help="File extension for files generated inside sorted_repositories_directory.",
    )

    parser.add_argument(
        "--sleep-time",
        default=sideroxylon_default_args_object.sleep_time,
        help="Seconds to wait until the next API call.",
    )

    parser.add_argument(
        "--verbose",
        default=sideroxylon_default_args_object.verbose,
        help=(
            "Define how descriptive you want sideroxylon to be."
            "\nZero (0) is non-descriptive."
            "\nOne (1) is minimally descriptive."
            "\nTwo (2) is fully descriptive."
        ),
    )

    parser.add_argument(
        "--write-in-file-without-duplicates",
        action="store_true",
        help=(
            "When writing the repository URLs into their respective files, check if the URLs already exist in the files."
        ),
    )

    parser.add_argument(
        "--check-at-start-for-rate-limits",
        action="store_true",
        help=(
            "Check for the reset date of rate limits at the start of sideroxylon. If a rate limit reset date is found and it hasn't happened yet, stop sideroxylon."
        ),
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help=("Display the current version of sideroxylon."),
    )

    args = parser.parse_args()

    if args.version:
        display_sideroxylon_version()

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
            # When writing the repository URLs into their respective files, check if the URLs already exist in the files.
            write_in_file_without_duplicates=args.write_in_file_without_duplicates,
            # Check for the reset date of rate limits at the start of sideroxylon. If a rate limit reset date is found and it hasn't happened yet, stop sideroxylon.
            check_at_start_for_rate_limits=args.check_at_start_for_rate_limits,
        )

    except KeyboardInterrupt:
        sys.exit("\nsideroxylon terminated by user.")

    end_time: float = time.perf_counter()

    print_time_elapsed(start_time, end_time)


def get_all_urls_from_pipes_and_urls_arg(args) -> str:
    piped_urls: str = ""

    if not sys.stdin.isatty():
        piped_urls: str = cast(str, sys.stdin.read())

    arg_urls: str = piped_urls + args.urls
    arg_urls: str = os.linesep.join([s for s in arg_urls.splitlines() if s])

    return arg_urls


def print_time_elapsed(start_time: float, end_time: float) -> None:
    time_elapsed: float = end_time - start_time

    print("sideroxylon finished")
    print(f"Approximate time elapsed: {time_elapsed:.6f} seconds")


def display_sideroxylon_version():
    print("0.3.0")
    sys.exit(0)


if __name__ == "__main__":
    main()
