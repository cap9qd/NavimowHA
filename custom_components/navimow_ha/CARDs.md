# Navimow Dashboard Cards

A complete, visually appealing Lovelace dashboard for the Navimow lawn mower.

## Included Cards

| Card | Description |
|-------|-------------|
| **Title + Chips** | Status, Battery, Signal at a glance |
| **SVG Live Map** | Animated mower on dark green lawn background |
| **Battery Gauge** | Needle display + 24h history (Mini Graph) |
| **Controls** | Mowing / Pause / Return / Locate — color active |
| **Settings** | Cutting height, edge mowing, rain mode, anti-theft |
| **Statistics** | Mowing time, area, status, signal |
| **Error Card** | Pulsing visible, only when error active |

## Requirements (HACS Frontend)

Install the following cards via **HACS → Frontend**:

| Card | HACS Name |
|------|-----------|
| Mushroom Cards | \lovelace-mushroom\ |
| Button Card | \lovelace-button-card\ |
| Mini Graph Card | \mini-graph-card\ |
| Card Mod | \lovelace-card-mod\ |

## Installation

1. Install HACS cards and reload HA  
2. Find device ID:  
   **Developer Tools → States → Search for "navimow"**  
   Example: \sensor.navimow_m550_battery\ → ID = \m550\  
3. In \dashboard-cards.yaml\ replace all **\[DEVICE_ID]\** with your ID  
4. Dashboard → ⋮ → Edit Dashboard → ＋ View → RAW Editor  
5. Paste entire content from \dashboard-cards.yaml\ → Save

## Live Map: Adjust RANGE

The live map uses **local coordinates** (meters from charging station, no GPS).  
Adjust the \RANGE\ value (line ~80 in \dashboard-cards.yaml\) to your lawn radius:

\\\javascript
const RANGE = 12;  // ← e.g. 8 for small lawn, 20 for large lawn
\\\

## Live Map Display

- 🟡 **Golden dot** = Charging station (coordinate origin)
- 🟢 **Green circle** = Mower → pulses while mowing
- **White triangle** = Driving direction (based on θ)
- **Cross blade** = rotates animated while mowing
- **Battery bar** top right on the map
- **Status badge** bottom on the map