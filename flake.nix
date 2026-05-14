{
  description = "sideroxylon: A repository classifier.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
  };

  outputs = { self, nixpkgs }:
  let
    supportedSystems = [ "x86_64-linux" ];
    forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
  in
  {
    packages = forAllSystems (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        default = pkgs.python313Packages.callPackage ./default.nix { };
      }
    );

    devShells = forAllSystems (system:
      let pkgs = import nixpkgs { inherit system; };
      in {
        default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python313
            uv
            ty
            ruff
            black
            conventional-changelog-cli
            nixd
            nixfmt
          ];
        };
      }
    );
  };
}
