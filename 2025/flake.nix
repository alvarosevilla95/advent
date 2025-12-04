{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs:
    inputs.flake-parts.lib.mkFlake {inherit inputs;} {
      systems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];

      perSystem = {pkgs, ...}: let
        pythonEnv = pkgs.python3.withPackages (ps: [
          ps.numpy
          ps.scipy
        ]);
      in {
        devShells.default = pkgs.mkShell {
          packages = [pythonEnv];
          env.PYTHONPATH = "${pythonEnv}/${pythonEnv.sitePackages}";
        };
      };
    };
}

