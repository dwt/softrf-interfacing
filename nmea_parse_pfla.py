#!/usr/bin/env python

import fileinput
import sys
import logging

import pynmea2

def parse_PFLA(line):
    """Fields:
    visible and alarm?
    snprintf_P(NMEABuffer, sizeof(NMEABuffer), PSTR("$PFLAA,%d,%d,%d,%d,%d,%06X!%s,%d,,%d,%s,%d*"),
      alarm_level,
      (int) (distance * cos(radians(bearing))), (int) (distance * sin(radians(bearing))),
      alt_diff, addr_type, Container[i].addr, NMEA_Callsign,
      (int) Container[i].course, (int) (Container[i].speed * _GPS_MPS_PER_KNOT),
      ltrim(str_climb_rate), Container[i].aircraft_type);

    visible aircraft:
    snprintf_P(NMEABuffer, sizeof(NMEABuffer),
        PSTR("$PFLAU,%d,%d,%d,%d,%d,%d,%d,%d,%u,%06X" PFLAU_EXT1_FMT "*"),
        total_objects,
        settings->txpower == RF_TX_POWER_OFF ? TX_STATUS_OFF : TX_STATUS_ON,
        GNSS_STATUS_3D_MOVING,
        POWER_STATUS_GOOD, HP_alarm_level, rel_bearing,
        ALARM_TYPE_AIRCRAFT, HP_alt_diff, (int) HP_distance, HP_addr
        PFLAU_EXT1_ARGS );
    
    no visible aircraft:
    snprintf_P(NMEABuffer, sizeof(NMEABuffer),
        PSTR("$PFLAU,0,%d,%d,%d,%d,,0,,," PFLAU_EXT1_FMT "*"),
        has_Fix && (settings->txpower != RF_TX_POWER_OFF) ?
          TX_STATUS_ON : TX_STATUS_OFF,
        has_Fix ? GNSS_STATUS_3D_MOVING : GNSS_STATUS_NONE,
        POWER_STATUS_GOOD, HP_alarm_level
        PFLAU_EXT1_ARGS );

    """
    message = pynmea2.parse(line)
    update_type, total_objects, tx_status, gnss_status_3d_moving, power_status, alarm_level, relative_bearing, aircraft_type, altitude_difference, distance, address, *extra_args = message.data
    # print(locals())
    print(f'{update_type=} {total_objects=} {tx_status=} {gnss_status_3d_moving=} {power_status=} {alarm_level=} {relative_bearing=} {aircraft_type=} {altitude_difference=} {distance=} {address=} {extra_args=}')


if __name__ == '__main__':
    logging.basicConfig()
    for line in fileinput.input():
        # FIXME somehow the line is not always a full line, but sometimes desynchronized half lines. Not sure what is going on here
        if '$' in line[1:]:
            for line in re.split(r'(?=\$)', line):
                parse_PFLA(line)
        
        parse_PFLA(line)
