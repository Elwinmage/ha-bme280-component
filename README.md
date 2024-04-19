bme280 connected via i2c 1 to a raspberry pi, component for home assistant 

Fork from https://github.com/gdiciocco/bme280

This is the original, old, home assistant component (now removed from the current distro) with a few mods to the code to make it compatible with the current version.
You can install it with hacs.

```yaml
bme280:
    - name: "bme"
      i2c_address: "0x77"
      i2c_bus: "1"
      operation_mode: 2
      time_standby: 5
      oversampling_temperature: 4
      oversampling_pressure: 4
      oversampling_humidity: 4
      delta_temperature: -0.5
      monitored_conditions:
         - temperature
         - humidity
         - pressure
      scan_interval: 40
```

