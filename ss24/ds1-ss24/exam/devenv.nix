{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  # env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = with pkgs;[
    git
    pyright
    ruff
    # ruff-lsp
    black
  ];
  # https://devenv.sh/scripts/
  scripts.build_server.exec = "docker build -t exam-env .";
  scripts.run_server.exec = "docker run -p 8888:8888 -v $(pwd):/home/jovyan/work exam-env:latest";

  # enterShell = ''
  #   hello
  #   git --version
  # '';

  # https://devenv.sh/tests/
  # enterTest = ''
  #   echo "Running tests"
  #   git --version | grep "2.42.0"
  # '';

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/languages/
  # languages.nix.enable = true;
  languages.python = {
    enable = true;
    # uv.enable = true;
    venv.enable = true;
    venv.requirements = ''
      pandas
      seaborn
      numpy
      scipy
      scikit-learn
      matplotlib
      geopy
      openpyxl
      git+https://github.com/sinzlab/dsplotter.git
    '';
  };

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # https://devenv.sh/processes/
  # processes.ping.exec = "ping example.com";

  # See full reference at https://devenv.sh/reference/options/
}
