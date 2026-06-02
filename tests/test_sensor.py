from __future__ import annotations

from unittest.mock import Mock

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.willow.const import DOMAIN, MANUFACTURER
from custom_components.willow.sensor import SENSOR_DESCRIPTIONS, WillowSensor


DEVICE = {
    "id": 1,
    "sensor_id": "sensor-1",
    "battery_life": 95,
    "version": "2.0.0",
    "user_plant": {"id": 10, "name": "Fern", "location": "Living Room"},
    "latest_reading": {
        "timestamp": "2026-06-02T08:00:00+00:00",
        "temperature": 21.5,
        "humidity": 55,
        "moisture": 42,
        "light": 1234,
    },
}


def make_coordinator(data: dict[str, dict]) -> DataUpdateCoordinator:
    coordinator = Mock(spec=DataUpdateCoordinator)
    coordinator.data = data
    coordinator.last_update_success = True
    return coordinator


def description_for(key: str):
    return next(description for description in SENSOR_DESCRIPTIONS if description.key == key)


def test_battery_sensor_value_and_device_info() -> None:
    sensor = WillowSensor(make_coordinator({"sensor-1": DEVICE}), DEVICE, description_for("battery_life"))

    assert sensor.unique_id == "sensor-1_battery_life"
    assert sensor.native_value == 95
    assert sensor.available is True
    assert sensor.device_info == {
        "identifiers": {(DOMAIN, "sensor-1")},
        "manufacturer": MANUFACTURER,
        "model": "Willow Sensor",
        "name": "Fern",
        "sw_version": "2.0.0",
        "suggested_area": "Living Room",
    }


def test_reading_sensor_value() -> None:
    sensor = WillowSensor(make_coordinator({"sensor-1": DEVICE}), DEVICE, description_for("temperature"))

    assert sensor.native_value == 21.5
    assert sensor.available is True


def test_timestamp_sensor_parses_datetime() -> None:
    sensor = WillowSensor(make_coordinator({"sensor-1": DEVICE}), DEVICE, description_for("timestamp"))

    assert sensor.entity_description.device_class is SensorDeviceClass.TIMESTAMP
    assert sensor.native_value.isoformat() == "2026-06-02T08:00:00+00:00"


def test_sensor_unavailable_without_reading() -> None:
    device = {**DEVICE, "latest_reading": None}
    sensor = WillowSensor(make_coordinator({"sensor-1": device}), device, description_for("temperature"))

    assert sensor.native_value is None
    assert sensor.available is False


def test_sensor_unavailable_when_device_is_missing() -> None:
    sensor = WillowSensor(make_coordinator({}), DEVICE, description_for("battery_life"))

    assert sensor.native_value is None
    assert sensor.available is False
