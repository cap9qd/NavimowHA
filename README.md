# Navimow for Home Assistant

<p align="center">
  <img src="https://fra-navimow-prod.s3.eu-central-1.amazonaws.com/img/navimowhomeassistant.png" width="600">
</p>

A feature-rich Home Assistant custom integration for **Segway Navimow** robotic lawn mowers.
This is a community fork of the [official integration](https://github.com/segwaynavimow/NavimowHA) with significantly extended functionality.

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![GitHub Release](https://img.shields.io/github/v/release/cap9qd/NavimowHA)](https://github.com/cap9qd/NavimowHA/releases)
[![License](https://img.shields.io/github/license/cap9qd/NavimowHA)](LICENSE)

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=cap9qd&repository=NavimowHA&category=Integration)

---

> **Using the official Navimow integration?**  
> This fork uses the integration domain `navimow_ha` (folder: `custom_components/navimow_ha/`).  
> It is fully independent of the official `navimow` integration and can be installed alongside it without conflict.  
> If you are **migrating from the official integration**, remove the old integration entry from  
> **Settings → Devices & Services** first, then add this one.

---

## 🚀 Quick Start in 5 Minutes

> New here? Follow this guide — from installation to your first map.

### Step 1 — Install Integration

1. Open **HACS** → **Integrations** → Top right menu → **Custom repositories**
2. Enter URL: `https://github.com/cap9qd/NavimowHA` · Category: **Integration** · **Add**
3. Search for **Navimow** in HACS and click **Download**
4. **Restart Home Assistant**

### Step 2 — Set up Integration

1. **Settings → Devices & Services → Add Integration**
2. Search for and select **Navimow**
3. Click **Confirm** → Navimow login page opens
4. Log in with your Navimow / Segway account
5. HA automatically detects your mower — done!

> No API key needed. Authentication runs via OAuth2.

### Step 3 — Add Dashboard Card

The **Navimow Card** is **automatically registered** by the integration — no additional HACS frontend installation needed.

1. Open your dashboard → Pencil icon (Edit) → **Add Card**
2. Search for **Navimow** → Select **Navimow Mower Card**
3. A form editor appears:

   **Entity prefix** — this is the middle part of your sensor IDs:
   - Go to **Developer Tools → States**
   - Search for `navimow`
   - Example: `sensor.navimow_m550_battery` → prefix is **`navimow_m550`**
   - Enter this value in the field

4. **Save** — the card appears immediately with live map and controls

That's it! 🎉

---

## Features

| Feature | Official | This Fork (HTTP) | This Fork (MQTT) |
|---------|----------|------------------|------------------|
| `lawn_mower` entity (start/pause/dock/resume) | ✅ | ✅ | ✅ |
| Battery sensor | ✅ | ✅ | ✅ |
| Status sensor | – | ✅ | ✅ |
| Signal strength sensor | – | ❌ | ✅ |
| Position tracking (X/Y/heading) | – | ❌ | ✅ |
| Device tracker on HA map | – | ❌ | ✅ |
| Error sensors (code + message) | – | ❌ | ✅ |
| Work statistics (time + area) | – | ❌ | ✅ |
| Binary sensors (error/charging/mowing/docked/returning) | – | ✅ | ✅ |
| Cutting height — number slider | – | ❌ | ✅ |
| Cutting height — select dropdown | – | ❌ | ✅ |
| Edge mowing switch | – | ❌ | ✅ |
| Rain mode switch | – | ❌ | ✅ |
| Anti-theft switch | – | ❌ | ✅ |
| Locate button (make mower beep) | – | ✅ | ✅ |
| Restart button | – | ✅ | ✅ |
| Real-time MQTT updates | – | ❌ | ✅ |
| Automatic token + MQTT credential refresh | – | ✅ | ✅ |
| HTTP fallback when MQTT is stale | – | ✅ | ✅ |
| **Custom Lovelace card** (auto-registered, GUI config) | – | ✅ | ✅ |
| **Live SVG map** with animated mower icon | – | ❌ | ✅ |

> **Note:** Some mower models (including X450) don't send position, metrics, or attribute data via MQTT. These models use HTTP polling mode and have limited features (marked ❌). Models that support full MQTT data have access to all features (marked ✅).

---

## Requirements

- Home Assistant **2026.1.0** or newer
- A **Segway Navimow** robotic mower with an active cloud account
- [HACS](https://hacs.xyz) for installation

---

## Installation

### HACS (recommended)

1. Open **HACS** → **Integrations** → top-right menu → **Custom repositories**
2. Add: `https://github.com/cap9qd/NavimowHA` — Category: **Integration**
3. Search for **Navimow** in HACS and install it
4. **Restart Home Assistant**
5. Go to **Settings** → **Devices & Services** → **Add Integration** → search for **Navimow**

### Manual

1. Download the latest release from the [Releases page](https://github.com/cap9qd/NavimowHA/releases)
2. Copy the `custom_components/navimow_ha/` directory into your HA `custom_components/` folder
3. Restart Home Assistant
4. Add the integration via **Settings** → **Devices & Services**

---

## Configuration

Authentication is handled via **OAuth2** — no API keys need to be entered manually:

1. Click **Add Integration** and search for **Navimow**
2. Click **Confirm** to open the Navimow login page
3. Log in with your Navimow / Segway account
4. You are redirected back to Home Assistant automatically

The integration discovers all mowers linked to your account and creates entities for each one.

---

## Entities

### Lawn Mower (`lawn_mower`)

The primary control entity. Supports:

| Action | Description |
|--------|-------------|
| Start | Send the mower out to mow |
| Pause | Pause at current location |
| Resume | Continue from paused position |
| Dock | Return to charging station |

**States**: `mowing`, `paused`, `docked`, `returning`, `error`

---

### Sensors

| Sensor | Unit | Description |
|--------|------|-------------|
| Battery | % | Current battery charge level |
| Signal Strength | % | GNSS satellite signal quality |
| Status | – | Raw mower status string |
| Position X | m | Local map X coordinate (from charging station) |
| Position Y | m | Local map Y coordinate (from charging station) |
| Heading | rad | Mower orientation in radians |
| Error Code | – | Active error code, if any |
| Error Message | – | Human-readable error description |
| Work Time | s | Total cumulative mowing time |
| Work Area | m² | Total cumulative mowed area |
| Last Update | – | Timestamp of the last state message |

> **Note**: Position X/Y are **local coordinates** (metres from the charging station), not GPS coordinates.
> They can still be used with the HA map card for relative positioning.

---

### Binary Sensors

| Sensor | Device Class | Description |
|--------|-------------|-------------|
| Error | Problem | `on` when an error is active |
| Charging | Battery Charging | `on` when at the station and charging |
| Mowing | – | `on` when actively mowing |
| Docked | – | `on` when docked at the station |
| Returning | – | `on` when driving back to the station |

---

### Number Entity

| Entity | Range | Step | Description |
|--------|-------|------|-------------|
| Cutting Height | 25–80 mm | 5 mm | Set the blade height via a slider |

---

### Select Entity

| Entity | Options | Description |
|--------|---------|-------------|
| Cutting Height (Select) | 25–80 mm | Set the blade height via a dropdown |

> The **number entity** (slider) is the recommended way to adjust the cutting height.
> The select entity is kept for dashboard card compatibility.

---

### Switches

| Switch | Description |
|--------|-------------|
| Edge Mowing | Toggle perimeter / edge mowing pass |
| Rain Mode | Allow or block mowing in rain |
| Anti-Theft | Enable or disable the theft alarm |

---

### Buttons

| Button | Description |
|--------|-------------|
| Locate | Make the mower beep/buzz so you can find it |
| Restart | Restart the mower firmware |

---

### Device Tracker

The mower appears as a GPS tracker entity on the **HA Map** card.  
Because the coordinates are local (metres relative to the charging station), the absolute
position on a world map will not be geographically accurate — but the relative movement
and mowing path are fully visible.

Extra attributes exposed:

- `posture_x` / `posture_y` — raw coordinates in metres
- `posture_theta` — heading in radians
- `map_id` — internal map identifier, if available

---

## Architecture

```
Home Assistant
  └── Navimow Integration  (custom_components/navimow_ha/)
        ├── sensor.py          — 11 sensor entities
        ├── binary_sensor.py   — 5 binary sensors
        ├── number.py          — cutting height slider
        ├── select.py          — cutting height dropdown
        ├── switch.py          — 3 feature switches
        ├── button.py          — locate + restart buttons
        ├── device_tracker.py  — position on HA map
        ├── lawn_mower.py      — main control entity
        ├── coordinator.py     — shared data + token refresh
        │     ├── MQTT (primary)   — real-time push via WebSocket
        │     └── REST API (fallback) — polled after 5 min silence
        └── www/
              └── navimow-card.js — custom Lovelace card (auto-registered)
```

### Data Flow

1. **MQTT (primary)**: Real-time state pushes via WebSocket.
   - Position, status, battery, signal — updated every few seconds.
   - Automatic reconnection with exponential back-off (1–60 s).
   - 40-minute MQTT keepalive to survive hourly broker disconnects.

2. **HTTP fallback**: Polled when no MQTT message has been received for 5+ minutes.
   - Rate-limited to once per hour to avoid API abuse.

3. **Token refresh**: The OAuth2 token is proactively refreshed on every coordinator
   update cycle (every 30 s). After a reconnect, MQTT credentials (username/password)
   are re-fetched from the server because they are tied to the access token.

---

## Example Automations

### Start mowing at sunrise

```yaml
automation:
  - alias: "Navimow – Start at sunrise"
    trigger:
      - platform: sun
        event: sunrise
        offset: "+00:30:00"
    condition:
      - condition: state
        entity_id: binary_sensor.navimow_charging
        state: "on"
    action:
      - service: lawn_mower.start_mowing
        target:
          entity_id: lawn_mower.navimow
```

### Dock when rain detected

```yaml
automation:
  - alias: "Navimow – Dock on rain"
    trigger:
      - platform: state
        entity_id: sensor.weather_condition
        to: "rainy"
    condition:
      - condition: state
        entity_id: binary_sensor.navimow_mowing
        state: "on"
    action:
      - service: lawn_mower.dock
        target:
          entity_id: lawn_mower.navimow
```

### Notify on mower error

```yaml
automation:
  - alias: "Navimow – Error notification"
    trigger:
      - platform: state
        entity_id: binary_sensor.navimow_error
        to: "on"
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Navimow Error"
          message: "Error: {{ states('sensor.navimow_error_message') }}"
```

### Test MQTT data quality (diagnostic)

Run this service to test if your mower model sends data via MQTT (position, metrics, etc.):

```yaml
service: navimow_ha.test_mqtt_data
data:
  duration: 60                    # Test duration in seconds (10-300)
  persistent_notification: true   # Show results in HA notifications
  send_notification: false        # Send to mobile app (optional)
```

Results appear in **Notifications** and are stored in `hass.data['navimow_ha']['mqtt_test_results']`.

**Note:** Some mower models (including X450) don't send position/metrics data via MQTT. These models rely on HTTP polling for state and battery data.

### Automatically test MQTT when mowing starts

This automation tests MQTT data quality after the mower has been running for 5 minutes:

```yaml
automation:
  - alias: "Navimow – Test MQTT when mowing starts"
    trigger:
      - platform: state
        entity_id: lawn_mower.navimow_YOUR_DEVICE_ID
        to: "mowing"
        for: "00:05:00"  # Wait 5 minutes after mowing starts
    action:
      - service: navimow_ha.test_mqtt_data
        data:
          duration: 60
          persistent_notification: true
```

Replace `YOUR_DEVICE_ID` with your actual device ID (e.g., `navimow_m550`).

---

## Dashboard Card

This integration includes a **custom Lovelace card** (`custom:navimow-card`) that is
**automatically registered** when the integration starts — no manual resource setup needed.

### Add the card

1. Edit your dashboard → **Add Card** → search **Navimow**
2. The **Navimow Mower Card** appears in the card picker
3. A GUI editor opens: enter the entity prefix and configure which sections to show

**Minimal YAML** (if added manually):
```yaml
type: custom:navimow-card
entity_prefix: navimow_m550   # prefix from sensor.navimow_m550_battery
```

### Card sections

| Section | Content |
|---------|---------|
| Live map | Animated SVG — mower pulsates while mowing, blade rotates, direction arrow, battery bar |
| Controls | Start / Pause / Return to base / Locate — highlight when active |
| Statistics | Battery %, mowing time, mowed area |
| Settings | Cutting height (±5 mm buttons), edge mowing, rain mode, anti-theft |
| Error bar | Shows error code + message when a fault is active |

### Config options

| Option | Default | Description |
|--------|---------|-------------|
| `entity_prefix` | *(required)* | e.g. `navimow_m550` |
| `range` | `12` | Map radius in metres — adjust to your lawn size |
| `show_map` | `true` | Show the live SVG map |
| `show_controls` | `true` | Show control buttons |
| `show_stats` | `true` | Show statistics row |
| `show_settings` | `false` | Show settings panel |

### Finding your entity prefix

Go to **Developer Tools → States** and search for `navimow`.
Take any sensor ID, e.g. `sensor.navimow_m550_battery` → prefix is `navimow_m550`.

### Full dashboard YAML

A complete multi-section Lovelace view (title + chips, map, gauge + mini graph,
control buttons, settings, error card) is also available in
[dashboard-cards.yaml](custom_components/navimow_ha/dashboard-cards.yaml).
This version uses Mushroom Cards, Button Card and Mini Graph Card from HACS.

---

## Troubleshooting

### Integration not found after installation

Make sure you restart Home Assistant after copying the files.

### Authentication fails / Re-authentication required

Navimow access tokens are valid for ~24-48 hours. If the token expires and a refresh
fails, HA will prompt you to re-authenticate. Open **Settings → Devices & Services →
Navimow** and click **Re-authenticate**.

### Entities show as unavailable

Entities are kept available as long as any cached state data exists. If all entities
go unavailable:

1. Check the HA logs for `navimow` related messages
2. Verify your Navimow account is accessible in the official app
3. Try reloading the integration via **Settings → Devices & Services → Navimow → Reload**

### Enable debug logging

```yaml
# configuration.yaml
logger:
  logs:
    custom_components.navimow_ha: debug
```

---

## Known Limitations

- **Position coordinates are local, not GPS**: The X/Y values are in metres relative
  to the charging station. They cannot be used for accurate world-map positioning.
- **No offline / LAN operation**: All communication goes through the Navimow cloud.
- **Single account instance**: Only one Navimow account can be linked at a time.

---

## Contributing

Pull requests and issue reports are welcome!  
Please open an issue first if you plan a larger change.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Acknowledgements

- [segwaynavimow/NavimowHA](https://github.com/segwaynavimow/NavimowHA) — the official
  integration this fork is based on
- The [navimow-sdk](https://pypi.org/project/navimow-sdk/) Python package
- The Home Assistant community
