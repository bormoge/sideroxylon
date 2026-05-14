{
  pkgs,
  lib,
  buildPythonPackage,
  fetchPypi,

  # build-system
  hatchling,

  # dependencies

  # tests
}:

buildPythonPackage rec {
  pname = "sideroxylon";
  version = "0.2.4";
  format = "pyproject";
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

  nativeCheckInputs = [ ];

  doCheck = false;

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
