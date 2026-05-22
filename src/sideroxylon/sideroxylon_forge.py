from urllib.error import HTTPError
from http.client import HTTPResponse
from typing import Any
from abc import ABC, abstractmethod


class SideroxylonForge(ABC):

    @abstractmethod
    def convert_forge_url_to_api_url(self, repository_url: str) -> str | None:
        pass

    @abstractmethod
    def fetch_forge_repository_data(
        self, api_url: str
    ) -> HTTPResponse | HTTPError | None:
        pass

    @abstractmethod
    def normalize_forge_repository_url(self, repository_url: str) -> str:
        pass

    @abstractmethod
    def get_repository_programming_language(
        self, api_url: str, response: HTTPResponse | HTTPError | None
    ) -> str | Any:
        pass

    @abstractmethod
    def get_forge_name(self) -> str:
        pass

    @abstractmethod
    def __init__(self):
        pass
