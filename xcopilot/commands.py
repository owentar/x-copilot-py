import re

class Command(object):
    def __init__(self, name, regex):
        self.name = name
        self.regex = re.compile(regex, re.IGNORECASE)
        self.value = None
        self.dataRefs = {}

    def recognizeCommand(self, strCommand):
        return self.regex.match(strCommand) is not None

    def parseCommand(self, strCommand):
        pass

    def _sanitizeValue(self, value):
        return value.strip().lower().replace('zero', '0').replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4').replace('five', '5').replace('six', '6').replace('seven', '7').replace('eight', '8').replace('nine', '9').replace(' ', '')


class SetAltimeterCommand(Command):
    def __init__(self):
        super(SetAltimeterCommand, self).__init__('SET_ALTIMETER', '^set altimeter (?P<number>((\d|zero|one|two|three|four|five|six|seven|eight|nine)\s?){4})$')

    def parseCommand(self, strCommand):
        match = self.regex.match(strCommand)
        value = self._sanitizeValue(match.group('number'))
        self.value = float(value[:2] + '.' + value[2:])
        self.dataRefs['sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot'] = self.value
        self.dataRefs['sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot'] = self.value

class SetAltitudeCommand(Command):
    def __init__(self):
        super(SetAltitudeCommand, self).__init__('SET_ALTITUDE', '^set altitude (?P<number>((\d|zero|one|two|three|four|five|six|seven|eight|nine)\s?){3,5})$')

    def parseCommand(self, strCommand):
        match = self.regex.match(strCommand)
        self.value = float(self._sanitizeValue(match.group('number')))
        self.dataRefs['sim/cockpit2/autopilot/altitude_dial_ft'] = self.value

class LandingLightsCommand(Command):
    def __init__(self):
        super(LandingLightsCommand, self).__init__('LANDING_LIGHTS', '^landing light[s]? (?P<boolean>on|off)$')

    def parseCommand(self, strCommand):
        match = self.regex.match(strCommand)
        self.value = 1 if match.group('boolean').lower() == 'on' else 0
        self.dataRefs['FJS/727/lights/OutboundLLSwitch_L'] = self.value
        self.dataRefs['FJS/727/lights/OutboundLLSwitch_R'] = self.value
        self.dataRefs['FJS/727/lights/InboundLLSwitch_L'] = self.value
        self.dataRefs['FJS/727/lights/InboundLLSwitch_R'] = self.value

def parseCommand(strCommand):
    commands = [SetAltimeterCommand(), SetAltitudeCommand(), LandingLightsCommand()]
    for command in commands:
        if command.recognizeCommand(strCommand):
            command.parseCommand(strCommand)
            return command
    return None
