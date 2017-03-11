import re

class Command:
    def __init__(self, name, regex):
        self.name = name
        self.regex = re.compile(regex, re.IGNORECASE)
        self.dataRefs = {}

    def addDataRef(self, id):
        self.dataRefs[id] = None

    def recognizeCommand(self, strCommand):
        return self.regex.match(strCommand) is not None

    def parseCommand(self, strCommand):
        match = self.regex.match(strCommand)

        if match:
            value = self._sanitizeValue(match.group(1))
            value = float(value[:2] + '.' + value[2:])
            self.dataRefs['sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot'] = value
            self.dataRefs['sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot'] = value

    def _sanitizeValue(self, value):
        return value.strip().lower().replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4').replace('five', '5').replace('six', '6').replace('seven', '7').replace('eight', '8').replace('nine', '9').replace(' ', '')

def parseCommand(strCommand):
    command = Command('SET_ALTIMETER', '^set altimeter (((\d|one|two|three|four|five|six|seven|eight|nine)\s?){4})$')
    command.addDataRef('sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot')
    command.addDataRef('sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot')
    if command.recognizeCommand(strCommand):
        command.parseCommand(strCommand)
        return command
    return None
