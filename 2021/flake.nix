{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils/master";
    rust-overlay.url = "github:oxalica/rust-overlay";
  };

  outputs = inputs: with inputs;
  flake-utils.lib.eachDefaultSystem (system:
  let
    overlays = [ (import rust-overlay) ];
    pkgs = import nixpkgs {
      inherit system overlays;
    };
  in
  with pkgs; rec {
    devShell = pkgs.mkShell {
      packages = [
        cargo
        libiconv
        darwin.apple_sdk.frameworks.Cocoa
        rust-bin.nightly.latest.default
      ];
    };

    defaultPackage = rustPlatform.buildRustPackage rec {
      pname = "advent_2021";
      version = "1.0.0";
      buildInputs = [ libiconv darwin.apple_sdk.frameworks.Cocoa rust-bin.nightly.latest.default ];
      nativeBuildInputs = [ libiconv darwin.apple_sdk.frameworks.Cocoa rust-bin.nightly.latest.default ];
      src = ./.;
      doInstallCheck = true;
      cargoLock.lockFile = ./Cargo.lock;
      meta = with lib; {
        description = "";
        homepage = "";
        license = with licenses; [ unlicense /* or */ mit ];
        maintainers = with maintainers; [ tailhook globin ma27 zowoq ];
        mainProgram = "advent_2021";
      };
    };
  }
  );
}
