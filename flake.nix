{
  description = "eSquid discord bot";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells."x86_64-linux".default = pkgs.mkShellNoCC {
        buildInputs = with pkgs; [
          ruff
          (with python3Packages; [
            black
            discordpy
            isort
            setuptools
          ])
        ];
      };

      overlays.default = final: prev: {
        esquid = final.callPackage ./nix/pkgs { };
      };

      packages.${system} =
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ self.overlays.default ];
          };
        in
        {
          default = pkgs.esquid;
        };

      nixosModules.${system} = {
        eSquid = import ./nix/modules/eSquid.nix;
      };
    };
}
