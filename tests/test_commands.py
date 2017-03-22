import unittest
from xcopilot.commands import CommandProcessor

class CommandProcessorTest(unittest.TestCase):

    def _assertCommand(self, command, name, value, cType):
        self.assertIsNotNone(command, 'Command unrecognized')
        self.assertEqual(command.name, name)
        self.assertEqual(command.value, value)
        self.assertEqual(command.type, cType)

    def _assertSetAltimeterCommand(self, command, value, cType):
        self._assertCommand(command, 'SET_ALTIMETER', value, cType)

    def _assertSetAltitudeCommand(self, command, value, cType):
        self._assertCommand(command, 'SET_ALTITUDE', value, cType)

    def _assertLandingLightsCommand(self, command, value, cType):
        self._assertCommand(command, 'LANDING_LIGHTS', value, cType)

    def setUp(self):
        self.commandProcessor = CommandProcessor()

    def test_support_SET_ALTIMETER_command(self):
        self._assertSetAltimeterCommand(self.commandProcessor.parseCommand('set altimeter 2992'), 29.92, 'float')
        self._assertSetAltimeterCommand(self.commandProcessor.parseCommand('set altimeter 2 99 2'), 29.92, 'float')
        self._assertSetAltimeterCommand(self.commandProcessor.parseCommand('set altimeter 2 9 9 2'), 29.92, 'float')
        self._assertSetAltimeterCommand(self.commandProcessor.parseCommand('set altimeter two nine nine two'), 29.92, 'float')
        self._assertSetAltimeterCommand(self.commandProcessor.parseCommand('set altimeter two 9 nine 2'), 29.92, 'float')
        self._assertSetAltimeterCommand(self.commandProcessor.parseCommand('set altimeter three zero zero 0'), 30.00, 'float')
        self._assertSetAltimeterCommand(self.commandProcessor.parseCommand('set altimeter three zero one two'), 30.12, 'float')

    def test_support_SET_ALTITUDE_command(self):
        self._assertSetAltitudeCommand(self.commandProcessor.parseCommand('set altitude one zero three'), 103, 'float')
        self._assertSetAltitudeCommand(self.commandProcessor.parseCommand('set altitude two nine zero zero'), 2900, 'float')
        self._assertSetAltitudeCommand(self.commandProcessor.parseCommand('set altitude three five eight zero zero'), 35800, 'float')

    def test_support_LANDING_LIGHTS_command(self):
        self._assertLandingLightsCommand(self.commandProcessor.parseCommand('landing light on'), 1, 'boolean')
        self._assertLandingLightsCommand(self.commandProcessor.parseCommand('landing light off'), 0, 'boolean')
        self._assertLandingLightsCommand(self.commandProcessor.parseCommand('landing lights on'), 1, 'boolean')
        self._assertLandingLightsCommand(self.commandProcessor.parseCommand('landing lights off'), 0, 'boolean')
