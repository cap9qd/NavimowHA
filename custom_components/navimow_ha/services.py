"""Services for Navimow integration."""

import logging
from datetime import datetime
from typing import Any

import voluptuous as vol

from homeassistant.components import persistent_notification
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_SET_BLADE_HEIGHT = "set_blade_height"
SERVICE_TEST_MQTT_DATA = "test_mqtt_data"

SERVICE_SCHEMA_SET_BLADE_HEIGHT = vol.Schema(
    {
        vol.Required("device_id"): cv.string,
        vol.Required("height"): vol.Coerce(int),
    }
)

SERVICE_SCHEMA_TEST_MQTT_DATA = vol.Schema(
    {
        vol.Optional("duration"): vol.All(int, vol.Range(min=10, max=300)),
        vol.Optional("send_notification"): vol.Boolean,
        vol.Optional("persistent_notification"): vol.Boolean,
    }
)


def async_setup_services(hass: HomeAssistant, _api: Any) -> None:
    async def _handle_set_blade_height(call: ServiceCall) -> None:
        device_id = call.data["device_id"]
        height = call.data["height"]
        _LOGGER.warning(
            "Blade height change requested via service but REST API does not support it "
            "(device %s, height %s). Use the number entity instead.",
            device_id,
            height,
        )
        raise HomeAssistantError(
            "Setting blade height via the REST API is not supported. "
            "Use the 'Cutting Height' number entity instead."
        )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_BLADE_HEIGHT,
        _handle_set_blade_height,
        schema=SERVICE_SCHEMA_SET_BLADE_HEIGHT,
    )

    async def _handle_test_mqtt_data(call: ServiceCall) -> None:
        """Test MQTT data quality and generate a diagnostic summary."""
        duration = call.data.get("duration", 60)
        send_notification = call.data.get("send_notification", False)
        persistent_notification = call.data.get("persistent_notification", True)

        # Get integration data
        domain_data = hass.data.get(DOMAIN, {})
        if not domain_data:
            raise HomeAssistantError("Navimow integration not loaded")

        # Get first config entry's data
        entry_id = list(domain_data.keys())[0]
        entry_data = domain_data[entry_id]

        coordinators = entry_data.get("coordinators", {})
        if not coordinators:
            raise HomeAssistantError("No Navimow coordinators found")

        # Test each device
        results = []
        for device_id, coordinator in coordinators.items():
            result = await _test_device_mqtt_data(coordinator, device_id, duration)
            results.append(result)

        # Generate summary
        summary = _generate_mqtt_test_summary(results)

        # Store in hass.data for diagnostics
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN]["mqtt_test_results"] = {
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "summary": summary,
        }

        _LOGGER.info("MQTT test completed:\n%s", summary)

        # Send notifications if requested
        if send_notification or persistent_notification:
            await _send_mqtt_test_notification(
                hass, summary, persistent_notification, send_notification
            )

        return {"summary": summary, "results": results}

    async def _test_device_mqtt_data(
        coordinator, device_id: str, duration: int
    ) -> dict:
        """Test MQTT data for a single device."""
        import asyncio
        import time

        start_time = time.time()
        fields_received = set()
        position_updates = 0
        metrics_updates = 0

        # Record initial state
        initial_data_source = coordinator._last_data_source
        initial_mqtt_ts = coordinator._last_mqtt_update
        initial_state = coordinator.get_device_state()

        # Wait for messages (check periodically)
        check_interval = 5  # Check every 5 seconds
        elapsed = 0
        while elapsed < duration:
            await asyncio.sleep(check_interval)
            elapsed += check_interval

            # Check current state
            state = coordinator.get_device_state()
            if state:
                if state.state:
                    fields_received.add("state")
                if state.battery is not None:
                    fields_received.add("battery")
                if state.position:
                    fields_received.add("position")
                    position_updates += 1
                if state.metrics:
                    fields_received.add("metrics")
                    metrics_updates += 1
                if state.signal_strength is not None:
                    fields_received.add("signal_strength")

        # Final check
        state = coordinator.get_device_state()
        attrs = coordinator.get_device_attributes()

        # Determine data source quality
        data_source = coordinator._last_data_source
        mqtt_working = data_source == "mqtt_push" or (
            initial_mqtt_ts is not None and initial_mqtt_ts > 0
        )

        # Check if state changed during test (indicates active mowing)
        state_changed = False
        if initial_state and state:
            if initial_state.state != state.state or initial_state.battery != state.battery:
                state_changed = True

        return {
            "device_id": device_id,
            "duration_seconds": round(time.time() - start_time, 1),
            "data_source": data_source,
            "mqtt_working": mqtt_working,
            "fields_received": sorted(list(fields_received)),
            "position_updates": position_updates,
            "metrics_updates": metrics_updates,
            "state_available": state is not None,
            "attributes_available": attrs is not None,
            "current_state": state.state if state else None,
            "current_battery": state.battery if state else None,
            "state_changed_during_test": state_changed,
        }

    def _generate_mqtt_test_summary(results: list[dict]) -> str:
        """Generate a human-readable summary of MQTT test results."""
        lines = ["=" * 60, "NAVIMOW MQTT DATA TEST SUMMARY", "=" * 60, ""]

        for result in results:
            lines.append(f"Device: {result['device_id']}")
            lines.append(f"  Data Source: {result['data_source']}")
            lines.append(f"  MQTT Working: {'Yes' if result['mqtt_working'] else 'No'}")
            lines.append(f"  State Available: {'Yes' if result['state_available'] else 'No'}")
            lines.append(f"  Attributes Available: {'Yes' if result['attributes_available'] else 'No'}")
            lines.append(f"  Current State: {result['current_state']}")
            lines.append(f"  Current Battery: {result['current_battery']}%")
            lines.append("")
            lines.append("  Fields Received:")

            field_status = {
                "state": "✓" if "state" in result["fields_received"] else "✗",
                "battery": "✓" if "battery" in result["fields_received"] else "✗",
                "position": "✓" if "position" in result["fields_received"] else "✗",
                "metrics": "✓" if "metrics" in result["fields_received"] else "✗",
                "signal_strength": "✓"
                if "signal_strength" in result["fields_received"]
                else "✗",
                "attributes": "✓" if "attributes" in result["fields_received"] else "✗",
            }

            for field, status in field_status.items():
                lines.append(f"    {status} {field}")

            lines.append("")
            lines.append(f"  Position Updates: {result['position_updates']}")
            lines.append(f"  Metrics Updates: {result['metrics_updates']}")
            lines.append("")

            # Overall assessment
            if not result["mqtt_working"]:
                lines.append(
                    "  ⚠️  WARNING: MQTT is not working. Using HTTP polling only."
                )
                lines.append(
                    "      This is expected for some models (including X450)."
                )
            elif result["position_updates"] == 0:
                lines.append(
                    "  ⚠️  NOTE: No position data received via MQTT."
                )
                lines.append(
                    "      Position data may not be available for your mower model."
                )
            else:
                lines.append("  ✓ MQTT is working and delivering full data!")

            lines.append("")
            lines.append("-" * 60)

        return "\n".join(lines)

    async def _send_mqtt_test_notification(
        hass: HomeAssistant, summary: str, persistent: bool, send: bool
    ):
        """Send MQTT test results as a notification."""
        title = "Navimow MQTT Test Results"

        if persistent or send:
            persistent_notification.async_create(
                hass,
                title=title,
                message=summary,
                notification_id="navimow_mqtt_test_results",
            )

    hass.services.async_register(
        DOMAIN,
        SERVICE_TEST_MQTT_DATA,
        _handle_test_mqtt_data,
        schema=SERVICE_SCHEMA_TEST_MQTT_DATA,
    )
