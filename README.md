# quietcool-python

A python library for communicating with the [QuietCool Wifi Smart Control](https://quietcoolsystems.com/products/wi-fi-smart-control/).

## Usage

QuietCool's wifi controller works with all the fans in your attic. One controller (the Master Hub) connects to your wifi and the others (the Remote Hubs) connect to the Master. All commands you send to any fan go through the Master Hub, which means you have to initialize the `Hub` class with the IP address of the Master Hub.

```python
async def print_all_fans():
    master_hub_ip = "10.0.0.100"
    hub = await Hub.create(master_hub_ip)
    fans = await hub.get_fans()

    for fan in fans:
        print(fan.name)
```

One you get the `Fan`s, all communication should really be done through those objects.

Currently, the library supports:

* Getting all fans in a system
* Turning them on/off
* Getting/setting current fan speed
* Getting/setting available fan speeds

Things this library doesn't support:

* Setting the fan name
* Configuring the wifi settings for the hub
* Updating firmware
* Reading the fan diagnostics

## Tests

There aren't any. I suppose I could set up a fake CoAP server that mimics the Wifi Smart Control, but that would just be the inverse of the code that's in the library. I usually test the code by...running the house fan or the attic fans.

## Disclaimer

As with all house fans, you should really make sure a window is opened before using the library.

Also, I don't have a three-speed fan, so while it should work with them, I actually have no idea if it actually does.