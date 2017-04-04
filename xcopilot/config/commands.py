from xcopilot.parser import sanitizeNumberValue

def parseAltimeterValue(value):
    sanitizedValue = sanitizeNumberValue(value)
    return float(sanitizedValue[:2] + '.' + sanitizedValue[2:])

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
