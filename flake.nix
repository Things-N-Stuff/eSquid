{
  description = "eSquid discord bot";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem(system:
    let
      pkgVersion = "0.0.1";

      pkgs = nixpkgs.legacyPackages.${system};
      lib = nixpkgs.lib;

      deps = with pkgs; [ ];

      pythonDeps = with pkgs.python3Packages; [
        discordpy
        setuptools
      ];

      devDeps = with pkgs; [
        ruff
        (with python3Packages; [
          black
          isort
        ])
      ];
    in {


      # Development environment (nix develop)
      devShells.default = pkgs.mkShellNoCC {
        buildInputs = deps ++ pythonDeps ++ devDeps;
      };

      # eSquid package (nix build)
      packages.default = pkgs.python3Packages.buildPythonApplication rec {
        pname = "eSquid";
        version = pkgVersion;

        src = ./.;
        format = "pyproject";

        buildInputs = deps;
        propagatedBuildInputs = pythonDeps;

        meta = {
          homepage = "https://github.com/Things-N-Stuff/eSquid";
          description = "A discord bot providing some quality of life for small servers";
          license = lib.licenses.bsd0;
        };
      };

      # TODO: service
      # eSquid service module
      # nixosModules.default =

      # TODO: overlay?
      # eSquid overlay
      #overlays.default = {};

      # Run eSquid (nix run . -- -a ... -g ... -t ...)
      # -a, --admins <admin-id-1>,<admin-id-2>,<admin-id-3>,...
      # -g, --guild <initial-guild-id>
      # -t, --token <bot-token>
      apps.default = {
        type = "app";
        program = "${self.packages.${system}.default}/bin/esquid";
      };
    });
}
