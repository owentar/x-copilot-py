import unittest
from mock import patch
from xcopilot.main import XCopilot

class XCopilotTest(unittest.TestCase):

    @patch('xcopilot.config.dataref.DataRefProvider')
    @patch('xcopilot.main.sr.Microphone')
    @patch('xcopilot.main.Recognizer')
    def setUp(self, mock_recognizer, mock_microphone, mock_dataRefProvider):
        self.mock_recognizer = mock_recognizer.return_value
        self.mock_recognizer.listen.return_value = None
        self.mock_recognizer.recognize_sphinx2.return_value = 'set altimeter two nine nine two'
        self.mock_dataRefProvider = mock_dataRefProvider.return_value
        self.mock_microphone = mock_microphone.return_value
        self.xcopilot = XCopilot()
        self.xcopilot.configureForAircraft(('DEFAULT', 'DEFAULT', 'DEFAULT'))

    def test_onRecordCommand_shouldListenTheMicrophone(self):
        self.xcopilot.recordCommand()
        self.mock_microphone.listen.assert_called_once

    def test_whenCommandIsRecognized_returnsCommandWithDataRefs(self):
        result = self.xcopilot.recordCommand()
        self.assertEqual('SET_ALTIMETER', result[0].name)
        self.assertEqual(29.92, result[0].value)
        self.assertEqual('float', result[0].type)
        self.assertEqual('sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot', result[1][0])
        self.assertEqual('sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot', result[1][1])
