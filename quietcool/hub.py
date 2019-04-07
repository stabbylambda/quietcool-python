import logging
import asyncio
import json

from aiocoap import Context, Message, Code
from .fan import Fan


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
        request = Message(code=Code.GET, uri=self._uri(path))
        return await self._send(request)

    async def _put(self, path, payload):
        stringified_payload = json.dumps(payload).encode()
        request = Message(code=Code.PUT, uri=self._uri(path),
                          payload=stringified_payload)
        return await self._send(request)

    async def get_fan_info(self, id):
        return await self._get(f"/device/{id}")

    async def get_fan_status(self, id):
        return await self._get(f"/control/{id}")

    async def get_fan_details(self, id):
        return (await self.get_fan_info(id), await self.get_fan_status(id))

    async def set_time_remaining(self, id, remaining):
        return await self._put(f"/control/{id}", {"remaining": remaining})

    async def set_current_speed(self, id, speed):
        return await self._put(f"/control/{id}", {"speed": speed})

    async def set_sequence(self, id, sequence):
        return await self._put(f"/control/{id}", {"sequence": sequence})

    async def get_fans(self):
        fan_uids = [f['uid'] for f in await self._get("/uids")]
        fans = [await Fan.create(self, uid) for uid in fan_uids]
        return fans
