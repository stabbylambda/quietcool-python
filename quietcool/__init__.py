import logging
import asyncio

from aiocoap import *

CONTROLLER_IP='10.0.0.151'

async def quietcool():
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri=f"coap://{CONTROLLER_IP}/uids")

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))
