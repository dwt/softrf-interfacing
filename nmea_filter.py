#!/usr/bin/env python

import fileinput
import sys
import logging
import re

import pynmea2

"""
This utility filters the NMEA messages and removed unwanted ones.

Call with the input file and a list of allowed messages, e.g.:
$ ./nmea_filter.py - GGA GSA GSV RMC VTG PFLAU

Empty allowed messages means all messages are allowed.
$ ./nmea_filter.py -
"""

def allow_line(line, allowed_messages=None):
    if not allowed_messages:
        return True
    
    if not line.startswith('$'):
        return False
    
    match = re.match(r'^\$(?P<identifier>\w*),', line)
    if not match:
        return False
    
    identifier = match.group('identifier')
    return identifier in allowed_messages
    # Not sure why the pynmea2 library doesn't recognize the non standard messages
    # anymore, but it doesn't. :-(
    # try:
    #     message = pynmea2.parse(line)
    #     return message.identifier() in allowed_messages
    # except pynmea2.nmea.ParseError:
    #     logging.exception("Couldn't parse line: %r", line)
    #     return False

if __name__ == '__main__':
    logging.basicConfig()
    input_file, *allowed_messages = sys.argv[1:]
    for line in fileinput.input(input_file):
        # if '$' in line[1:]:
        #     for line in re.split(r'(?=\$)', line):
        #         if allow_line(line, allowed_messages):
        #             print(line, end='', flush=True)
        
        # elif 
        if allow_line(line, allowed_messages):
            print(line, end='', flush=True)
