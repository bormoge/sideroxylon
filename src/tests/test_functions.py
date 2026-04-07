from sideroxylon import sideroxylon
from typing import Any
import os
import pytest

@pytest.fixture
def test_dir():
    return 'src/tests'

@pytest.fixture
def throwaway_dir(test_dir):
    return f'{test_dir}/throwaway'

@pytest.fixture
def forge_headers(throwaway_dir):
    return sideroxylon.assign_token_to_headers(f'{throwaway_dir}/token.org')

@pytest.fixture
def test_repository():
    return 'https://github.com/bormoge/sideroxylon'

def test_initialize_directories_and_files(throwaway_dir):
    example_dir = f'{throwaway_dir}/languages_example/'
    example_file = f'{throwaway_dir}/example.org'

    directories_and_files: dict[str, list[str]] = {
        "directories": [example_dir],
        "files": [example_file]
    }

    if os.path.isdir(example_dir):
        os.rmdir(example_dir)

    if os.path.isfile(example_file):
        os.remove(example_file)

    sideroxylon.initialize_directories_and_files(directories_and_files)

    assert os.path.isdir(example_dir)
    assert os.path.isfile(example_file)


def test_assign_token_to_headers(throwaway_dir, forge_headers):
    with open(f'{throwaway_dir}/token.org', 'r') as file:
        forge_token: str = file.read().replace('\n', '')

    repository_headers: dict[str, Any] = {}
    repository_headers['Authorization'] = f'token {forge_token}'

    assert forge_headers == repository_headers

def test_convert_forge_url_to_api_url(test_repository):
    assert sideroxylon.convert_forge_url_to_api_url(test_repository) == 'https://api.github.com/repos/bormoge/sideroxylon'

def test_get_urls_inside_repository_url_file(throwaway_dir):
    url_list: list[str] = ['https://github.com/bormoge/sideroxylon', 'https://github.com/bormoge/spinosum', 'https://github.com/bormoge/guava-themes']

    test_url_file = f'{throwaway_dir}/test_url_file.org'

    if not os.path.exists(test_url_file) or os.path.getsize(test_url_file) == 0:
        with open(test_url_file, "w") as file:
            for url in url_list:
                file.write(url + "\n")

    assert sideroxylon.get_urls_inside_repository_url_file(f'{throwaway_dir}/test_url_file.org') == url_list

def test_fetch_forge_repository_data(forge_headers):
    api_url_success = 'https://api.github.com/repos/bormoge/sideroxylon'
    api_url_failure = 'https://api.github.com/repos/bormoge/failure'

    assert sideroxylon.fetch_forge_repository_data(api_url_success, forge_headers).get('language') == 'Python'
    assert sideroxylon.fetch_forge_repository_data(api_url_failure, forge_headers) is None

def test_get_repository_programming_language(forge_headers, test_repository):
    test_repository_failure: str = 'https://github.com/bormoge/failure'

    assert sideroxylon.get_repository_programming_language(test_repository, forge_headers) == 'Python'
    assert sideroxylon.get_repository_programming_language(test_repository_failure, forge_headers) == 'Unknown'

def test_store_repository_urls_in_corresponding_files(throwaway_dir, forge_headers, test_repository):
    if os.path.isfile(f'{throwaway_dir}/Python.txt'):
        os.remove(f'{throwaway_dir}/Python.txt')

    test_url: list[str] = [test_repository]

    sideroxylon.store_repository_urls_in_corresponding_files(test_url, forge_headers, throwaway_dir, 'txt', 2)

    with open(f'{throwaway_dir}/Python.txt', 'r') as file:
        python_org_contents: str = file.read().replace('\n', '')

    assert os.path.isfile(f'{throwaway_dir}/Python.txt')
    assert python_org_contents == 'https://github.com/bormoge/sideroxylon'
