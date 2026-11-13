+++
id = "install-and-update"
group = "GET STARTED"
title = "Install and update"
lead = "Use a standalone download for everyday desktop use; Python is bundled."
wiki = "Getting-started"
+++

::: table {"widths": [0.25, 0.27, 0.48], "headers": true}
| Computer | Download suffix | Open after extraction |
| --- | --- | --- |
| macOS Apple Silicon | macos-arm64.zip | Move Tagcast.app to Applications. |
| macOS Intel | macos-x64.zip | Move Tagcast.app to Applications. |
| Windows x64 | windows-x64.zip | Run Tagcast.exe; keep its folder complete. |
| Debian / Ubuntu | linux-amd64.deb | Install with sudo apt install ./package.deb. |
| Linux x64 | linux-x64.tar.gz | Run ./Tagcast in a graphical session. |
:::

The complete package name starts with **tagcast-1.7.0-**. macOS requires 13 Ventura or newer; Linux requires glibc 2.35 or newer. Use the [official Releases page](https://github.com/cyberdeliaAI/tagcast/releases), rather than GitHub's source-code archive, for a standalone app.

## Updating

Quit the older app, extract the new download and replace the application while preserving your user settings. Tagcast checks for stable updates when enabled, but does not install them automatically. **Settings > About & updates** offers a manual check and the release link.

## Homebrew and source use

On macOS: **brew install --cask cyberdeliaAI/apps/tagcast**. Later run **brew update**, then **brew upgrade --cask cyberdeliaAI/apps/tagcast**. The cask also provides **tagcast-cli --open**.

For source use, Python 3.11+ is required. From the repository, **uv run --frozen tagcast --open** starts the browser interface. The supplied platform start scripts are another option.

::: callout
Verify the download

Compare its SHA-256 with the accompanying checksum file. On macOS use **shasum -a 256 filename.zip**; on Linux use **sha256sum filename.tar.gz**; in PowerShell use **Get-FileHash .\\filename.zip -Algorithm SHA256**.
:::

::: small
Official macOS distributions use Developer ID signing and Apple notarization. Check the selected release's notes and available assets; Windows signing is not yet active. Tagcast 1.7.0 is published. Windows code signing remains deferred; physical Wayland and every hardware/audio combination are not fully validated.
:::
