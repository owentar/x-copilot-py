import unittest
from mock import patch
from xcopilot.config import CommandDataRefProvider, DataRef

class CommandDataRefProviderTest(unittest.TestCase):

    AIRCRAFT_ID = ('TEST', 'TEST', 'TEST')

    def setUp(self):
        DataRef['DEFAULT_COMMAND'] = 'DEFAULT_DATA_REF'

    @patch('xcopilot.config.dataref.FJS727')
    def test_whenSpecificAircraftDataRefExist_mergeAircraftDataRefWithDefault(self, mock_config):
        aircraftDataRef = {
            'Identifier': { 'author': 'TEST', 'ICAO': 'TEST', 'description': 'TEST' },
            'DataRef': { 'TEST_COMMAND': 'TEST', 'DEFAULT_COMMAND': 'OVERRIDE' }
        }
        mock_config.configure_mock(**aircraftDataRef)
        commandDataRefProvider = CommandDataRefProvider()
        dataRef = commandDataRefProvider.get(self.AIRCRAFT_ID)
        self.assertEqual(dataRef.get('DEFAULT_COMMAND'), 'OVERRIDE')
        self.assertEqual(dataRef.get('TEST_COMMAND'), 'TEST')

    @patch('xcopilot.config.dataref.FJS727')
    def test_whenNoSpecificAircraftDataRefExist_defaultAircraftDataRefIsReturned(self, mock_config):
        aircraftDataRef = {
            'Identifier': { 'author': 'TEST2', 'ICAO': 'TEST2', 'description': 'TEST2' },
            'DataRef': { 'TEST_COMMAND': 'TEST' }
        }
        mock_config.configure_mock(**aircraftDataRef)
        commandDataRefProvider = CommandDataRefProvider()
        dataRef = commandDataRefProvider.get(self.AIRCRAFT_ID)
        self.assertEqual(dataRef.get('DEFAULT_COMMAND'), 'DEFAULT_DATA_REF')
        self.assertIsNone(dataRef.get('TEST_COMMAND'))
