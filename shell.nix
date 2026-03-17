{
  pkgs ? import <nixpkgs> { },
}:
pkgs.callPackage (
  {
    mkShell,
    python314,
    uv,
    ty,
    ruff,
    black,
  }:
  mkShell {
    strictDeps = true;
    nativeBuildInputs = [
      python314
      uv
      ty
      ruff
      black
    ];
  }
) { }
