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
