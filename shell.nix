# shell.nix
let
  pkgs = import <nixpkgs> {};
  unstable = import (fetchTarball https://nixos.org/channels/nixpkgs-unstable/nixexprs.tar.xz) {};
in pkgs.mkShell {
  shellHook = ''
    if [ -f .venv/bin/activate ]; then
      source .venv/bin/activate

      set -a; source .env; set +a
      echo "SHELLHOOK LOG: .env loaded to ENV variables"
    fi
  '';

  packages = with pkgs; [
    envsubst
    kubernetes-helm
    kubeseal
    pulumi-bin
    pulumiPackages.pulumi-language-python

    python314
  ];

    LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath [
        pkgs.stdenv.cc.cc
    ]}";
}
