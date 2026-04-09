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
def test_repository():
    return "https://github.com/bormoge/sideroxylon"


@pytest.fixture
def test_repository_list():
    return [
        "https://github.com/bormoge/sideroxylon",
        "https://github.com/bormoge/spinosum",
        "https://github.com/bormoge/guava-themes",
    ]


def test_get_urls_inside_repository_url_file(throwaway_dir, test_repository_list):
    test_url_file = f"{throwaway_dir}/test_url_file.org"

    if not os.path.exists(test_url_file) or os.path.getsize(test_url_file) == 0:
        with open(test_url_file, "w") as file:
            for url in test_repository_list:
                file.write(url + "\n")

    assert (
        sideroxylon.get_urls_inside_repository_url_file(
            f"{throwaway_dir}/test_url_file.org"
        )
        == test_repository_list
    )


def test_write_into_file(throwaway_dir, test_repository):
    if os.path.isfile(f"{throwaway_dir}/Python.txt"):
        os.remove(f"{throwaway_dir}/Python.txt")

    sideroxylon.write_into_file(f"{throwaway_dir}/Python.txt", test_repository)

    with open(f"{throwaway_dir}/Python.txt", "r") as file:
        python_org_contents: str = file.read().replace("\n", "")

    assert os.path.isfile(f"{throwaway_dir}/Python.txt")
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
        throwaway_dir, test_repository
):
    if os.path.isfile(f"{throwaway_dir}/Python.txt"):
        os.remove(f"{throwaway_dir}/Python.txt")

    if os.path.isfile(f"{throwaway_dir}/JavaScript.txt"):
        os.remove(f"{throwaway_dir}/JavaScript.txt")

    if os.path.isfile(f"{throwaway_dir}/Emacs Lisp.txt"):
        os.remove(f"{throwaway_dir}/Emacs Lisp.txt")

    test_url: list[str] = [test_repository]

    sideroxylon.store_repository_urls_in_corresponding_files(
        test_url, f"{throwaway_dir}/token.org", throwaway_dir, "txt", 2
    )

    with open(f"{throwaway_dir}/Python.txt", "r") as file:
        python_org_contents: str = file.read().replace("\n", "")

    assert os.path.isfile(f"{throwaway_dir}/Python.txt")
    assert python_org_contents == "https://github.com/bormoge/sideroxylon"
