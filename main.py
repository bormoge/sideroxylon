import requests
import time
import os

# File that cotains the token
API_PATH = "token.org"

# File that contains the repository links
ORIGINAL_FILE = "repos.org"

# Directory with all the programming language files
LANGUAGES_DIRECTORY = "languages/"

# Get contents of API file and store them on GITHUB_TOKEN
with open(API_PATH, "r") as file:
    GITHUB_TOKEN = file.read().replace("\n", "")  # Example: "ghp_xxx"

# If it exists, pass token to GitHub
HEADERS = {}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"


def convert_github_url_to_api_url(repo_url):
    """
    Convert GitHub URL to GitHub API URL
    """
    # Check if we are at the correct position of the url, store user and
    # repository names, and return the converted URL
    parts = repo_url.strip().split("/")
    if len(parts) < 5:
        return None
    user = parts[3]
    repo = parts[4]
    return f"https://api.github.com/repos/{user}/{repo}"


def get_github_repository_programming_language(repo_url):
    # Convert normal url to api url
    api_url = convert_github_url_to_api_url(repo_url)

    # Check if api url exists, and if not return Unknown
    if not api_url:
        return "Unknown"

    # Try to use the token. If the token fails send the url to Unknown.
    # Note: I will probably change the implementation so, instead
    # of classifying the link as Unknown, the program continues
    # without using a token.
    try:
        response = requests.get(api_url, headers=HEADERS)
        if response.status_code != 200:
            print(response.status_code)
            return "Unknown"

        data = response.json()

        # If there is no language then default to Unknown
        return data.get("language") or "Unknown"
    except Exception as e:
        # If there is an exception then default to Unknown
        print(f"Error fetching {repo_url}: {e}")
        return "Unknown"


def main():
    # Get each link in the original file
    with open(ORIGINAL_FILE, "r") as file:
        links = [line.strip() for line in file if line.strip()]

    # Once we get the main programming language, put the link in a file with the
    # same name as the language
    for link in links:
        language = get_github_repository_programming_language(link)

        filename = f"{language}.txt" # Note: I might want to replace spaces with hyphens

        full_path_filename = os.path.join(LANGUAGES_DIRECTORY, filename)

        # If full_path_filename doesn't exist, create it
        os.makedirs(os.path.dirname(full_path_filename), exist_ok=True)

        with open(full_path_filename, "a") as file:
            file.write(link + "\n")

        print(f"{link} -> {language}")

        # This line is here to avoid hitting rate limits
        time.sleep(2)

    # Clear the original file after going through each link
    # At some point I will change this so at the beginning of the program it clears all files
    open(ORIGINAL_FILE, "w").close()


if __name__ == "__main__":
    main()
