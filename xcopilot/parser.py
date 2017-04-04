def sanitizeNumberValue(value):
    return value.strip().lower().replace('zero', '0').replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4').replace('five', '5').replace('six', '6').replace('seven', '7').replace('eight', '8').replace('nine', '9').replace(' ', '')

def parseToFloat(value):
    return float(sanitizeNumberValue(value))

def parseToBoolean(value):
    return 1 if value.lower() in ['on', 'down'] else 0
