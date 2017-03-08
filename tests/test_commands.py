import unittest
from xcopilot.commands import parseCommand

class TestAltimeterCommand(unittest.TestCase):

    def _assertSetAltimeterCommand(self, command, value):
        self.assertEqual(command.name, "SET_ALTIMETER")
        self.assertEqual(len(command.dataRefs), 2)
        self.assertEqual(command.dataRefs["sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot"], value)
        self.assertEqual(command.dataRefs["sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot"], value)

    def setUp(self):
        pass

    def test_parseCommand_creates_SET_ALTIMETER_command(self):
        self._assertSetAltimeterCommand(parseCommand("set altimeter 2992"), 29.92)
        self._assertSetAltimeterCommand(parseCommand("set altimeter 2 99 2"), 29.92)
        self._assertSetAltimeterCommand(parseCommand("set altimeter 2 9 9 2"), 29.92)
        self._assertSetAltimeterCommand(parseCommand("set altimeter two nine nine two"), 29.92)
        self._assertSetAltimeterCommand(parseCommand("set altimeter two 9 nine 2"), 29.92)
