# Navimow Live Map

## Coordinate System

The position (X/Y) from Navimow is **local** in meters from the charging station — **no GPS**.

| Value | Meaning |
|------|-----------|
| X | East (+) / West (-) in meters |
| Y | North (+) / South (-) in meters |
| θ (Theta) | Orientation in radians |

Origin (0, 0) = Charging station.

## SVG Live Map (in dashboard-cards.yaml)

The included SVG map shows:
- Charging station as golden ⚡-point in the center
- Mower as colored circle with direction arrow
- Pulsing animation while mowing
- Rotating blade while mowing
- Battery bar and position display directly on the map

### Adjust RANGE

In \dashboard-cards.yaml\ (approx. line 80):

\```javascript
const RANGE = 12;  // Radius in meters
\```

Choose the value according to your lawn:
- Small lawn (< 100 m²): \RANGE = 6\
- Medium lawn (~300 m²): \RANGE = 12\
- Large lawn (> 500 m²): \RANGE = 20\

## Real GPS Map

If the mower provides real GPS coordinates (future SDK version),
the standard HA map type will work automatically:

\```yaml
type: map
entities:
  - device_tracker.navimow_[DEVICE_ID]_location
default_zoom: 19
\```

Currently \device_tracker\ reports the local X/Y values as Lat/Lon — 
this places the mower at an arbitrary world map location,
but is functional for the native HA map (movement is visible).