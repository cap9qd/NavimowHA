"""Diagnostics for Navimow integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

# Keys to redact for privacy
TO_REDACT = {"token", "access_token", "refresh_token", "pwdInfo", "password", "userName", "username"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    domain_data = hass.data.get(DOMAIN, {})
    entry_data = domain_data.get(entry.entry_id, {})

    diagnostics_data = {
        "integration": DOMAIN,
        "entry_id": entry.entry_id,
        "config_entry": async_redact_data(entry.data, TO_REDACT),
        "options": async_redact_data(entry.options, TO_REDACT),
    }

    # Add device information
    devices = entry_data.get("devices", [])
    diagnostics_data["devices"] = [
        {
            "id": device.id,
            "name": device.name,
            "model": device.model,
            "serial_number": device.serial_number,
            "firmware_version": device.firmware_version,
        }
        for device in devices
    ]

    # Add coordinator status for each device
    coordinators = entry_data.get("coordinators", {})
    diagnostics_data["coordinators"] = {}

    for device_id, coordinator in coordinators.items():
        state = coordinator.get_device_state()
        attrs = coordinator.get_device_attributes()

        diagnostics_data["coordinators"][device_id] = {
            "data_source": coordinator._last_data_source,
            "last_mqtt_update": coordinator._last_mqtt_update,
            "last_http_fetch": coordinator._last_http_fetch,
            "state": {
                "state": state.state if state else None,
                "battery": state.battery if state else None,
                "signal_strength": state.signal_strength if state else None,
                "has_position": bool(state.position) if state else False,
                "has_metrics": bool(state.metrics) if state else False,
                "has_error": bool(state.error) if state else False,
            }
            if state
            else None,
            "attributes": {
                "attribute_count": len(attrs.attributes) if attrs and attrs.attributes else 0,
            }
            if attrs
            else None,
        }

    # Add MQTT test results if available
    mqtt_test_results = domain_data.get("mqtt_test_results")
    if mqtt_test_results:
        diagnostics_data["mqtt_test_results"] = mqtt_test_results

    # Add SDK connection status
    sdk = entry_data.get("sdk")
    if sdk:
        diagnostics_data["sdk"] = {
            "is_connected": sdk.is_connected,
            "broker": sdk.broker,
            "port": sdk.port,
        }

    return diagnostics_data


async def async_get_device_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry, device: Any
) -> dict[str, Any]:
    """Return diagnostics for a specific device."""
    domain_data = hass.data.get(DOMAIN, {})
    entry_data = domain_data.get(entry.entry_id, {})

    coordinators = entry_data.get("coordinators", {})
    coordinator = coordinators.get(device.id)

    if not coordinator:
        return {"error": "Coordinator not found for device"}

    state = coordinator.get_device_state()
    attrs = coordinator.get_device_attributes()

    diagnostics_data = {
        "device": {
            "id": device.id,
            "name": device.name,
            "model": device.model,
            "serial_number": device.serial_number,
            "firmware_version": device.firmware_version,
        },
        "coordinator": {
            "data_source": coordinator._last_data_source,
            "last_mqtt_update": coordinator._last_mqtt_update,
            "last_http_fetch": coordinator._last_http_fetch,
        },
        "state": {
            "state": state.state if state else None,
            "battery": state.battery if state else None,
            "signal_strength": state.signal_strength if state else None,
            "position": state.position if state else None,
            "metrics": state.metrics if state else None,
            "error": state.error if state else None,
        }
        if state
        else None,
        "attributes": attrs.attributes if attrs else None,
    }

    # Add MQTT test results if available
    mqtt_test_results = domain_data.get("mqtt_test_results")
    if mqtt_test_results:
        for result in mqtt_test_results.get("results", []):
            if result.get("device_id") == device.id:
                diagnostics_data["mqtt_test_result"] = result
                break

    return diagnostics_data
