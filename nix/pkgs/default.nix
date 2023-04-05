{ pkgs, lib, ... }:

pkgs.python3Packages.buildPythonApplication {
  pname = "eSquid";
  version = "0.0.1";

  src = ../..;
  format = "pyproject";

  buildInputs = with pkgs; [
    (with python3Packages; [
      setuptools
    ])
  ];

  propagatedBuildInputs = with pkgs; [
    (with pkgs.python3Packages; [
      discordpy
    ])
  ];

  meta = {
    description = "A discord bot providing some quality of life for small servers";
    homepage = "https://github.com/Things-N-Stuff/eSquid";
    license = lib.licenses.bsd0;
    mainProgram = "esquid";
  };
}
