import unittest
from mock import patch, MagicMock
from xcopilot.main import XCopilot

class XCopilotTest(unittest.TestCase):

    @patch('xcopilot.config.configprovider.ConfigProvider')
    @patch('xcopilot.main.Recognizer')
    def setUp(self, mock_recognizer, mock_configProvider):
        self.mock_recognizer = mock_recognizer.return_value
        self.mock_recognizer.listen.return_value = None
        self.mock_recognizer.recognize_sphinx2.return_value = 'set altimeter two nine nine two'
        self.mock_configProvider = mock_configProvider.return_value
        self.xcopilot = XCopilot()
        self.mock_mic = MagicMock()
        self.xcopilot.getMicrophone = lambda: self.mock_mic
        self.xcopilot.configureForAircraft(('DEFAULT', 'DEFAULT', 'DEFAULT'))

    def test_onRecordCommand_shouldListenTheMicrophone(self):
        self.xcopilot.recordCommand()
        self.mock_recognizer.listen.assert_called_once

    def test_whenCommandIsRecognized_returnsCommandWithDataRefs(self):
        command = self.xcopilot.recordCommand()
        self.assertEqual('SET_ALTIMETER', command.name)
        self.assertEqual(29.92, command.value)
        self.assertEqual('sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot', command.dataRefs[0]['name'])
        self.assertEqual('sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot', command.dataRefs[1]['name'])
