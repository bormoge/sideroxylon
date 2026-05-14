import sys
import argparse
from .sideroxylon_main import sideroxylon
from .sideroxylon_main import SIDEROXYLON_CONFIG_HOME_DIR
from .sideroxylon_main import SIDEROXYLON_DATA_HOME_DIR

def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="sideroxylon",
        description="sideroxylon CLI",
    )

    parser.add_argument(
        "--env-file",
        default = f"{SIDEROXYLON_CONFIG_HOME_DIR}/.env",
        help = "Path to the dotenv (.env) file.",
    )

    parser.add_argument(
        "--repository-url-file",
        default = f"{SIDEROXYLON_DATA_HOME_DIR}/repository_urls.org",
        help = "Path to the file that contains the repository URLs file.",
    )

    parser.add_argument(
        "--languages-directory",
        default = f"{SIDEROXYLON_DATA_HOME_DIR}/languages/",
        help = "Path to the directory where the URLs will be stored.",
    )

    parser.add_argument(
        "--file-extension",
        default = "org",
        help = "File extension for files generated inside languages-directory.",
    )

    parser.add_argument(
        "--sleep-time",
        default = 2.0,
        help = "Seconds to wait until the next API call.",
    )

    parser.add_argument(
        "--verbose",
        default = 1,
        help = (
            "Define how descriptive you want sideroxylon to be."
            "\nZero (0) is non-descriptive."
            "\nOne (1) is minimally descriptive."
            "\nTwo (2) is fully descriptive."
        ),
    )

    args = parser.parse_args()

    try:
        sideroxylon(
            # File that contains the environment variables.
            env_file = args.env_file,
            # File that contains the repository urls.
            repository_url_file = args.repository_url_file,
            # Directory with all the programming language files.
            languages_directory = args.languages_directory,
            # File extension for languages_directory generated files.
            file_extension = args.file_extension,
            # Seconds to wait until the next API call.
            sleep_time = args.sleep_time,
            # Verbose modes.
            verbose = args.verbose,
        )

    except KeyboardInterrupt:
        sys.exit("\nsideroxylon terminated by user.")

if __name__ == "__main__":
    main()
