FlapsToValue = {
    'up': 0,
    'ten': 0.333333,
    'twenty': 0.666667,
    'thirty': 1,
    'down': 1,
}

def parseFlapsValue(value):
    return FlapsToValue[value.strip().lower()]

Identifier = {
    'author': 'www.dmax3d.com',
    'description': 'Cessna 172 SP SkyHawk - 180HP',
    'ICAO': 'C172'
}

Commands = {
    'FLAPS': {
        'regex': '^flaps (?P<float>up|down|ten|twenty|thirty)$',
        'parseValue': parseFlapsValue,
        'dataRefs': [{ 'name': 'sim/cockpit2/controls/flap_ratio', 'type': 'float' }]
    }
}
