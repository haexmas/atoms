{
  description = "Reproducible Nix devShell skeleton, delivered by spaex";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # Blanket allow, not a per-package predicate: `cudatoolkit` (pulled
        # in by consumers like `com.github.haexmas.atoms.holzi` for local
        # CUDA builds) is a meta-package bundling several separately
        # unfree-licensed sub-derivations (cuda_nvcc, cuda_cuobjdump, ...),
        # so scoping to one name is not enough and the set of names is not
        # stable across nixpkgs bumps. Revisit if a consumer ever needs
        # finer-grained control.
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        # spaex regenerates this from every currently-adopted molecule's
        # `nix_packages` fragment (spaex Spec 027's composable atom
        # category). Absent when no adopted molecule declares one — that
        # is a valid "no extra packages" state, not an error.
        generatedPackagesPath = ./.spaex/generated/nix-packages.json;
        packageNames =
          if builtins.pathExists generatedPackagesPath
          then builtins.fromJSON (builtins.readFile generatedPackagesPath)
          else [ ];
        packages = map (name: pkgs.${name}) packageNames;
      in
      {
        devShells.default = pkgs.mkShell {
          inherit packages;
        };
      });
}
