import unittest
from mock import patch
from xcopilot.config import ConfigProvider, DefaultCommands

class ConfigProviderTest(unittest.TestCase):

    AIRCRAFT_ID = ('TEST', 'TEST', 'TEST')

    def setUp(self):
        DefaultCommands['DEFAULT_COMMAND'] = 'DEFAULT_VALUE'

    def tearDown(self):
        del DefaultCommands['DEFAULT_COMMAND']

    @patch('xcopilot.config.configprovider.FJS727')
    def test_whenSpecificAircraftConfigExist_mergeAircraftConfigWithDefault(self, mock_config):
        aircraftConfig = {
            'Identifier': { 'author': 'TEST', 'ICAO': 'TEST', 'description': 'TEST' },
            'Commands': { 'TEST_COMMAND': 'TEST', 'DEFAULT_COMMAND': 'OVERRIDE' }
        }
        mock_config.configure_mock(**aircraftConfig)
        configProvider = ConfigProvider()
        config = configProvider.get(self.AIRCRAFT_ID)
        self.assertEqual(config.get('DEFAULT_COMMAND'), 'OVERRIDE')
        self.assertEqual(config.get('TEST_COMMAND'), 'TEST')

    @patch('xcopilot.config.configprovider.FJS727')
    def test_whenNoSpecificAircraftConfigExist_defaultConfigIsReturned(self, mock_config):
        aircraftConfig = {
            'Identifier': { 'author': 'TEST2', 'ICAO': 'TEST2', 'description': 'TEST2' },
            'Commands': { 'TEST_COMMAND': 'TEST' }
        }
        mock_config.configure_mock(**aircraftConfig)
        configProvider = ConfigProvider()
        config = configProvider.get(self.AIRCRAFT_ID)
        self.assertEqual(config.get('DEFAULT_COMMAND'), 'DEFAULT_VALUE')
        self.assertIsNone(config.get('TEST_COMMAND'))
