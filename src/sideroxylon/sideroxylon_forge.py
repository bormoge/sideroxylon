from abc import ABC, abstractmethod
from typing import Any


class SideroxylonForge(ABC):

    @abstractmethod
    def fetch_forge_repository_data(
        self, api_url: str
    ) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def get_repository_programming_language(
        self, repository_url: str
    ) -> str | Any:
        pass

    @abstractmethod
    def get_forge_name():
        pass

    @abstractmethod
    def __init__(token_file):
        pass
