from xcopilot.parser import sanitizeNumberValue, parseToFloat

Identifier = {
    'author': '2016',
    'description': '727 Series by FlyJSim',
    'ICAO': 'B727'
}

Commands = {
    'LANDING_LIGHTS': {
        'regex': '^landing light[s]? (?P<boolean>on|off)$',
        'dataRefs': [
            { 'name': 'FJS/727/lights/OutboundLLSwitch_L', 'type': 'float' },
            { 'name': 'FJS/727/lights/OutboundLLSwitch_R', 'type': 'float' },
            { 'name': 'FJS/727/lights/InboundLLSwitch_L', 'type': 'float' },
            { 'name': 'FJS/727/lights/InboundLLSwitch_R', 'type': 'float' }
        ]
    },
    'TAXI_LIGHTS': {
        'regex': '^taxi light[s]? (?P<boolean>on|off)$',
        'dataRefs': [{ 'name': 'FJS/727/lights/TaxiLightSwitch', 'type': 'float' }]
    },
    'NAV_LIGHTS': {
        'regex': '^navigation light[s]? (?P<boolean>on|off)$',
        'dataRefs': [{ 'name': 'FJS/727/lights/NavLightSwitch', 'type': 'float' }]
    },
    'STROBE_LIGHTS': {
        'regex': '^strobe light[s]? (?P<boolean>on|off)$',
        'dataRefs': [{ 'name': 'FJS/727/lights/StrobeLightSwitch', 'type': 'float' }]
    },
    'BEACON_LIGHTS': {
        'regex': '^beacon light[s]? (?P<boolean>on|off)$',
        'dataRefs': [{ 'name': 'FJS/727/lights/BeaconLightSwitch', 'type': 'float' }]
    }
}
