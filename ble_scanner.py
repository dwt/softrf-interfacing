#!/usr/bin/env python

import asyncio
from bleak import BleakScanner

def detection_callback(device, advertisement_data):
    # print(device.address, "RSSI:", device.rssi, advertisement_data)
    print('.', flush=True, end='')

async def run():
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(5.0)
    await scanner.stop()
    devices = await scanner.get_discovered_devices()
    
    print()
    print()

    for device in devices:
        print(device)#, vars(device))

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
