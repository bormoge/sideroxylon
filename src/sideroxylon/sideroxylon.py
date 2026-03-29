import requests
import time
import os
import typer
from typing import Annotated
# from typing_extensions import Annotated

def assign_token_to_headers(token_file):
    """
    Get headers for GitHub
    """

    # Get contents of token file and store them on GITHUB_TOKEN
    with open(token_file, 'r') as file:
        github_token = file.read().replace('\n', '')  # Example: 'ghp_xxx'

    # If it exists, pass token to GitHub
    repository_headers = {}
    if github_token:
        repository_headers['Authorization'] = f'token {github_token}'

    return repository_headers

def convert_github_url_to_api_url(repo_url):
    """
    Convert GitHub URL to GitHub API URL
    """

    # Check if we are at the correct position of the url, store user and
    # repository names, and return the converted URL
    parts = repo_url.strip().split('/')

    if len(parts) < 5:
        return None

    user = parts[3]
    repo = parts[4]

    return f'https://api.github.com/repos/{user}/{repo}'


def get_github_repository_programming_language(repository_url, repository_headers):
    """
    Get the main programming language of the provided repository url.
    """

    # Convert normal url to api url
    api_url = convert_github_url_to_api_url(repository_url)

    # Check if api url exists, and if not return Unknown
    if not api_url:
        return 'Unknown'

    # Try to use the token. If the token fails send the url to Unknown.
    try:
        response = requests.get(api_url, headers=repository_headers)
        if response.status_code != 200:
            print(f'Status code: {response.status_code}')
            return 'Unknown'

        data = response.json()

        # If there is no language then default to Unknown
        return data.get('language') or 'Unknown'
    except Exception as e:
        # If there is an exception then default to Unknown
        print(f'Error fetching {repository_url}: {e}')
        return 'Unknown'

def sideroxylon(
    # File that cotains the token
    token_file: Annotated[str, typer.Option(help='Path to the GitHub token file.')] = 'gh_token.org',
    # File that contains the repository urls
    repository_url_file: Annotated[str, typer.Option(help='Path to the repository urls file.')] = 'github_repos.org',
    # Directory with all the programming language files
    languages_directory: Annotated[str, typer.Option(help='Path to the directory where urls are stored.')] = 'languages/',
):
    """
    Entry point of the sideroxylon cli.
    """

    repository_headers: dict = assign_token_to_headers(token_file)

    # Get each link in the repository url file
    with open(repository_url_file, 'r') as file:
        urls: list[str] = [line.strip() for line in file if line.strip()]

    # Once we get the main programming language, put the link in a file with the
    # same name as the language
    for url in urls:
        language = get_github_repository_programming_language(url, repository_headers)

        filename = (
            f'{language}.org'  # Note: I might want to replace spaces with hyphens
        )

        full_path_filename = os.path.join(languages_directory, filename)

        # If full_path_filename doesn't exist, create it
        os.makedirs(os.path.dirname(full_path_filename), exist_ok=True)

        with open(full_path_filename, 'a') as file:
            file.write(url + '\n')

        print(f'{url} -> {language}')

        # This line is here to avoid hitting rate limits
        time.sleep(2)

    # Clear the repository url file after going through each link
    # At some point I will change this so at the beginning of the program it clears all files
    open(repository_url_file, 'w').close()


if __name__ == '__main__':
    sideroxylon()
