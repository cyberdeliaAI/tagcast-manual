+++
id = "mini-player-sound-and-quality"
group = "LISTEN"
title = "Mini Player, sound and quality"
lead = "Keep compact playback visible, and choose the output and stream that suit your setup."
wiki = "Playback-and-queue#desktop-mini-player"
+++

::: figure figure-005
1.7.0: native Mini Player; Pin and return to the main window stay separate.
:::

Open it from **View > Open Mini Player**, **Cmd/Ctrl+Shift+M**, or expanded Now playing. It hides the main window. **Open Tagcast**, closing the Mini Player or returning to the main window restores the full interface. Playback uses the same engine. Pin keeps it above other windows where supported; Linux/Wayland does not offer Pin. Window size and Pin are remembered.

## Output and volume

Open **Sound** from the output/speaker-cabinet button for player volume, mute and available outputs. If a browser cannot change volume or select a device, use your system controls. This is not direct Sonos or Chromecast control.

For AirPlay in the macOS Electron app, leave Tagcast on **System default** and choose the AirPlay device in **macOS Control Centre > Sound**. This routes system audio, including other apps. Safari may offer its own route picker.

## File format is not stream quality

**Settings > Playback > Streaming quality** applies on the next track after Save. Free accounts use MP3 128 kbps. Premium adds other offered bitrates and Original. A FLAC upload may still be playing as MP3; read the File and Stream labels. If Original cannot play, Tagcast can try MP3 128 kbps once and labels the fallback.
