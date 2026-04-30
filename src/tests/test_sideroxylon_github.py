from sideroxylon import sideroxylon
from sideroxylon.sideroxylon_github import SideroxylonGitHub
from typing import Any
import pytest
import os


@pytest.fixture
def test_dir():
    return "src/tests"


@pytest.fixture
def throwaway_dir(test_dir):
    return f"{test_dir}/throwaway"


@pytest.fixture
def env_file(throwaway_dir):
    return os.path.expanduser(f"{throwaway_dir}/.env")


@pytest.fixture
def test_repository_success():
    return "https://github.com/bormoge/sideroxylon"


@pytest.fixture
def test_repository_failure():
    return "https://github.com/bormoge/failure"


@pytest.fixture
def test_repository_no_language():
    return "https://github.com/nix-community/awesome-nix"


@pytest.fixture
def github_forge_object(env_file):
    sideroxylon.load_sideroxylon_env_variables(env_file)
    return SideroxylonGitHub()


@pytest.fixture
def test_api_url_success(github_forge_object, test_repository_success):
    test_api_url_success: str | None = github_forge_object.convert_forge_url_to_api_url(
        test_repository_success
    )
    return test_api_url_success


@pytest.fixture
def test_api_url_failure(github_forge_object, test_repository_failure):
    test_api_url_failure: str | None = github_forge_object.convert_forge_url_to_api_url(
        test_repository_failure
    )
    return test_api_url_failure


@pytest.fixture
def test_api_url_no_language(github_forge_object, test_repository_no_language):
    test_api_url_no_language: str | None = (
        github_forge_object.convert_forge_url_to_api_url(test_repository_no_language)
    )
    return test_api_url_no_language


@pytest.fixture
def fetched_data_success(github_forge_object, test_api_url_success):
    fetched_data_success: dict[str, Any] | None = (
        github_forge_object.fetch_forge_repository_data(test_api_url_success)
    )
    return fetched_data_success


@pytest.fixture
def fetched_data_failure(github_forge_object, test_api_url_failure):
    fetched_data_failure: dict[str, Any] | None = (
        github_forge_object.fetch_forge_repository_data(test_api_url_failure)
    )
    return fetched_data_failure


@pytest.fixture
def fetched_data_no_language(github_forge_object, test_api_url_no_language):
    fetched_data_no_language: dict[str, Any] | None = (
        github_forge_object.fetch_forge_repository_data(test_api_url_no_language)
    )
    return fetched_data_no_language


def test_convert_forge_url_to_api_url(test_repository_success, github_forge_object):
    assert (
        github_forge_object.convert_forge_url_to_api_url(test_repository_success)
        == "https://api.github.com/repos/bormoge/sideroxylon/languages"
    )


def test_fetch_forge_repository_data(
    github_forge_object,
    test_api_url_success,
    test_api_url_failure,
    test_api_url_no_language,
):
    data_success: dict[str, Any] | None = (
        github_forge_object.fetch_forge_repository_data(test_api_url_success)
    )

    assert max(data_success, key=lambda k: data_success[k]) == "Python"
    assert github_forge_object.fetch_forge_repository_data(test_api_url_failure) is None
    assert github_forge_object.fetch_forge_repository_data(test_api_url_no_language) == {}


def test_get_repository_programming_language(
    github_forge_object,
    test_repository_success,
    test_repository_failure,
    test_repository_no_language,
    test_api_url_success,
    test_api_url_failure,
    test_api_url_no_language,
    fetched_data_success,
    fetched_data_failure,
    fetched_data_no_language,
):
    assert (
        github_forge_object.get_repository_programming_language(
            test_repository_success, fetched_data_success
        )
        == "Python"
    )
    assert (
        github_forge_object.get_repository_programming_language(
            test_repository_failure, fetched_data_failure
        )
        == "GitHub_URL"
    )
    assert (
        github_forge_object.get_repository_programming_language(
            test_repository_no_language, fetched_data_no_language
        )
        == "No_Programming_Language"
    )
