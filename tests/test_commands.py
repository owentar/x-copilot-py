import unittest
from xcopilot.commands import CommandProcessor
from xcopilot.config import DefaultCommands

class CommandProcessorTest(unittest.TestCase):

    def _assertCommand(self, command, name, value):
        self.assertIsNotNone(command, 'Command unrecognized')
        self.assertEqual(command.name, name)
        self.assertEqual(command.value, value)

    def _assertCommandNotRecognized(self, command):
        self.assertIsNone(command, 'Command recognized when it should not')

    def setUp(self):
        self.commandProcessor = CommandProcessor()
        self.commandProcessor.setConfig(DefaultCommands)

    def test_support_SET_ALTIMETER_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter 2992'), 'SET_ALTIMETER', 29.92)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter 2 99 2'), 'SET_ALTIMETER', 29.92)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter 2 9 9 2'), 'SET_ALTIMETER', 29.92)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter two nine nine two'), 'SET_ALTIMETER', 29.92)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter two 9 nine 2'), 'SET_ALTIMETER', 29.92)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter three zero zero 0'), 'SET_ALTIMETER', 30.00)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter three zero one two'), 'SET_ALTIMETER', 30.12)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter one zero one three'), 'SET_ALTIMETER', 1013 * 0.0295301)

    def test_support_SET_ALTITUDE_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('set altitude one zero three'), 'SET_ALTITUDE', 103)
        self._assertCommand(self.commandProcessor.parseCommand('set altitude two nine zero zero'), 'SET_ALTITUDE', 2900)
        self._assertCommand(self.commandProcessor.parseCommand('set altitude three five eight zero zero'), 'SET_ALTITUDE', 35800)

    def test_support_FLIGHT_LEVEL_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('set flight level three five zero'), 'FLIGHT_LEVEL', 35000)
        self._assertCommand(self.commandProcessor.parseCommand('flight level zero five zero'), 'FLIGHT_LEVEL', 5000)

    def test_support_LANDING_GEAR_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('landing gear up'), 'LANDING_GEAR', 0)
        self._assertCommand(self.commandProcessor.parseCommand('landing gear down'), 'LANDING_GEAR', 1)
        self._assertCommand(self.commandProcessor.parseCommand('gear up'), 'LANDING_GEAR', 0)
        self._assertCommand(self.commandProcessor.parseCommand('gear down'), 'LANDING_GEAR', 1)

    def test_support_FLAPS_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('flaps up'), 'FLAPS', 0)
        self._assertCommand(self.commandProcessor.parseCommand('flaps down'), 'FLAPS', 1)

    def test_support_SET_NAV1_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('set nav one to one zero eight decimal two five'), 'SET_NAV1', 10825)
        self._assertCommand(self.commandProcessor.parseCommand('set nav one to one zero eight two zero'), 'SET_NAV1', 10820)
        self._assertCommand(self.commandProcessor.parseCommand('set nav one to one zero eight decimal two'), 'SET_NAV1', 10820)
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set nav one to one zero eight decimal five one'))
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set nav one to one zero eight decimal five two'))
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set nav one to one zero eight decimal five three'))
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set nav one to one zero eight decimal five four'))
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set nav one to one zero eight decimal five six'))
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set nav one to one zero eight decimal five sevem'))
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set nav one to one zero eight decimal five eight'))
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set nav one to one zero eight decimal five nine'))

    def test_support_SET_COM1_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('set com one to one one eight decimal two five'), 'SET_COM1', 11825)
        self._assertCommand(self.commandProcessor.parseCommand('set com one to one one eight two seven'), 'SET_COM1', 11827)
        self._assertCommand(self.commandProcessor.parseCommand('set com one to one one eight decimal two'), 'SET_COM1', 11820)
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set com one to one zero eight decimal five zero'))
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set com one to one three eight five'))

    def test_support_SET_HEADING_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('set heading zero zero zero'), 'SET_HEADING', 000)
        self._assertCommand(self.commandProcessor.parseCommand('set heading three six zero'), 'SET_HEADING', 360)
        self._assertCommand(self.commandProcessor.parseCommand('set heading zero seven four'), 'SET_HEADING', 74)
        self._assertCommand(self.commandProcessor.parseCommand('set heading one seven six'), 'SET_HEADING', 176)
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set heading four seven four'))
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set heading three seven two'))

    def test_support_HEADING_SELECT_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('heading select off'), 'HEADING_SELECT', 0)
        self._assertCommand(self.commandProcessor.parseCommand('heading select on'), 'HEADING_SELECT', 1)

    def test_support_SET_SPEED_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('set speed zero zero zero'), 'SET_SPEED', 000)
        self._assertCommand(self.commandProcessor.parseCommand('set speed one two zero'), 'SET_SPEED', 120)
        self._assertCommand(self.commandProcessor.parseCommand('set speed one eight nine'), 'SET_SPEED', 189)
        self._assertCommand(self.commandProcessor.parseCommand('set speed two five zero'), 'SET_SPEED', 250)
        self._assertCommand(self.commandProcessor.parseCommand('set speed three two zero'), 'SET_SPEED', 320)
        self._assertCommandNotRecognized(self.commandProcessor.parseCommand('set speed four zero zero'))

    def test_support_SPEED_SELECT_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('speed select off'), 'SPEED_SELECT', 0)
        self._assertCommand(self.commandProcessor.parseCommand('speed select on'), 'SPEED_SELECT', 1)

    def test_support_LANDING_LIGHTS_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('landing light on'), 'LANDING_LIGHTS', 1)
        self._assertCommand(self.commandProcessor.parseCommand('landing light off'), 'LANDING_LIGHTS', 0)
        self._assertCommand(self.commandProcessor.parseCommand('landing lights on'), 'LANDING_LIGHTS', 1)
        self._assertCommand(self.commandProcessor.parseCommand('landing lights off'), 'LANDING_LIGHTS', 0)

    def test_support_TAXI_LIGHTS_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('taxi lights off'), 'TAXI_LIGHTS', 0)
        self._assertCommand(self.commandProcessor.parseCommand('taxi lights on'), 'TAXI_LIGHTS', 1)
        self._assertCommand(self.commandProcessor.parseCommand('taxi light off'), 'TAXI_LIGHTS', 0)
        self._assertCommand(self.commandProcessor.parseCommand('taxi light on'), 'TAXI_LIGHTS', 1)

    def test_support_NAV_LIGHTS_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('navigation lights off'), 'NAV_LIGHTS', 0)
        self._assertCommand(self.commandProcessor.parseCommand('navigation lights on'), 'NAV_LIGHTS', 1)
        self._assertCommand(self.commandProcessor.parseCommand('navigation light off'), 'NAV_LIGHTS', 0)
        self._assertCommand(self.commandProcessor.parseCommand('navigation light on'), 'NAV_LIGHTS', 1)

    def test_support_STROBE_LIGHTS_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('strobe lights off'), 'STROBE_LIGHTS', 0)
        self._assertCommand(self.commandProcessor.parseCommand('strobe lights on'), 'STROBE_LIGHTS', 1)
        self._assertCommand(self.commandProcessor.parseCommand('strobe light off'), 'STROBE_LIGHTS', 0)
        self._assertCommand(self.commandProcessor.parseCommand('strobe light on'), 'STROBE_LIGHTS', 1)

    def test_support_BEACON_LIGHTS_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('beacon lights off'), 'BEACON_LIGHTS', 0)
        self._assertCommand(self.commandProcessor.parseCommand('beacon lights on'), 'BEACON_LIGHTS', 1)
        self._assertCommand(self.commandProcessor.parseCommand('beacon light off'), 'BEACON_LIGHTS', 0)
        self._assertCommand(self.commandProcessor.parseCommand('beacon light on'), 'BEACON_LIGHTS', 1)
