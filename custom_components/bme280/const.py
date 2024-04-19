"""Constants for the BME280 component."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.components.sensor import SensorDeviceClass, SensorEntityDescription
from homeassistant.const import PERCENTAGE, UnitOfTemperature

# Common
DOMAIN = "bme280"
CONF_OVERSAMPLING_TEMP = "oversampling_temperature"
CONF_OVERSAMPLING_PRES = "oversampling_pressure"
CONF_OVERSAMPLING_HUM = "oversampling_humidity"
CONF_T_STANDBY = "time_standby"
CONF_FILTER_MODE = "filter_mode"
DEFAULT_NAME = "BME280 Sensor"
DEFAULT_OVERSAMPLING_TEMP = 1
DEFAULT_OVERSAMPLING_PRES = 1
DEFAULT_OVERSAMPLING_HUM = 1
DEFAULT_T_STANDBY = 5
DEFAULT_FILTER_MODE = 0
DEFAULT_SCAN_INTERVAL = 300
SENSOR_TEMP = "temperature"
SENSOR_HUMID = "humidity"
SENSOR_PRESS = "pressure"
SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=SENSOR_TEMP,
        name="Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SensorEntityDescription(
        key=SENSOR_HUMID,
        name="Humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
    ),
    SensorEntityDescription(
        key=SENSOR_PRESS,
        name="Pressure",
        native_unit_of_measurement="mbar",
        device_class=SensorDeviceClass.PRESSURE,
    ),
)
SENSOR_KEYS: list[str] = [desc.key for desc in SENSOR_TYPES]
DEFAULT_MONITORED = [SENSOR_TEMP, SENSOR_HUMID, SENSOR_PRESS]
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=3)
# I2C
CONF_I2C_ADDRESS = "i2c_address"
CONF_I2C_BUS = "i2c_bus"
CONF_DELTA_TEMP = "delta_temperature"
CONF_OPERATION_MODE = "operation_mode"
DEFAULT_OPERATION_MODE = 3  # Normal mode (forced mode: 2)
DEFAULT_I2C_ADDRESS = "0x76"
DEFAULT_I2C_BUS = 1
DEFAULT_DELTA_TEMP = 0.0
