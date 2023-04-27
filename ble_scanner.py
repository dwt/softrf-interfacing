#!/usr/bin/env python

import asyncio
from bleak import BleakScanner

# 11.24 seconds is the max BLE advertising interval
SCAN_TIME = 11.0 # seconds

def detection_callback(device, advertisement_data):
    # print(device.address, "RSSI:", device.rssi, advertisement_data)
    print('.', flush=True, end='')

async def run():
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(SCAN_TIME)
    await scanner.stop()
    devices = await scanner.get_discovered_devices()
    
    print()
    print()

    for device in devices:
        print(device)#, vars(device))

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
