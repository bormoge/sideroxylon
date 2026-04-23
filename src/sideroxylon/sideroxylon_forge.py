from abc import ABC, abstractmethod
from typing import Any


class SideroxylonForge(ABC):

    @abstractmethod
    def fetch_forge_repository_data(self, api_url: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def clean_forge_repository_url(self, repository_url: str) -> str | None:
        pass

    @abstractmethod
    def get_repository_programming_language(self, repository_url: str) -> str | Any:
        pass

    @abstractmethod
    def get_forge_name(self):
        pass

    @abstractmethod
    def __init__(self):
        pass
