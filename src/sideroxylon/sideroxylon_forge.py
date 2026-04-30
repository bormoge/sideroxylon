from abc import ABC, abstractmethod
from typing import Any


class SideroxylonForge(ABC):

    @abstractmethod
    def convert_forge_url_to_api_url(self, repository_url: str) -> str | None:
        pass

    @abstractmethod
    def fetch_forge_repository_data(self, api_url: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def clean_forge_repository_url(self, repository_url: str) -> str | None:
        pass

    @abstractmethod
    def get_repository_programming_language(
        self, api_url: str, fetched_data: dict[str, Any] | None
    ) -> str | Any:
        pass

    @abstractmethod
    def get_forge_name(self) -> str:
        pass

    @abstractmethod
    def __init__(self):
        pass
