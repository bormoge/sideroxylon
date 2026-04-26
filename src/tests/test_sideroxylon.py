from sideroxylon import sideroxylon
import os
import pytest


@pytest.fixture
def test_dir():
    return "src/tests"


@pytest.fixture
def throwaway_dir(test_dir):
    return f"{test_dir}/throwaway"


@pytest.fixture
def python_txt_file(throwaway_dir):
    return f"{throwaway_dir}/Python.txt"


@pytest.fixture
def env_file(throwaway_dir):
    return os.path.expanduser(f"{throwaway_dir}/.env")


@pytest.fixture
def test_repository():
    return "https://github.com/bormoge/sideroxylon"


@pytest.fixture
def test_repository_list():
    return [
        "https://github.com/bormoge/sideroxylon",
        "https://github.com/bormoge/spinosum",
        "https://github.com/bormoge/guava-themes",
    ]


def test_load_sideroxylon_env_variables(env_file):
    sideroxylon.load_sideroxylon_env_variables(env_file)

    assert os.environ.get("SIDEROXYLON_GITHUB_TOKEN") is not None


def test_get_urls_inside_repository_url_file(throwaway_dir, test_repository_list):
    test_url_file = f"{throwaway_dir}/test_url_file.org"

    if not os.path.exists(test_url_file) or os.path.getsize(test_url_file) == 0:
        try:
            with open(test_url_file, "w") as file:
                for url in test_repository_list:
                    file.write(url + "\n")

        except OSError as e:
            print(f"Error reading {test_url_file}: {e}")

    assert (
        sideroxylon.get_urls_inside_repository_url_file(
            f"{throwaway_dir}/test_url_file.org"
        )
        == test_repository_list
    )


def test_sequential_write_into_file(python_txt_file, test_repository):
    if os.path.isfile(python_txt_file):
        os.remove(python_txt_file)

    sideroxylon.sequential_write_into_file(python_txt_file, test_repository)

    try:
        with open(python_txt_file, "r") as file:
            python_org_contents: str = file.read().replace("\n", "")

    except OSError as e:
        print(f"Error reading {python_txt_file}: {e}")

    assert os.path.isfile(python_txt_file)
    assert python_org_contents == "https://github.com/bormoge/sideroxylon"


def test_initialize_directories_and_files(throwaway_dir):
    example_dir = f"{throwaway_dir}/languages_example/"
    example_file = f"{throwaway_dir}/example.org"

    directories_and_files: dict[str, list[str]] = {
        "directories": [example_dir],
        "files": [example_file],
    }

    if os.path.isdir(example_dir):
        os.rmdir(example_dir)

    if os.path.isfile(example_file):
        os.remove(example_file)

    sideroxylon.initialize_directories_and_files(directories_and_files)

    assert os.path.isdir(example_dir)
    assert os.path.isfile(example_file)


def test_store_repository_urls_in_corresponding_files(
    throwaway_dir, python_txt_file, test_repository
):
    if os.path.isfile(python_txt_file):
        os.remove(python_txt_file)

    # if os.path.isfile(f"{throwaway_dir}/JavaScript.txt"):
    #     os.remove(f"{throwaway_dir}/JavaScript.txt")
    #
    # if os.path.isfile(f"{throwaway_dir}/Emacs Lisp.txt"):
    #     os.remove(f"{throwaway_dir}/Emacs Lisp.txt")

    # test_url: list[str] = test_repository_list
    test_url: list[str] = [test_repository]

    sideroxylon.store_repository_urls_in_corresponding_files(
        test_url, throwaway_dir, "txt", 2, False
    )

    try:
        with open(python_txt_file, "r") as file:
            python_txt_contents: str = file.read().replace("\n", "")

    except OSError as e:
        print(f"Error reading {python_txt_file}: {e}")

    assert os.path.isfile(python_txt_file)
    assert python_txt_contents == "https://github.com/bormoge/sideroxylon"
