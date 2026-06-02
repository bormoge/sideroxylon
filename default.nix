{
  pkgs,
  lib,
  buildPythonPackage,
  fetchPypi,

  # build-system
  hatchling,

  # dependencies

  # tests
  pytestCheckHook,
}:

buildPythonPackage rec {
  pname = "sideroxylon";
  version = "0.2.5";
  # format = "pyproject";
  pyproject = true;

  # Update when necessary

  # src = fetchPypi {
  #   inherit pname version;
  #   hash = "sha256-1luMdGApfVbtZTodPAUtqdE1wCyfWn1fnIjC8hIPfjU=";
  # };

  src = lib.cleanSource ./.;

  postPatch = "";

  build-system = [
    hatchling
  ];

  dependencies = [ ];

  nativeCheckInputs = [
    pytestCheckHook
  ];

  doCheck = true;

  disabledTests = [
    # These tests require a network connection.
    "test_handle_repository_urls"
    "test_sideroxylon_main_function"
    "test_fetch_forge_repository_data"
    "test_get_repository_programming_language"
  ];

  pythonImportsCheck = [ "sideroxylon" ];

  meta = {
    description = "A repository classifier.";
    homepage = "https://github.com/bormoge/sideroxylon";
    # changelog = "https://github.com/bormoge/sideroxylon/releases/tag/v${version}";
    changelog = "https://github.com/bormoge/sideroxylon/blob/main/CHANGELOG.md";
    license = lib.licenses.gpl3Plus;
    mainProgram = "sideroxylon";
    maintainers = with lib.maintainers; [ ];
  };
}
