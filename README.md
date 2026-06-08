# Willow for Home Assistant

![Willow](assets/willow-icon.svg)

Willow is a Home Assistant custom integration for connected Willow plant sensors.

This repository is HACS-ready and currently stages the Willow integration code from Home Assistant Core under `custom_components/willow`.

Public repository: <https://github.com/PlantWithWillow/willow-home-assistant>

Current version: `1.0.1`

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

> **Important:** Because `hacs.json` sets `"zip_release": true`, HACS extracts the contents of `willow-home-assistant.zip` **directly into** `config/custom_components/willow/`. The release zip must therefore contain the integration files (`manifest.json`, `__init__.py`, ...) at its **root**, not nested under `custom_components/willow/`. `build_release.py` produces this layout. If the files are nested, Home Assistant won't find `manifest.json` and the integration will never appear in the **Add integration** list even though HACS shows it as downloaded.

## Integration icon (local brand images)

The icon shown in the HACS list and the **Add integration** page is **not** read from `icons.json` (which only controls entity icons). Since Home Assistant **2026.3**, custom integrations can ship their own brand images in a `brand/` directory inside the integration, and these take priority over the brands CDN — no `home-assistant/brands` pull request is needed.

The assets live at `custom_components/willow/brand/` and are bundled into the HACS release zip automatically:

```text
custom_components/willow/brand/
  icon.png      # 256x256
  icon@2x.png   # 512x512
```

Supported filenames are `icon.png`, `icon@2x.png`, `logo.png`, `logo@2x.png` and their `dark_` variants. After installing/updating via HACS and restarting, the Willow icon replaces the default puzzle icon (a browser refresh may be needed).

> Requires Home Assistant **2026.3 or newer** for local brand images. On older versions the default puzzle icon is shown unless the integration is registered in the `home-assistant/brands` CDN repo.

## Repository structure

```text
custom_components/
  willow/
    __init__.py
    api.py
    application_credentials.py
    client.py
    config_flow.py
    const.py
    coordinator.py
    exceptions.py
    icons.json
    manifest.json
    sensor.py
    strings.json
    brand/
      icon.png
      icon@2x.png
    translations/
      en.json
assets/
  willow-icon.svg
  willow-icon.png
  willow-brand.svg
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
- Keep `custom_components/willow/brand/` icons in place; they ship in the HACS zip and provide the integration icon on Home Assistant 2026.3+ (see the Integration icon section above).
- Create a GitHub release whose tag matches the integration version in `manifest.json` (currently `1.0.1`). The release **must** attach the `dist/willow-home-assistant.zip` artifact built by `scripts/build_release.py`, since `hacs.json` uses `zip_release`.
- Add GitHub repository topics such as `home-assistant`, `hacs`, `custom-component`, and `willow`.

## Notes

The integration uses Willow's OAuth2 API and imports built-in application credentials automatically, so users should not need to manually enter client credentials during setup.
