#!/usr/bin/env python

import asyncio
import logging
import sys

import serial_asyncio

PATH_TO_SERIAL_PORT = sys.argv[1]
UART_SAFE_SIZE = 20

logging.basicConfig()

class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        transport.serial.rts = False  # You can manipulate Serial object via transport
        asyncio.create_task(self.connect_stdin())

    def data_received(self, data):
        # pass
        print(data.decode('utf8'), flush=True, end='')
        # REFACT do I need to do that on exit? In some kind of callback?
        # if b'\n' in data:
        #     self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        pass
        # print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        pass
        # print(self.transport.get_write_buffer_size())
    
    async def connect_stdin(self):
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

            self.transport.write(data)  # Write serial data via transport
            print("sent:", data)

loop = asyncio.get_event_loop()
connection = serial_asyncio.create_serial_connection(loop, Output, PATH_TO_SERIAL_PORT, baudrate=115200)
loop.run_until_complete(connection)
loop.run_forever()
loop.close()
