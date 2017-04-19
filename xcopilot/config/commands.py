from XPLMDataAccess import *
from XPLMUtilities import *
from xcopilot.parser import sanitizeNumberValue, parseToFloat

def parseAltimeterValue(value):
    sanitizedValue = sanitizeNumberValue(value)
    if float(sanitizedValue) < 2500:
        return float(sanitizedValue) * 0.0295301
    else:
        return float(sanitizedValue[:2] + '.' + sanitizedValue[2:])

def parseFlapsValue(value):
    if value.strip().lower() == 'up':
        return 0
    elif value.strip().lower() == 'down':
        return 1
    else:
        return parseToFloat(value)

def parseFlightLevel(value):
    return parseToFloat(value) * 100

def parseFrequency(value):
    sanitizedValue = sanitizeNumberValue(value).replace('.', '')
    sanitizedValue = sanitizedValue if len(sanitizedValue) == 5 else sanitizedValue + '0'
    return int(sanitizedValue)

def headingSelectCommand(headingSelectOn):
    headingStatusID = XPLMFindDataRef('sim/cockpit2/autopilot/heading_mode')
    headingStatus = XPLMGetDatai(headingStatusID)
    if headingSelectOn != headingStatus:
        headingCommandID = XPLMFindCommand('sim/autopilot/heading')
        XPLMCommandOnce(headingCommandID)

DefaultCommands = {
    'SET_ALTIMETER': {
        'regex': '^set altimeter (?P<custom>((\d|zero|one|two|three|four|five|six|seven|eight|nine)\s?){4})$',
        'parseValue': parseAltimeterValue,
        'dataRefs': [
            { 'name': 'sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot', 'type': 'float' },
            { 'name': 'sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot', 'type': 'float' }
        ]
    },
    'SET_ALTITUDE': {
        'regex': '^set altitude (?P<float>((\d|zero|one|two|three|four|five|six|seven|eight|nine)\s?){3,5})$',
        'dataRefs': [{ 'name': 'sim/cockpit2/autopilot/altitude_dial_ft', 'type': 'float' }]
    },
    'FLIGHT_LEVEL': {
        'regex': '^(?:set )?flight level (?P<float>((\d|zero|one|two|three|four|five|six|seven|eight|nine)\s?){3})$',
        'parseValue': parseFlightLevel,
        'dataRefs': [{ 'name': 'sim/cockpit2/autopilot/altitude_dial_ft', 'type': 'float' }]
    },
    'LANDING_GEAR': {
        'regex': '^(?:landing )?gear (?P<boolean>up|down)$',
        'dataRefs': [{ 'name': 'sim/cockpit2/controls/gear_handle_down', 'type': 'boolean' }]
    },
    'FLAPS': {
        'regex': '^flaps (?P<custom>up|down)$',
        'parseValue': parseFlapsValue,
        'dataRefs': [{ 'name': 'sim/cockpit2/controls/flap_ratio', 'type': 'float' }]
    },
    'SET_NAV1': {
        'regex': '^set nav one to (?P<custom>one (zero|one) (zero|one|two|three|four|five|six|seven|eight|nine) (decimal|zero|one|two|three|four|five|six|seven|eight|nine) (zero|one|two|three|four|five|six|seven|eight|nine)\s?(zero|five)?)$',
        'parseValue': parseFrequency,
        'dataRefs': [{ 'name': 'sim/cockpit2/radios/actuators/nav1_left_frequency_hz', 'type': 'int' }]
    },
    'SET_COM1': {
        'regex': '^set com one to (?P<custom>one ((one (eight|nine))|(two (zero|one|two|three|four|five|six|seven|eight|nine))|(three (zero|one|two|three|four|five|six))) (decimal )?(zero|one|two|three|four|five|six|seven|eight|nine)( (zero|two|five|seven))?)$',
        'parseValue': parseFrequency,
        'dataRefs': [{ 'name': 'sim/cockpit2/radios/actuators/com1_left_frequency_hz', 'type': 'int' }]
    },
    'SET_HEADING': {
        'regex': '^set heading (?P<float>((zero|one|two) (zero|one|two|three|four|five|six|seven|eight|nine) (zero|one|two|three|four|five|six|seven|eight|nine))|(three (zero|one|two|three|four|five) (zero|one|two|three|four|five|six|seven|eight|nine))|three six zero)$',
        'dataRefs': [{ 'name': 'sim/cockpit2/autopilot/heading_dial_deg_mag_pilot', 'type': 'float' }]
    },
    'HEADING_SELECT': {
        'regex': '^heading select (?P<boolean>on|off)$',
        'command': headingSelectCommand
    },
    'SET_SPEED': {
        'regex': '^set speed (?P<float>((zero|one|two|three) (\s?(zero|one|two|three|four|five|six|seven|eight|nine)){2}))$',
        'dataRefs': [{ 'name': 'sim/cockpit2/autopilot/airspeed_dial_kts_mach', 'type': 'float' }]
    },
    'SPEED_SELECT': {
        'regex': '^speed select (?P<boolean>on|off)$',
        'dataRefs': [{ 'name': 'sim/cockpit2/autopilot/heading_mode', 'type': 'boolean' }]
    },
    'LANDING_LIGHTS': {
        'regex': '^landing light[s]? (?P<boolean>on|off)$',
        'dataRefs': [{ 'name': 'sim/cockpit2/switches/landing_lights_on', 'type': 'int' }]
    },
    'TAXI_LIGHTS': {
        'regex': '^taxi light[s]? (?P<boolean>on|off)$',
        'dataRefs': [{ 'name': 'sim/cockpit2/switches/taxi_light_on', 'type': 'int' }]
    },
    'NAV_LIGHTS': {
        'regex': '^navigation light[s]? (?P<boolean>on|off)$',
        'dataRefs': [{ 'name': 'sim/cockpit2/switches/navigation_lights_on', 'type': 'int' }]
    },
    'STROBE_LIGHTS': {
        'regex': '^strobe light[s]? (?P<boolean>on|off)$',
        'dataRefs': [{ 'name': 'sim/cockpit2/switches/strobe_lights_on', 'type': 'int' }]
    },
    'BEACON_LIGHTS': {
        'regex': '^beacon light[s]? (?P<boolean>on|off)$',
        'dataRefs': [{ 'name': 'sim/cockpit2/switches/beacon_on', 'type': 'int' }]
    },
}
