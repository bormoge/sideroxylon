{
  description = "sideroxylon: A GitHub repository classifier.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      # Define dev shells for all supported systems
      devShells = forAllSystems (system: {
        default = self.buildShell { inherit system; };
      });

      # Function to build a dev shell for a given system
      buildShell = { system }:
        let pkgs = import nixpkgs { inherit system; };
        in pkgs.mkShell {
          buildInputs = with pkgs; [
            python314
            uv
            ty
            ruff
            black
          ];
        };
    };
}
