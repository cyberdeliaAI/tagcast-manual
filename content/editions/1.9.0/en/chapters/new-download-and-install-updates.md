+++
id = "download-and-install-updates"
group = "GET STARTED"
title = "Download and install updates"
lead = "Check the release, download its package and choose when to install."
wiki = "Updating-Tagcast"
+++

::: figure figure-102
Update dialog example. The illustrated 1.7.0 to 1.8.0 offer shows the interface; its version numbers are examples.
:::

Open **Settings > About & updates** to check manually. Release notes appear as plain text. Checking is separate from downloading, installing or enabling automatic package downloads.

**1.** Read the offered release and notes. Choose **Download update** where supported, **Later** to postpone, or **Skip this version** to suppress its automatic offer. A manual check can still show a skipped release.

**2.** A download can finish while you listen. Automatic package download is optional and starts off for a new profile. It is separate from the saved automatic stable-release check preference.

**3.** Choose **Restart and install** explicitly and accept the native confirmation. An ordinary Quit never installs a pending update. Tagcast waits for accepted writes and read-back; uncertain results postpone installation. **Keep Tagcast open** cancels that shutdown.

Supported official signed macOS apps can install later releases in-app. Homebrew uses **brew update**, then **brew upgrade --cask cyberdeliaAI/apps/tagcast**. A Debian/Ubuntu .deb installed in **/opt/Tagcast** asks for package-installation privileges. Windows installer/ZIP, Linux TAR and source/browser installations update manually.

::: small
Ad-hoc test apps or a desktop shell reusing another backend may also require manual installation. Packages come from GitHub without iBroadcast credentials. Public package SHA-256 checksums, updater SHA-512 checks and audio-download integrity files serve different purposes. Future signed upgrade chains still require release validation.
:::
