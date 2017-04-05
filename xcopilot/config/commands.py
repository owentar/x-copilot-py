from xcopilot.parser import sanitizeNumberValue, parseToFloat

def parseAltimeterValue(value):
    sanitizedValue = sanitizeNumberValue(value)
    return float(sanitizedValue[:2] + '.' + sanitizedValue[2:])

def parseFlapsValue(value):
    if value.strip().lower() == 'up':
        return 0
    elif value.strip().lower() == 'down':
        return 1
    else:
        return parseToFloat(value)

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
    'LANDING_GEAR': {
        'regex': '^(?:landing )?gear (?P<boolean>up|down)$',
        'dataRefs': [{ 'name': 'sim/cockpit2/controls/gear_handle_down', 'type': 'boolean' }]
    },
    'FLAPS': {
        'regex': '^flaps (?P<float>up|down)$',
        'parseValue': parseFlapsValue,
        'dataRefs': [{ 'name': 'sim/cockpit2/controls/flap_ratio', 'type': 'float' }]
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
