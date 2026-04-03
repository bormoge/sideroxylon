from sideroxylon import sideroxylon
from typing import Any
import os
import pytest

@pytest.fixture
def test_dir():
    return 'src/tests'

@pytest.fixture
def github_headers(test_dir):
    return sideroxylon.assign_token_to_headers(f'{test_dir}/gh_token.org')

@pytest.fixture
def test_repository():
    return 'https://github.com/bormoge/sideroxylon'

def test_initialize_directories_and_files(test_dir):
    languages_dir = f'{test_dir}/languages_straw/'
    token_file = f'{test_dir}/straw.org'

    directories_and_files: dict[str, list[str]] = {
        "directories": [languages_dir],
        "files": [token_file]
    }

    if os.path.isdir(languages_dir):
        os.rmdir(languages_dir)

    if os.path.isfile(token_file):
        os.remove(token_file)

    sideroxylon.initialize_directories_and_files(directories_and_files)

    assert os.path.isdir(languages_dir)
    assert os.path.isfile(token_file)


def test_assign_token_to_headers(test_dir, github_headers):
    with open(f'{test_dir}/gh_token.org', 'r') as file:
        github_token: str = file.read().replace('\n', '')

    repository_headers: dict[str, Any] = {}
    repository_headers['Authorization'] = f'token {github_token}'

    assert github_headers == repository_headers

def test_convert_github_url_to_api_url(test_repository):
    assert sideroxylon.convert_github_url_to_api_url(test_repository) == 'https://api.github.com/repos/bormoge/sideroxylon'

def test_get_urls_inside_repository_url_file(test_dir):
    url_list: list[str] = ['https://github.com/bormoge/sideroxylon', 'https://github.com/bormoge/spinosum', 'https://github.com/bormoge/guava-themes']

    assert sideroxylon.get_urls_inside_repository_url_file(f'{test_dir}/test_url_file.org') == url_list

def test_get_github_repository_programming_language(github_headers, test_repository):
    test_repository_failure: str = 'https://github.com/bormoge/failure'

    assert sideroxylon.get_github_repository_programming_language(test_repository, github_headers) == 'Python'
    assert sideroxylon.get_github_repository_programming_language(test_repository_failure, github_headers) == 'Unknown'

def test_store_repository_url_in_corresponding_file(test_dir, github_headers):
    if os.path.isfile(f'{test_dir}/Python.txt'):
        os.remove(f'{test_dir}/Python.txt')

    url_file: list[str] = ['https://github.com/bormoge/sideroxylon']

    sideroxylon.store_repository_url_in_corresponding_file(url_file, github_headers, test_dir, 'txt', 2)

    with open(f'{test_dir}/Python.txt', 'r') as file:
        python_org_contents: str = file.read().replace('\n', '')

    assert os.path.isfile(f'{test_dir}/Python.txt')
    assert python_org_contents == 'https://github.com/bormoge/sideroxylon'
