from sideroxylon.sideroxylon_github import SideroxylonGitHub
from typing import Any
import pytest


@pytest.fixture
def test_dir():
    return "src/tests"


@pytest.fixture
def throwaway_dir(test_dir):
    return f"{test_dir}/throwaway"


@pytest.fixture
def token_file(throwaway_dir):
    return f"{throwaway_dir}/token.org"


@pytest.fixture
def test_repository():
    return "https://github.com/bormoge/sideroxylon"


@pytest.fixture
def github_forge_object(token_file):
    return SideroxylonGitHub(token_file)


def test_assign_token_to_headers(token_file):
    with open(token_file, "r") as file:
        forge_token: str = file.read().replace("\n", "")

    g_forge_obj: SideroxylonGitHub = SideroxylonGitHub(token_file)

    assert g_forge_obj.forge_headers == {"Authorization": "token " + forge_token}


def test_convert_forge_url_to_api_url(test_repository, github_forge_object):
    assert (
        github_forge_object.convert_forge_url_to_api_url(test_repository)
        == "https://api.github.com/repos/bormoge/sideroxylon/languages"
    )


def test_fetch_forge_repository_data(github_forge_object):
    api_url_success = "https://api.github.com/repos/bormoge/sideroxylon/languages"
    api_url_failure = "https://api.github.com/repos/bormoge/failure/languages"
    api_url_no_language = (
        "https://api.github.com/repos/nix-community/awesome-nix/languages"
    )

    data_success: dict[str, Any] | None = (
        github_forge_object.fetch_forge_repository_data(api_url_success)
    )

    assert max(data_success, key=lambda k: data_success[k]) == "Python"
    assert github_forge_object.fetch_forge_repository_data(api_url_failure) is None
    assert github_forge_object.fetch_forge_repository_data(api_url_no_language) == {}


def test_get_repository_programming_language(github_forge_object, test_repository):
    test_repository_failure: str = "https://github.com/bormoge/failure"
    test_repository_no_language: str = "https://github.com/nix-community/awesome-nix"

    assert (
        github_forge_object.get_repository_programming_language(test_repository)
        == "Python"
    )
    assert (
        github_forge_object.get_repository_programming_language(
            test_repository_failure
        )
        == "Unknown"
    )
    assert (
        github_forge_object.get_repository_programming_language(
            test_repository_no_language
        )
        == "No_Programming_Language"
    )
