from xcopilot.config import DefaultCommands

FlapsToValue = {
    'up': 0,
    'two': 0.142857,
    'five': 0.285714,
    'fifteen': 0.428571,
    'twenty': 0.571429,
    'twenty five': 0.714286,
    'thirty': 0.857143,
    'fourty': 1,
    'down': 1,
}

def parseFlapsValue(value):
    return FlapsToValue[value.strip().lower()]

Identifier = {
    'author': '2016',
    'description': '727 Series by FlyJSim',
    'ICAO': 'B727'
}

Commands = {
    'FLAPS': {
        'regex': '^flaps (?P<custom>up|two|five|fifteen|twenty|twenty five|thirty|fourty|down)$',
        'parseValue': parseFlapsValue,
        'dataRefs': [{ 'name': 'sim/cockpit2/controls/flap_ratio', 'type': 'float' }]
    },
    'LANDING_LIGHTS': {
        'regex': DefaultCommands['LANDING_LIGHTS']['regex'],
        'dataRefs': [
            { 'name': 'FJS/727/lights/OutboundLLSwitch_L', 'type': 'float' },
            { 'name': 'FJS/727/lights/OutboundLLSwitch_R', 'type': 'float' },
            { 'name': 'FJS/727/lights/InboundLLSwitch_L', 'type': 'float' },
            { 'name': 'FJS/727/lights/InboundLLSwitch_R', 'type': 'float' }
        ]
    },
    'TAXI_LIGHTS': {
        'regex': DefaultCommands['TAXI_LIGHTS']['regex'],
        'dataRefs': [{ 'name': 'FJS/727/lights/TaxiLightSwitch', 'type': 'float' }]
    },
    'NAV_LIGHTS': {
        'regex': DefaultCommands['NAV_LIGHTS']['regex'],
        'dataRefs': [{ 'name': 'FJS/727/lights/NavLightSwitch', 'type': 'float' }]
    },
    'STROBE_LIGHTS': {
        'regex': DefaultCommands['STROBE_LIGHTS']['regex'],
        'dataRefs': [{ 'name': 'FJS/727/lights/StrobeLightSwitch', 'type': 'float' }]
    },
    'BEACON_LIGHTS': {
        'regex': DefaultCommands['BEACON_LIGHTS']['regex'],
        'dataRefs': [{ 'name': 'FJS/727/lights/BeaconLightSwitch', 'type': 'float' }]
    }
}
