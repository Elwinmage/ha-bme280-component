"""Support for BME280 temperature, humidity and pressure sensor."""
from __future__ import annotations

from functools import partial
import logging

from i2csense.bme280 import BME280 as BME280_i2c  # pylint: disable=import-error
import smbus

from homeassistant.components.sensor import (
    DOMAIN as SENSOR_DOMAIN,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import CONF_MONITORED_CONDITIONS, CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.util import slugify

from .const import (
    CONF_DELTA_TEMP,
    CONF_FILTER_MODE,
    CONF_I2C_ADDRESS,
    CONF_I2C_BUS,
    CONF_OPERATION_MODE,
    CONF_OVERSAMPLING_HUM,
    CONF_OVERSAMPLING_PRES,
    CONF_OVERSAMPLING_TEMP,
    CONF_T_STANDBY,
    DOMAIN,
    MIN_TIME_BETWEEN_UPDATES,
    SENSOR_HUMID,
    SENSOR_PRESS,
    SENSOR_TEMP,
    SENSOR_TYPES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the BME280 sensor."""
    if discovery_info is None:
        return
    sensor_conf = discovery_info[SENSOR_DOMAIN]
    name = sensor_conf[CONF_NAME]
    scan_interval = max(sensor_conf[CONF_SCAN_INTERVAL], MIN_TIME_BETWEEN_UPDATES)
    i2c_address = sensor_conf[CONF_I2C_ADDRESS]
    bus = smbus.SMBus(sensor_conf[CONF_I2C_BUS])
    sensor = await hass.async_add_executor_job(
        partial(
            BME280_i2c,
            bus,
            i2c_address,
            osrs_t=sensor_conf[CONF_OVERSAMPLING_TEMP],
            osrs_p=sensor_conf[CONF_OVERSAMPLING_PRES],
            osrs_h=sensor_conf[CONF_OVERSAMPLING_HUM],
            mode=sensor_conf[CONF_OPERATION_MODE],
            t_sb=sensor_conf[CONF_T_STANDBY],
            filter_mode=sensor_conf[CONF_FILTER_MODE],
            delta_temp=sensor_conf[CONF_DELTA_TEMP],
        )
    )
    if not sensor.sample_ok:
        _LOGGER.error("BME280 sensor not detected at %s", i2c_address)
        return

    async def async_update_data():
        await hass.async_add_executor_job(sensor.update)
        if not sensor.sample_ok:
            raise UpdateFailed(f"Bad update of sensor {name}")
        return sensor

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=scan_interval,
    )
    await coordinator.async_refresh()
    monitored_conditions = sensor_conf[CONF_MONITORED_CONDITIONS]
    entities = [
        BME280Sensor(name, coordinator, description)
        for description in SENSOR_TYPES
        if description.key in monitored_conditions
    ]
    async_add_entities(entities, True)


class BME280Sensor(CoordinatorEntity, SensorEntity):
    """Implementation of the BME280 sensor."""

    def __init__(self, name, coordinator, description: SensorEntityDescription) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_name = f"{name} {description.name}"
        self._unique_id = slugify(f"{DOMAIN}_{self._attr_name}_{self.entity_description.key}")

    @property
    def unique_id(self):
        """Return a unique_id for this entity."""
        return self._unique_id

    @property
    def native_value(self) -> any:
        """Return the state of the sensor."""
        sensor_type = self.entity_description.key
        if sensor_type == SENSOR_TEMP:
            temperature = round(self.coordinator.data.temperature, 1)
            state = temperature
        elif sensor_type == SENSOR_HUMID:
            state = round(self.coordinator.data.humidity, 1)
        elif sensor_type == SENSOR_PRESS:
            state = round(self.coordinator.data.pressure, 1)
        return state

 
    @property
    def should_poll(self) -> bool:
        """Return False if entity should not poll."""
        return False
