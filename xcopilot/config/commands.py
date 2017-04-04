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

CommandConfig = {
    'SET_ALTIMETER': {
        'regex': '^set altimeter (?P<custom>((\d|zero|one|two|three|four|five|six|seven|eight|nine)\s?){4})$',
        'parseValue': parseAltimeterValue
    },
    'SET_ALTITUDE': {
        'regex': '^set altitude (?P<float>((\d|zero|one|two|three|four|five|six|seven|eight|nine)\s?){3,5})$'
    },
    'LANDING_GEAR': {
        'regex': '^(?:landing )?gear (?P<boolean>up|down)$'
    },
    'FLAPS': {
        'regex': '^flaps (?P<float>up|down)$',
        'parseValue': parseFlapsValue
    },
    'LANDING_LIGHTS': {
        'regex': '^landing light[s]? (?P<boolean>on|off)$'
    },
    'TAXI_LIGHTS': {
        'regex': '^taxi light[s]? (?P<boolean>on|off)$'
    },
    'NAV_LIGHTS': {
        'regex': '^navigation light[s]? (?P<boolean>on|off)$'
    },
    'STROBE_LIGHTS': {
        'regex': '^strobe light[s]? (?P<boolean>on|off)$'
    },
    'BEACON_LIGHTS': {
        'regex': '^beacon light[s]? (?P<boolean>on|off)$'
    },
}
