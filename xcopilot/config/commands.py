from xcopilot.parser import sanitizeNumberValue

def parseAltimeterValue(value):
    sanitizedValue = sanitizeNumberValue(value)
    return float(sanitizedValue[:2] + '.' + sanitizedValue[2:])

CommandConfig = {
    'SET_ALTIMETER': {
        'regex': '^set altimeter (?P<custom>((\d|zero|one|two|three|four|five|six|seven|eight|nine)\s?){4})$',
        'parseValue': parseAltimeterValue,
        'type': 'float'
    },
    'SET_ALTITUDE': {
        'regex': '^set altitude (?P<float>((\d|zero|one|two|three|four|five|six|seven|eight|nine)\s?){3,5})$'
    },
    'LANDING_LIGHTS': {
        'regex': '^landing light[s]? (?P<boolean>on|off)$'
    }
}
