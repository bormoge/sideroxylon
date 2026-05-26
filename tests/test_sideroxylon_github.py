import pytest
import os
from typing import Any
from typing import cast
from pathlib import Path
from sideroxylon.sideroxylon_main import SideroxylonMain
from sideroxylon.sideroxylon_github import SideroxylonGitHub


@pytest.fixture
def sideroxylon_main_object():
    sideroxylon_main_object: SideroxylonMain = SideroxylonMain()
    return sideroxylon_main_object


@pytest.fixture
def test_dir():
    directory = "./tests"
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory


@pytest.fixture
def throwaway_dir(test_dir):
    directory = f"{test_dir}/throwaway"
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory


@pytest.fixture
def env_file(throwaway_dir):
    file = f"{throwaway_dir}/.env"
    Path(file).touch(exist_ok=True)
    return os.path.expanduser(file)


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
def github_forge_object(sideroxylon_main_object, env_file):
    sideroxylon_main_object.read_sideroxylon_env_variables(env_file)
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
def response_success(github_forge_object, test_api_url_success):
    response_success: dict[str, Any] | None = (
        github_forge_object.fetch_forge_repository_data(test_api_url_success)
    )
    return response_success


@pytest.fixture
def response_failure(github_forge_object, test_api_url_failure):
    response_failure: dict[str, Any] | None = (
        github_forge_object.fetch_forge_repository_data(test_api_url_failure)
    )
    return response_failure


@pytest.fixture
def response_no_language(github_forge_object, test_api_url_no_language):
    response_no_language: dict[str, Any] | None = (
        github_forge_object.fetch_forge_repository_data(test_api_url_no_language)
    )
    return response_no_language


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
    data_success: dict[str, Any] | None = github_forge_object.convert_response_to_dict(
        github_forge_object.fetch_forge_repository_data(test_api_url_success)
    )

    assert (
        max(cast(dict, data_success), key=lambda k: cast(dict, data_success)[k])
        == "Python"
    )
    assert (
        github_forge_object.fetch_forge_repository_data(test_api_url_failure).getcode()
        == 404
    )
    assert (
        github_forge_object.convert_response_to_dict(
            github_forge_object.fetch_forge_repository_data(test_api_url_no_language)
        )
        == {}
    )


def test_get_repository_programming_language(
    github_forge_object,
    test_repository_success,
    test_repository_failure,
    test_repository_no_language,
    response_success,
    response_failure,
    response_no_language,
):
    assert (
        github_forge_object.get_repository_programming_language(
            test_repository_success, response_success
        )
        == "Python"
    )
    assert (
        github_forge_object.get_repository_programming_language(
            test_repository_failure, response_failure
        )
        == "GitHub_URL"
    )
    assert (
        github_forge_object.get_repository_programming_language(
            test_repository_no_language, response_no_language
        )
        == "No_Programming_Language"
    )
