# NavimowHA Integration Development Session Summary

**Date:** July 18, 2026  
**Repository:** https://github.com/cap9qd/NavimowHA  
**Branch:** main (merged from `http-only-no-mqtt`)

---

## Issues Resolved

### 1. Fixed `entity_category` Import Error
**Problem:** Home Assistant 2026.7.1 threw error:
```
ValueError: entity_category must be a valid EntityCategory instance, got action
```

**Fix:** Removed `entity_category=EntityCategory.ACTION` from button entity descriptions (buttons don't need entity_category).

**Files:** `custom_components/navimow_ha/button.py`

---

### 2. Translated German to English
**Problem:** Integration had German UI text that needed translation.

**Fix:** Translated all German text to English:
- `README.md` - Quick start guide
- `CARDs.md` - Dashboard card documentation  
- `dashboard-cards.yaml` - Dashboard configuration
- `MAP.md` - Map documentation
- `navimow-card.js` - Lovelace card UI (status labels, button text, settings)

**Files:** Multiple documentation and UI files

---

### 3. Fixed HTTP Fallback Interval
**Problem:** HTTP fallback interval was 3600 seconds (1 hour), causing entities to show "unknown" or stale data for up to an hour when MQTT failed.

**Fix:** Reduced `HTTP_FALLBACK_MIN_INTERVAL` from 3600 to 60 seconds.

**Files:** `custom_components/navimow_ha/const.py`

---

### 4. Added HTTP-Only Mode
**Problem:** Navimow X450 (and some other models) don't send position/metrics data via MQTT. The integration was trying to use unreliable MQTT data, causing values to flicker between current and stale states.

**Fix:** Added `HTTP_ONLY_MODE` configuration in `const.py`:
- When `True`: Skips MQTT connection, always polls HTTP API every 30 seconds
- When `False`: Uses MQTT + HTTP fallback (original behavior)
- Default: `True` (HTTP-only for reliability)

**Files:** `custom_components/navimow_ha/const.py`, `coordinator.py`, `__init__.py`

---

### 5. Created Navimow SDK Tester
**Problem:** No way to independently test if Navimow Cloud MQTT sends data for specific mower models.

**Fix:** Created standalone Python utility (`navimow-sdk-tester`) that:
- Performs OAuth2 authentication via browser redirect
- Connects to Navimow MQTT broker
- Listens for messages and displays them in real-time
- Generates summary of which fields are received
- Saves results to JSON file

**Repository:** https://github.com/cap9qd/navimow-sdk-tester

**Key Finding:** Navimow X450 does NOT send position, metrics, or attributes via MQTT - only basic state and battery.

---

### 6. Added MQTT Diagnostic Test Service
**Problem:** No built-in way to test MQTT data quality from within Home Assistant.

**Fix:** Added `navimow_ha.test_mqtt_data` service:
- Monitors MQTT messages for specified duration (default 60s)
- Reports which fields are received (state, battery, position, metrics, etc.)
- Stores results in `hass.data['navimow_ha']['mqtt_test_results']`
- Sends persistent notification with test summary
- Optional mobile app notification

**Usage:**
```yaml
service: navimow_ha.test_mqtt_data
data:
  duration: 60
  persistent_notification: true
```

**Files:** `custom_components/navimow_ha/services.py`, `services.yaml`

---

### 7. Added Diagnostics Platform
**Problem:** No easy way to view integration status and debug issues.

**Fix:** Created diagnostics platform accessible via:
**Settings → Devices & Services → Navimow → ⋮ → Diagnostics**

Shows:
- Device information
- Coordinator status (data source, last update times)
- Current state and attributes
- MQTT test results (if run)
- SDK connection status

**Files:** `custom_components/navimow_ha/diagnostics.py`

---

### 8. Fixed OAuth2 Client Secret Typo
**Problem:** `navimow-sdk-tester` failed with `CODE_OAUTH_INFO_ILLEGAL` error.

**Fix:** Corrected `CLIENT_SECRET` from `57056e15-72e-42be-bbaa-b0cbfb208a52` to `57056e15-722e-42be-bbaa-b0cbfb208a52` (missing digit `2`).

**Files:** `navimow-sdk-tester/navimow_tester.py`

---

### 9. Fixed Windows Compatibility
**Problem:** `navimow-sdk-tester` failed on Windows with `NotImplementedError` for asyncio signal handlers.

**Fix:** Wrapped signal handler registration in try/except for Windows compatibility.

**Files:** `navimow-sdk-tester/navimow_tester.py`

---

### 10. Fixed OAuth2 Callback Race Condition
**Problem:** `navimow-sdk-tester` received callback but didn't capture the authorization code properly.

**Fix:** 
- Changed from `handle_request()` to `serve_forever()` for server
- Added `callback_received` flag to track completion
- Used class variables instead of instance variables
- Added proper server shutdown sequence

**Files:** `navimow-sdk-tester/navimow_tester.py`

---

### 11. Fixed Notification Import Error
**Problem:** Integration failed to load with:
```
ImportError: cannot import name 'notification' from 'homeassistant.helpers'
```

**Fix:** Changed import from `homeassistant.helpers.notification` (doesn't exist) to `homeassistant.components.persistent_notification`.

**Files:** `custom_components/navimow_ha/services.py`

---

## X450 Model Findings

The Navimow X450 **does NOT send the following via MQTT**:
- ❌ Position coordinates (X/Y/theta)
- ❌ Work metrics (time, area)
- ❌ Signal strength
- ❌ Device attributes (blade height, edge mowing, rain mode, anti-theft)

The X450 **DOES send via MQTT**:
- ✅ State (mowing, docked, charging, paused, error)
- ✅ Battery percentage

**Conclusion:** X450 and similar models should use HTTP-only mode for reliable data. Position and metrics data are not available from the Navimow cloud for these models.

---

## New Features Added

| Feature | Description | Files |
|---------|-------------|-------|
| HTTP-only mode | Bypass unreliable MQTT, poll HTTP API | `const.py`, `coordinator.py`, `__init__.py` |
| MQTT test service | Test data quality, generate diagnostic summary | `services.py`, `services.yaml` |
| Diagnostics platform | View integration status in UI | `diagnostics.py` |
| SDK tester tool | Standalone MQTT testing utility | `navimow-sdk-tester/` |
| English translations | All German UI text translated | Multiple files |

---

## Configuration Options

### HTTP-Only Mode (Recommended for X450)
```python
# custom_components/navimow_ha/const.py
HTTP_ONLY_MODE: Final = True  # Set to False to re-enable MQTT
```

### MQTT Test Service
```yaml
# Developer Tools → Services
service: navimow_ha.test_mqtt_data
data:
  duration: 60                    # 10-300 seconds
  persistent_notification: true   # Show in HA notifications
  send_notification: false        # Send to mobile app
```

---

## Available Entities for X450

### Working ✅
- `lawn_mower.navimow_X450` - Start/Pause/Dock/Resume
- `sensor.navimow_X450_battery` - Battery percentage
- `sensor.navimow_X450_status` - Mower status
- `binary_sensor.navimow_X450_charging` - Charging state
- `binary_sensor.navimow_X450_mowing` - Mowing state
- `binary_sensor.navimow_X450_docked` - Docked state

### Not Working (X450 Limitation) ❌
- `sensor.navimow_X450_position_x/y/theta` - No position data
- `sensor.navimow_X450_work_time/area` - No metrics data
- `sensor.navimow_X450_signal_strength` - No signal data
- `number.navimow_X450_cutting_height` - No attribute data
- `switch.navimow_X450_*` - No attribute data
- `device_tracker.navimow_X450_location` - No position data

---

## Repositories

- **NavimowHA:** https://github.com/cap9qd/NavimowHA
- **Navimow SDK Tester:** https://github.com/cap9qd/navimow-sdk-tester

---

## Testing Recommendations

1. **Run MQTT test after mower starts:**
   - Wait 5 minutes after mowing starts
   - Run `navimow_ha.test_mqtt_data` service
   - Check notification for results

2. **Check diagnostics for current status:**
   - Settings → Devices & Services → Navimow → ⋮ → Diagnostics
   - View data source, last update times, coordinator status

3. **Use HTTP-only mode for X450:**
   - Set `HTTP_ONLY_MODE = True` in `const.py`
   - Provides consistent, reliable data from HTTP API
   - Avoids flickering between stale and current values

---

## Session Participants
- User: cap9qd (Navimow X450 owner)
- Assistant: Claude Code

## Models Used
- Home Assistant 2026.7.1
- Navimow SDK 0.1.2+
- Python 3.12
