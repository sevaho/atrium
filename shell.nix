{pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
    packages = [
        pkgs.envsubst
        pkgs.kubernetes-helm
        pkgs.kubeseal
        pkgs.pulumi-bin
        pkgs.pulumiPackages.pulumi-language-python

        pkgs.python312

        (pkgs.poetry.override { python3 = pkgs.python312; })

        (pkgs.python312.withPackages (p: with p; [
            pip
            pipx
            cryptography

            # Ansible
            ansible
            ansible-core
            hvac

            # IDE config
            python-lsp-server
            pynvim
            pyls-isort
            python-lsp-black
        ]))
    ];

    LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath [
        pkgs.stdenv.cc.cc
    ]}";

    shellHook = ''
        set -a; source .env; set +a
        echo "SHELLHOOK LOG: .env loaded to ENV variables"
    '';
}
