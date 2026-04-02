import requests
import time
import os
import typer
from typing import Annotated
# from typing_extensions import Annotated
from typing import Any

HOME_DIR: str = os.environ.get("HOME", os.path.expanduser("~"))
XDG_DATA_HOME_DIR: str = os.environ.get("XDG_DATA_HOME", os.path.expanduser(f"{HOME_DIR}/.local/share"))
SIDEROXYLON_DIR: str = f"{XDG_DATA_HOME_DIR}/sideroxylon"

def assign_token_to_headers(token_file):
    """
    Get headers for GitHub.
    """

    # Get contents of token file and store them on GITHUB_TOKEN
    with open(token_file, 'r') as file:
        github_token: str = file.read().replace('\n', '')  # Example: 'ghp_xxx'

    # If it exists, pass token to GitHub
    repository_headers: dict[str, Any] = {}
    if github_token:
        repository_headers['Authorization'] = f'token {github_token}'

    return repository_headers

def convert_github_url_to_api_url(repository_url):
    """
    Convert GitHub URL to GitHub API URL.
    """

    # Check if we are at the correct position of the URL, store user and
    # repository names, and return the converted URL
    parts = repository_url.strip().split('/')

    if len(parts) < 5:
        return None

    user: str = parts[3]
    repo: str = parts[4]

    return f'https://api.github.com/repos/{user}/{repo}'

def get_urls_inside_repository_url_file(repository_url_file):
    """
    Read URLs inside repository_url_file.
    """

    with open(repository_url_file, 'r') as file:
        urls: list[str] = [line.strip() for line in file if line.strip()]

    return urls

def get_github_repository_programming_language(repository_url, repository_headers):
    """
    Get the main programming language of the provided repository URL.
    """

    # Convert normal URL to api URL
    api_url: str = convert_github_url_to_api_url(repository_url)

    # Check if api URL exists, and if not return Unknown
    if not api_url:
        return 'Unknown'

    # Try to use the token. If the token fails send the URL to Unknown.
    try:
        response: requests.models.Response = requests.get(api_url, headers=repository_headers)

        if response.status_code != 200:
            print(f'Status code: {response.status_code}')
            return 'Unknown'

        data: dict[str, Any] = response.json()

        # If there is no language then default to Unknown
        return data.get('language') or 'Unknown'

    except Exception as e:
        # If there is an exception then default to Unknown
        print(f'Error fetching {repository_url}: {e}')
        return 'Unknown'

def store_repository_url_in_corresponding_file(repository_urls, repository_headers, languages_directory, file_extension, sleep_time):
    """
    Store each repository URL in the file with the name of its main programming language.
    """
    for url in repository_urls:
        language: dict[str, Any] | str = get_github_repository_programming_language(url, repository_headers)

        filename = (
            f'{language}.{file_extension}'  # Note: I might want to replace spaces with hyphens
        )

        full_path_filename = os.path.join(languages_directory, filename)

        # If full_path_filename doesn't exist, create it
        os.makedirs(os.path.dirname(full_path_filename), exist_ok=True)

        with open(full_path_filename, 'a') as file:
            file.write(url + '\n')

        print(f'{url} -> {language}')

        # This line is here to avoid hitting rate limits
        time.sleep(sleep_time)

def clean_repository_url_file(repository_url_file):
    """
    Clean the file with the repository URLs.
    """
    open(repository_url_file, 'w').close()

def sideroxylon(
    # File that cotains the token.
    token_file: Annotated[str, typer.Option(help='Path to the GitHub token file.')] = f'{SIDEROXYLON_DIR}/gh_token.org',
    # File that contains the repository urls.
    repository_url_file: Annotated[str, typer.Option(help='Path to the repository URLs file.')] = f'{SIDEROXYLON_DIR}/github_repos.org',
    # Directory with all the programming language files.
    languages_directory: Annotated[str, typer.Option(help='Path to the directory where URLs are stored.')] = f'{SIDEROXYLON_DIR}/languages/',
    # File extension for languages_directory generated files.
    file_extension: Annotated[str, typer.Option(help='File extension for files generated inside languages_directory.')] = 'org',
    # Seconds to wait until the next API call.
    sleep_time: Annotated[int, typer.Option(help='Seconds to wait until the next API call.')] = 2,
):
    """
    Entry point of the sideroxylon cli.
    """

    repository_headers: dict[str, Any] = assign_token_to_headers(token_file)

    # Get each link in the repository URL file
    urls: list[str] = get_urls_inside_repository_url_file(repository_url_file)

    # Once we get the main programming language, put the link in a file with the
    # same name as the language
    store_repository_url_in_corresponding_file(urls, repository_headers, languages_directory, file_extension, sleep_time)

    # Clear the repository URL file after going through each link
    # At some point I will change this so at the beginning of the program it clears all files
    clean_repository_url_file(repository_url_file)


if __name__ == '__main__':
    sideroxylon()
