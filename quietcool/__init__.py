import logging
import asyncio
import json

from aiocoap import *

class Hub:
    @classmethod
    async def create(cls, ip):
        self = Hub()
        self.ip = ip
        self.protocol = await Context.create_client_context()
        return self

    def _uri(self, path):
        return f"coap://{self.ip}{path}"

    async def _send(self, request):
        response = await self.protocol.request(request).response
        payload = json.loads(response.payload)
        return payload

    async def _get(self, path):
        request = Message(code=GET, uri=self._uri(path))
        return await self._send(request)

    async def _put(self, path, payload):
        stringified_payload = json.dumps(payload).encode()
        request = Message(code=PUT, uri=self._uri(path), payload=stringified_payload)
        return await self._send(request)

    async def get_fan_info(self, id):
        return await self._get(f"/device/{id}")

    async def get_fan_status(self, id):
        return await self._get(f"/control/{id}")

    async def get_fan_details(self, id):
        return (await self.get_fan_info(id), await self.get_fan_status(id))

    async def set_time_remaining(self, id, remaining):
        return await self._put(f"/control/{id}", { "remaining" : remaining })

    async def set_current_speed(self, id, speed):
        return await self._put(f"/control/{id}", { "speed" : speed })

    async def set_sequence(self, id, sequence):
        return await self._put(f"/control/{id}", { "sequence" : sequence })

    async def get_fans(self):
        fan_uids = [f['uid'] for f in await self._get("/uids")]
        fans = [await Fan.create(self, uid) for uid in fan_uids]
        return fans

class Fan:
    @classmethod
    async def create(cls, hub, id):
        self = Fan()
        self.hub = hub
        self.id = id
        await self.refresh()
        return self

    async def refresh(self):
        (info, status) = await self.hub.get_fan_details(self.id)
        self.info = info
        self.status = status

    def __str__(self):
        return f"{self.id} - {self.info['name']}"

    @property
    def name(self):
        return self.info['name']

    @property
    def current_power(self):
        return self.info['status'] == "1"

    @property
    def current_speed(self):
        speeds = {
            '3': 'High',
            '2': 'Medium',
            '1': 'Low'
        }
        return speeds[self.status['speed']]

    @property
    def configured_speeds(self):
        sequence = self.status["sequence"]
        speeds = {
            '0': ['Low', 'Medium', 'High'],
            '1': ['Low', 'High'],
            '4': ['High'],
        }
        return speeds[sequence]

    async def set_configured_speeds(self, number_of_speeds):
        sequences = {
            '3': '0',
            '2': '1',
            '1': '4'
        }
        sequence = sequences[str(number_of_speeds)]
        await self.hub.set_sequence(self.id, sequence)
        await self.refresh()

    async def set_current_speed(self, speed):
        speeds = {
            'High': '3',
            'Medium': '2',
            'Low': '1'
        }
        translated_speed = speeds[speed]
        await self.hub.set_current_speed(self.id, translated_speed)
        await self.refresh()

    async def turn_on(self):
        await self.hub.set_time_remaining(self.id, 65535)
        await self.refresh()

    async def turn_off(self):
        await self.hub.set_time_remaining(self.id, 0)
        await self.refresh()
