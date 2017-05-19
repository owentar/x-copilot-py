TO_NUMBER = {
    0: 'ZERO',
    1: 'ONE',
    2: 'TWO',
    3: 'THREE',
    4: 'FOUR',
    5: 'FIVE',
    6: 'SIX',
    7: 'SEVEN',
    8: 'EIGHT',
    9: 'NINE',
    10: 'TEN',
    11: 'ELEVEN',
    15: 'FIFTEEN',
    20: 'TWENTY',
    25: 'TWENTY FIVE',
    30: 'THIRTY',
    40: 'FOURTY'
}

FLAPS = ['UP', 'DOWN', 'FULL', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30, 40]

TRAIN_COMMANDS_METADATA = {
    'SET ALTIMETER': {
        'range': range(0, 10),
        'transcription': lambda i: 'SET ALTIMETER TWO NINE NINE {}'.format(TO_NUMBER[i])
    },
    'SET ALTITUDE': {
        'range': range(0, 3),
        'transcription': lambda i: 'SET ALTITUDE THREE FIVE {}'.format(('ZERO ' * (i + 1)).strip())
    },
    'FLIGHT LEVEL': {
        'range': range(0, 3),
        'transcription': lambda i: '{} FLIGHT LEVEL {} {} ZERO'.format('SET' if i % 2 == 0 else '', TO_NUMBER[i + 2], TO_NUMBER[i + 1]).strip()
    },
    'LANDING GEAR': {
        'range': range(0, 4),
        'transcription': lambda i: '{} GEAR {}'.format('LANDING' if i > 1 else '', 'UP' if i % 2 == 0 else 'DOWN').strip()
    },
    'FLAPS': {
        'range': FLAPS,
        'transcription': lambda i: 'FLAPS {}'.format(TO_NUMBER[i] if i in TO_NUMBER else i).strip()
    },
    'HEADING SELECT': {
        'range': range(0, 2),
        'transcription': lambda i: 'HEADING SELECT {}'.format('ON' if i % 2 == 0 else 'OFF')
    }
}
