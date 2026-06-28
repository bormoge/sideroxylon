import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SideroxylonXDG:
    HOME_DIR: str = os.environ.get("HOME", os.path.expanduser("~"))
    XDG_DATA_HOME_DIR: str = os.environ.get(
        "XDG_DATA_HOME", os.path.expanduser(f"{HOME_DIR}/.local/share")
    )
    XDG_CONFIG_HOME_DIR: str = os.environ.get(
        "XDG_CONFIG_HOME", os.path.expanduser(f"{HOME_DIR}/.config")
    )
    XDG_CACHE_HOME_DIR: str = os.environ.get(
        "XDG_CACHE_HOME", os.path.expanduser(f"{HOME_DIR}/.cache")
    )
    SIDEROXYLON_DATA_HOME_DIR: str = f"{XDG_DATA_HOME_DIR}/sideroxylon"
    SIDEROXYLON_CONFIG_HOME_DIR: str = f"{XDG_CONFIG_HOME_DIR}/sideroxylon"
    SIDEROXYLON_CACHE_HOME_DIR: str = f"{XDG_CACHE_HOME_DIR}/sideroxylon"


sideroxylon_xdg_object: SideroxylonXDG = SideroxylonXDG()


@dataclass(frozen=True)
class SideroxylonDefaultArgs:
    # File that contains the configuration values.
    config_file: str = (
        f"{sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR}/config.json"
    )
    # File that contains the environment variables.
    env_file: str = f"{sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR}/.env"
    # File that contains the repository urls.
    repository_url_file: str = (
        f"{sideroxylon_xdg_object.SIDEROXYLON_DATA_HOME_DIR}/repository_urls.org"
    )
    # File that contains the filtered urls.
    filtered_urls_file: str = (
        f"{sideroxylon_xdg_object.SIDEROXYLON_CONFIG_HOME_DIR}/filtered_urls.org"
    )
    # Directory with all the repository URLs already sorted.
    sorted_repositories_directory: str = (
        f"{sideroxylon_xdg_object.SIDEROXYLON_DATA_HOME_DIR}/sorted_repositories/"
    )
    # File extension for files generated inside sorted_repositories_directory.
    file_extension: str = "org"
    # Seconds to wait until the next API call.
    sleep_time: float = 2.0
    # Verbose modes.
    verbose: int = 1
    # String that contains URLs passed by the user as
    # a positional argument and/or pipe output.
    arg_urls: str = ""
    # Check for the reset date of rate limits at the start of sideroxylon. If a rate limit reset date is found and it hasn't happened yet, stop sideroxylon.
    check_at_start_for_rate_limits: bool = False


sideroxylon_default_args_object: SideroxylonDefaultArgs = SideroxylonDefaultArgs()
