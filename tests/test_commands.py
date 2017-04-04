import unittest
from xcopilot.commands import CommandProcessor

class CommandProcessorTest(unittest.TestCase):

    def _assertCommand(self, command, name, value):
        self.assertIsNotNone(command, 'Command unrecognized')
        self.assertEqual(command.name, name)
        self.assertEqual(command.value, value)

    def setUp(self):
        self.commandProcessor = CommandProcessor()

    def test_support_SET_ALTIMETER_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter 2992'), 'SET_ALTIMETER', 29.92)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter 2 99 2'), 'SET_ALTIMETER', 29.92)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter 2 9 9 2'), 'SET_ALTIMETER', 29.92)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter two nine nine two'), 'SET_ALTIMETER', 29.92)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter two 9 nine 2'), 'SET_ALTIMETER', 29.92)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter three zero zero 0'), 'SET_ALTIMETER', 30.00)
        self._assertCommand(self.commandProcessor.parseCommand('set altimeter three zero one two'), 'SET_ALTIMETER', 30.12)

    def test_support_SET_ALTITUDE_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('set altitude one zero three'), 'SET_ALTITUDE', 103)
        self._assertCommand(self.commandProcessor.parseCommand('set altitude two nine zero zero'), 'SET_ALTITUDE', 2900)
        self._assertCommand(self.commandProcessor.parseCommand('set altitude three five eight zero zero'), 'SET_ALTITUDE', 35800)

    def test_support_LANDING_GEAR_command(self):
        self._assertCommand(self.commandProcessor.parseCommand('landing gear up'), 'LANDING_GEAR', 0)
        self._assertCommand(self.commandProcessor.parseCommand('landing gear down'), 'LANDING_GEAR', 1)
        self._assertCommand(self.commandProcessor.parseCommand('gear up'), 'LANDING_GEAR', 0)
        self._assertCommand(self.commandProcessor.parseCommand('gear down'), 'LANDING_GEAR', 1)

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
