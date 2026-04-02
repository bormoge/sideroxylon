from sideroxylon import sideroxylon
from typing import Any
import os

def test_assign_token_to_headers():
    with open('gh_token.org', 'r') as file:
        github_token: str = file.read().replace('\n', '')

    repository_headers: dict[str, Any] = {}
    repository_headers['Authorization'] = f'token {github_token}'

    assert sideroxylon.assign_token_to_headers('src/tests/gh_token.org') == repository_headers

def test_convert_github_url_to_api_url():
    test_repository: str = 'https://github.com/bormoge/sideroxylon'
    assert sideroxylon.convert_github_url_to_api_url(test_repository) == 'https://api.github.com/repos/bormoge/sideroxylon'

def test_get_urls_inside_repository_url_file():
    url_list: list[str] = ['https://github.com/bormoge/sideroxylon', 'https://github.com/bormoge/spinosum', 'https://github.com/bormoge/guava-themes']

    assert sideroxylon.get_urls_inside_repository_url_file('src/tests/test_url_file.org') == url_list

def test_get_github_repository_programming_language():
    headers: dict[str, Any] = sideroxylon.assign_token_to_headers('src/tests/gh_token.org')
    url_sucess: str = 'https://github.com/bormoge/sideroxylon'
    url_failure: str = 'https://github.com/bormoge/failure'

    assert sideroxylon.get_github_repository_programming_language(url_sucess, headers) == 'Python'
    assert sideroxylon.get_github_repository_programming_language(url_failure, headers) == 'Unknown'

def test_store_repository_url_in_corresponding_file():
    if os.path.isfile('src/tests/Python.txt'):
        os.remove('src/tests/Python.txt')

    headers: dict[str, Any] = sideroxylon.assign_token_to_headers('src/tests/gh_token.org')
    url_file: list[str] = ['https://github.com/bormoge/sideroxylon']
    dir: str = 'src/tests'

    sideroxylon.store_repository_url_in_corresponding_file(url_file, headers, dir, 'txt', 2)

    with open('src/tests/Python.txt', 'r') as file:
        python_org_contents: str = file.read().replace('\n', '')

    assert os.path.isfile('src/tests/Python.txt')
    assert python_org_contents == 'https://github.com/bormoge/sideroxylon'
