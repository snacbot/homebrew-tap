# snacbot/homebrew-tap

Homebrew casks for [Khaos Studios](https://khaosstudio.com) apps.

## Install

```sh
brew install --cask snacbot/tap/delve
```

Homebrew adds the tap automatically on first use.

## Casks

| Cask | App | Requires |
|---|---|---|
| `delve` | [Delve](https://khaosstudio.com/delve/) — disk space analyzer with a GPU-rendered treemap | macOS 26+, Apple Silicon |

## Updating on release

Delve auto-updates through Sparkle, so the cask is `auto_updates true` — Homebrew won't
fight the in-app updater. The cask still needs a version/sha bump each release so fresh
installs get the current build:

```sh
VERSION=0.8.13
SHA=$(curl -sL "https://github.com/snacbot/delve-releases/releases/download/v$VERSION/Delve-$VERSION.dmg" | shasum -a 256 | cut -d' ' -f1)
sed -i '' "s/version \".*\"/version \"$VERSION\"/; s/sha256 \".*\"/sha256 \"$SHA\"/" Casks/delve.rb
```

Verify before pushing — `brew fetch` re-downloads and checks the sha:

```sh
brew fetch --cask snacbot/tap/delve
```

## Why a tap and not homebrew-cask core

homebrew-cask has a [notability requirement](https://docs.brew.sh/Acceptable-Casks) for new
submissions. Once Delve clears it, the same cask file can be submitted upstream and this tap
retired.
