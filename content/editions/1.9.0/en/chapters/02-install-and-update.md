+++
id = "install-and-update"
group = "GET STARTED"
title = "Install and update"
lead = "Use a standalone download for everyday desktop use; Python is bundled."
wiki = "Getting-started"
+++

::: table {"widths": [0.25, 0.29, 0.46], "headers": true}
| Computer | Package | Install or open |
| --- | --- | --- |
| macOS Apple Silicon | macos-arm64.zip | Move Tagcast.app to Applications. |
| macOS Intel | macos-x64.zip | Move Tagcast.app to Applications. |
| Windows x64 | NSIS installer or windows-x64.zip | Install for this user, or extract the whole ZIP and run Tagcast.exe. |
| Debian / Ubuntu | linux-amd64.deb | Install with sudo apt install ./package.deb. |
| Linux x64 | linux-x64.tar.gz | Extract completely; run ./Tagcast in a graphical session. |
:::

Release packages identify **1.9.0**. macOS requires 13 Ventura or newer; Linux requires glibc 2.35 or newer. Use the [official 1.9.0 release](https://github.com/cyberdeliaAI/tagcast/releases/tag/v1.9.0) and its actual asset names, rather than GitHub's source-code archive, for a standalone app.

## Updating from 1.7.0 or 1.8.0

Install 1.9.0 manually first. Quit normally and wait for accepted changes and checks to finish before replacing the app. Keep the settings folder. The next chapter explains the update routes available from 1.9.0 for later stable releases.

## Homebrew and source use

On macOS: **brew install --cask cyberdeliaAI/apps/tagcast**. Later run **brew update**, then **brew upgrade --cask cyberdeliaAI/apps/tagcast**. The cask also provides **tagcast-cli --open**.

For source use, Python 3.11+ is required. From the repository, **uv run --frozen tagcast --open** starts the browser interface. The supplied platform start scripts are another option.

::: callout
Verify the download

Compare its SHA-256 with the accompanying checksum file. On macOS use **shasum -a 256 filename.zip**; on Linux use **sha256sum filename.tar.gz**; in PowerShell use **Get-FileHash .\filename.zip -Algorithm SHA256**.
:::

::: small
Official macOS distributions use Developer ID signing and Apple notarization. Windows packages remain unsigned; install or replace them manually. Check the selected release's notes and assets. Physical Wayland and every hardware/audio combination are not fully validated.
:::
