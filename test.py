import asyncio

from quietcool import *

run = asyncio.get_event_loop().run_until_complete

hub = run(Hub.create("10.0.0.151"))
fans = run(hub.get_fans())

for fan in fans:
    print(fan.name)
    print(fan.configured_speeds)
    print(fan.current_speed)
    print("===============")
