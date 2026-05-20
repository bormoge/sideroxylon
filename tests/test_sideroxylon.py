from sideroxylon import sideroxylon_main
from sideroxylon.sideroxylon_main import SideroxylonArgs
import os
import pytest
from pathlib import Path


@pytest.fixture
def test_dir():
    # directory = f"{sideroxylon_main.SIDEROXYLON_CACHE_HOME_DIR}/tests"
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
def config_file(throwaway_dir):
    file = f"{throwaway_dir}/config.json"
    Path(file).touch(exist_ok=True)
    return os.path.expanduser(file)


@pytest.fixture
def repository_url_file(throwaway_dir):
    file: str = f"{throwaway_dir}/repository_url_file.org"
    Path(file).touch(exist_ok=True)
    return file


@pytest.fixture
def languages_directory(throwaway_dir):
    directory = f"{throwaway_dir}/languages_directory"
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory


@pytest.fixture
def arg_urls():
    return ""


@pytest.fixture
def file_extension():
    return "txt"


@pytest.fixture
def sleep_time():
    return 1.0


@pytest.fixture
def verbose():
    return 0


@pytest.fixture
def args_list(
    config_file,
    env_file,
    repository_url_file,
    languages_directory,
    file_extension,
    sleep_time,
    verbose,
    arg_urls
):
    args_list: dict = {
        "config_file": config_file,
        "env_file": env_file,
        "repository_url_file": repository_url_file,
        "languages_directory": languages_directory,
        "file_extension": file_extension,
        "sleep_time": sleep_time,
        "verbose": verbose,
        "arg_urls": arg_urls,
    }
    return args_list


@pytest.fixture
def sid_args(args_list):
    sid_args: SideroxylonArgs = sideroxylon_main.SideroxylonArgs(
        args_list["env_file"],
        args_list["repository_url_file"],
        args_list["languages_directory"],
        args_list["file_extension"],
        args_list["sleep_time"],
        args_list["verbose"],
        args_list["arg_urls"],
    )
    return sid_args


@pytest.fixture
def repository_url_dict():
    repository_url_dict: dict[str, list[str]] = {}
    return repository_url_dict


@pytest.fixture
def test_repository_list():
    return [
        "https://github.com/bormoge/sideroxylon",
        "https://github.com/bormoge/spinosum",
        "https://github.com/bormoge/guava-themes",
        "https://github.com/bormoge/failure",
        "https://www.google.com/",
    ]


@pytest.fixture
def python_language_file(languages_directory, file_extension):
    return f"{languages_directory}/Python.{file_extension}"


@pytest.fixture
def javascript_language_file(languages_directory, file_extension):
    return f"{languages_directory}/JavaScript.{file_extension}"


@pytest.fixture
def emacs_lisp_language_file(languages_directory, file_extension):
    return f"{languages_directory}/Emacs_Lisp.{file_extension}"


@pytest.fixture
def github_url_language_file(languages_directory, file_extension):
    return f"{languages_directory}/GitHub_URL.{file_extension}"


@pytest.fixture
def unknown_language_file(languages_directory, file_extension):
    return f"{languages_directory}/Unknown.{file_extension}"


@pytest.fixture
def test_language_files_list(
    python_language_file,
    javascript_language_file,
    emacs_lisp_language_file,
    github_url_language_file,
    unknown_language_file,
):
    return [
        python_language_file,
        javascript_language_file,
        emacs_lisp_language_file,
        github_url_language_file,
        unknown_language_file,
    ]


@pytest.fixture
def test_repository_list_2():
    return [
        "https://github.com/ziglang/zig",
        "https://github.com/nim-lang/Nim",
        "https://github.com/odin-lang/Odin",
    ]


@pytest.fixture
def zig_language_file(languages_directory, file_extension):
    file: str = f"{languages_directory}/Zig.{file_extension}"
    Path(file).touch(exist_ok=True)
    return file


@pytest.fixture
def nim_language_file(languages_directory, file_extension):
    file: str = f"{languages_directory}/Nim.{file_extension}"
    Path(file).touch(exist_ok=True)
    return file


@pytest.fixture
def odin_language_file(languages_directory, file_extension):
    file: str = f"{languages_directory}/Odin.{file_extension}"
    Path(file).touch(exist_ok=True)
    return file


@pytest.fixture
def test_language_files_list_2(
    zig_language_file,
    nim_language_file,
    odin_language_file,
):
    return [
        zig_language_file,
        nim_language_file,
        odin_language_file,
    ]


# I don't think this one can be realistically tested outside
# of the developer's machine. Nevertheless, I'll leave it here
# for posteriority's sake.

