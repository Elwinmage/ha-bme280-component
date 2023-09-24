bme280 connected via i2c 1 to a raspberry pi, component for home assistant 

you need to load some kernel modules to enable i2c, there's an home assistant component to do it easily:
https://community.home-assistant.io/t/add-on-hassos-i2c-configurator/264167

This is the original home assistant component (removed from the current distro) with a few mods to the code to make it compatible with the current version
you can place the bme280 folder inside your config/custom_components folder and configure it inside your configuration.yaml, this is mine:

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

I'm not an home assistant expert, I'm sharing this because it took me a good afternoon understanding why it has to be so hard to use a weather chip with a board perfectly able to handle it and have it monitored

If you want to help and make this repo easily usable from home assistant feel free to drop me a message for co-op access or fork this.
