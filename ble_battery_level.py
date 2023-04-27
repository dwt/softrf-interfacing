#!/usr/bin/env python

import asyncio
import sys

from bleak import BleakScanner, BleakClient
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice

ADDRESS = sys.argv[1]

BATTERY_SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"
BATTERY_LEVEL_CHARACTERISTIC_UUID = "00002a19-0000-1000-8000-00805f9b34fb"
BATTERY_LEVEL_DESCRIPTOR_UUID = "00002902-0000-1000-8000-00805f9b34fb"

async def main(address):
    async with BleakClient(address) as client:
        battery_level = await client.read_gatt_char(BATTERY_LEVEL_CHARACTERISTIC_UUID)
        print("Battery Level: {0} %".format(ord(battery_level)))

asyncio.run(main(ADDRESS))