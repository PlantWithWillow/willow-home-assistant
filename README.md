# Willow for Home Assistant

![Willow](assets/willow-icon.svg)

Willow is a Home Assistant custom integration for connected Willow plant sensors.

This repository is HACS-ready and currently stages the Willow integration code from Home Assistant Core under `custom_components/willow`.

Public repository: <https://github.com/PlantWithWillow/willow-home-assistant>

Current version: `1.0.0`

## Features

- OAuth2 configuration flow through the Home Assistant UI
- Cloud polling of Willow profile and paired sensor devices
- Battery, temperature, humidity, soil moisture, light, and last reading sensors
- Device registry entries for each paired Willow sensor

## Installation with HACS

1. Open Home Assistant.
2. Go to **HACS**.
3. Open the menu and select **Custom repositories**.
4. Add `https://github.com/PlantWithWillow/willow-home-assistant`.
5. Select **Integration** as the repository category.
6. Install **Willow**.
7. Restart Home Assistant.

## Manual installation

1. Copy `custom_components/willow` into your Home Assistant configuration directory:

   ```text
   config/custom_components/willow
   ```

2. Restart Home Assistant.

## Configuration

1. Go to **Settings** > **Devices & services**.
2. Select **Add integration**.
3. Search for **Willow**.
4. Complete the OAuth2 authorization flow.

## Build a GitHub release artifact

Run the release build script from the repository root:

```bash
python3 scripts/build_release.py --clean
```

The script reads the integration version from `custom_components/willow/manifest.json` and creates a HACS-installable zip file under `dist/`.

## Repository structure

```text
custom_components/
  willow/
    __init__.py
    application_credentials.py
    client.py
    config_flow.py
    const.py
    coordinator.py
    manifest.json
    sensor.py
assets/
  willow-icon.svg
  willow-icon.png
  willow-sensor-icon.svg
  willow-sensor-icon.png
scripts/
  build_release.py
hacs.json
README.md
```

## Before publishing

- Confirm `custom_components/willow/manifest.json` points to `https://github.com/PlantWithWillow/willow-home-assistant`.
- Keep Home Assistant brand assets in `assets/`; SVG and PNG versions are included for compatibility.
- Create a GitHub release for `1.0.0` to match the integration version in `manifest.json`.
- Add GitHub repository topics such as `home-assistant`, `hacs`, `custom-component`, and `willow`.

## Notes

The integration uses Willow's OAuth2 API and imports built-in application credentials automatically, so users should not need to manually enter client credentials during setup.