# def test_load_sideroxylon_env_variables(env_file):
#     sideroxylon_main.load_sideroxylon_env_variables(env_file)
#
#     assert os.environ.get("SIDEROXYLON_GITHUB_TOKEN") is not None


def test_get_urls_inside_repository_url_file(repository_url_file, test_repository_list, arg_urls):
    if os.path.isfile(repository_url_file):
        os.remove(repository_url_file)

    if (
        not os.path.exists(repository_url_file)
        or os.path.getsize(repository_url_file) == 0
    ):
        try:
            with open(repository_url_file, "w") as file:
                for url in test_repository_list:
                    file.write(url + "\n")

        except OSError as e:
            print(f"Error reading {repository_url_file}: {e}")

    assert (
        sideroxylon_main.get_urls_inside_repository_url_file(repository_url_file, arg_urls)
        == test_repository_list
    )


def test_store_batches_in_memory(
    test_language_files_list, test_repository_list, repository_url_dict
):
    for language_file in test_language_files_list:
        if os.path.isfile(language_file):
            os.remove(language_file)

    for language_file, repository_url in zip(
        test_language_files_list, test_repository_list
    ):
        sideroxylon_main.store_batches_in_memory(
            language_file, repository_url, repository_url_dict
        )

    for language_file, repository_url in zip(
        test_language_files_list, test_repository_list
    ):
        assert repository_url_dict[language_file] == [repository_url]


def test_initialize_directories_and_files(repository_url_file, languages_directory):
    directories_and_files: dict[str, list[str]] = {
        "directories": [languages_directory],
        "files": [repository_url_file],
    }

    for filename in os.listdir(languages_directory):
        file_path = os.path.join(languages_directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    if os.path.isdir(languages_directory):
        os.rmdir(languages_directory)

    if os.path.isfile(repository_url_file):
        os.remove(repository_url_file)

    sideroxylon_main.initialize_directories_and_files(directories_and_files)

    assert os.path.isdir(languages_directory)
    assert os.path.isfile(repository_url_file)


def test_assign_sideroxylon_variables(args_list, sid_args):
    assert sideroxylon_main.assign_sideroxylon_variables(args_list) == sid_args


def test_handle_repository_urls(
    test_language_files_list, test_repository_list, sid_args
):
    for language_file in test_language_files_list:
        if os.path.isfile(language_file):
            os.remove(language_file)

    sideroxylon_main.handle_repository_urls(test_repository_list, sid_args)

    file_dict: dict[str, str] = {}

    try:
        for language_file in test_language_files_list:
            with open(language_file, "r") as file:
                file_dict[language_file] = file.read().replace("\n", "")

    except OSError as e:
        print(f"Error reading {language_file}: {e}")

    for language_file, repository_url in zip(
        test_language_files_list, test_repository_list
    ):
        assert os.path.isfile(language_file)
        assert file_dict[language_file] == repository_url


def test_clean_repository_url_file(repository_url_file):
    try:
        with open(repository_url_file, "w") as file:
            file.write(
                "This is a test.\nTo check the function clean_repository_url_file."
            )

    except OSError as e:
        print(f"Error reading {repository_url_file}: {e}")

    assert os.path.getsize(repository_url_file) != 0

    sideroxylon_main.clean_repository_url_file(
        repository_url_file, [repository_url_file], os.path.getsize(repository_url_file)
    )

    # "0" means no lines, "1" means one empty line
    assert (
        os.path.getsize(repository_url_file) == 1
        or os.path.getsize(repository_url_file) == 0
    )


def test_sideroxylon(
    args_list,
    repository_url_file,
    test_language_files_list_2,
    test_repository_list_2,
):
    if os.path.isfile(repository_url_file):
        os.remove(repository_url_file)

    for language_file in test_language_files_list_2:
        if os.path.isfile(language_file):
            os.remove(language_file)

    if (
        not os.path.exists(repository_url_file)
        or os.path.getsize(repository_url_file) == 0
    ):
        try:
            with open(repository_url_file, "w") as file:
                for url in test_repository_list_2:
                    file.write(url + "\n")

        except OSError as e:
            print(f"Error reading {repository_url_file}: {e}")

    sideroxylon_main.sideroxylon(*list(args_list.values()))

    file_dict: dict[str, str] = {}

    try:
        for language_file in test_language_files_list_2:
            with open(language_file, "r") as file:
                file_dict[language_file] = file.read().replace("\n", "")

    except OSError as e:
        print(f"Error reading {language_file}: {e}")

    for language_file, repository_url in zip(
        test_language_files_list_2, test_repository_list_2
    ):
        assert os.path.isfile(language_file)
        assert file_dict[language_file] == repository_url
