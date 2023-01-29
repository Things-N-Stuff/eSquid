{
  description = "eSquid flake";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
  let pkgs = import nixpkgs { system = "x86_64-linux"; };
  in {
    devShells.x86_64-linux.default = pkgs.mkShell {
      buildInputs = with pkgs; [
        (with python3Packages; [
          python
          discordpy

          pyls-isort
          pylsp-mypy
          python-lsp-black
          python-lsp-server
          #python-lsp-server.optional-dependencies.pycodestyle
          #python-lsp-server.optional-dependencies.pydocstyle
          python-lsp-server.optional-dependencies.pylint
          python-lsp-server.optional-dependencies.rope
        ])
      ];
    };
  };
}
