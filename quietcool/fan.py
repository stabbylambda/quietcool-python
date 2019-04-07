import logging
import asyncio
import json

CONFIG_MAP = {
    3: '0',
    2: '1',
    1: '4'
}


def reverse(a):
    return {v: k for k, v in a.items()}


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
        return int(self.status['speed'])

    @property
    def configured_speeds(self):
        sequence = self.status["sequence"]
        speeds = reverse(CONFIG_MAP)
        return speeds[sequence]

    async def set_configured_speeds(self, number_of_speeds):
        sequences = CONFIG_MAP
        sequence = sequences[number_of_speeds]
        await self.hub.set_sequence(self.id, sequence)
        await self.refresh()

    async def set_current_speed(self, speed):
        await self.hub.set_current_speed(self.id, str(speed))
        await self.refresh()

    async def turn_on(self):
        await self.hub.set_time_remaining(self.id, 65535)
        await self.refresh()

    async def turn_off(self):
        await self.hub.set_time_remaining(self.id, 0)
        await self.refresh()
