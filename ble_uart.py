#!/usr/bin/env python

# Implements the nordic uart service - supposedly this works with SoftRF too, as I could get a closed source terminal emulation going over ble, but not this code yet - and I don't know why
# Nordic documents their protocol here: https://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.sdk5.v14.0.0%2Fble_sdk_app_nus_eval.html

import asyncio
import sys

from bleak import BleakScanner, BleakClient
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice

ADDRESS = sys.argv[1]

UART_SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
UART_RX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
UART_TX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

# All BLE devices have MTU of at least 23. Subtracting 3 bytes overhead, we can
# safely send 20 bytes at a time to any device supporting this service.
UART_SAFE_SIZE = 20


async def uart_terminal():
    """This is a simple "terminal" program that uses the Nordic Semiconductor
    (nRF) UART service. It reads from stdin and sends each line of data to the
    remote device. Any data received from the device is printed to stdout.
    Adapted to use HMSoft uart Service (which seems to mostly just use a different set of UUIDs)
    """
 
    def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

    def handle_rx(_: int, data: bytearray):
        # FIXME this should probably put the data into a buffer from which it can then be printed
        
        # Poor Mans Version: don't print newlines unless they are contained in the data
        # and don't print empty strings
        
        # convert to bytes first, as it is backend specific bridged data
        line = bytes(data).decode('utf8') # is this actually true or is this 7bit? Probably part of the nmea standard
        print(line, end='', flush=True)

    async with BleakClient(ADDRESS, disconnected_callback=handle_disconnect) as client:
        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)

        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        print("Connected, start typing and press ENTER...")

        while True:
            # This waits until you type a line and press ENTER.
            # A real terminal program might put stdin in raw mode so that things
            # like CTRL+C get passed to the remote device.
            data = await reader.read(UART_SAFE_SIZE)

            # data will be empty on EOF (e.g. CTRL+D on *nix)
            if not data:
                break

            # some devices, like devices running MicroPython, expect Windows
            # line endings (uncomment line below if needed)
            # data = data.replace(b"\n", b"\r\n")

            await client.write_gatt_char(UART_RX_CHAR_UUID, data)
            print("sent:", data)


# It is important to use asyncio.run() to get proper cleanup on KeyboardInterrupt.
# This was introduced in Python 3.7. If you need it in Python 3.6, you can copy
# it from https://github.com/python/cpython/blob/3.7/Lib/asyncio/runners.py
try:
    asyncio.run(uart_terminal())
except asyncio.CancelledError:
    # task is cancelled on disconnect, so we ignore this error
    pass
