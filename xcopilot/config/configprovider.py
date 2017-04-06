from xcopilot.config import DefaultCommands, aircraft
from xcopilot.config.aircraft import *
import logging

class ConfigProvider:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.configPerAircraft = {}

        for moduleName in aircraft.__all__:
            module = globals()[moduleName]
            key = (module.Identifier['author'], module.Identifier['description'], module.Identifier['ICAO'])
            self.configPerAircraft[key] = moduleName

    def get(self, aircraftIdentifier):
        if aircraftIdentifier in self.configPerAircraft:
            self.logger.debug('Config for %s found.', aircraftIdentifier)
            module = globals()[self.configPerAircraft[aircraftIdentifier]]
            configForAircraft = DefaultCommands.copy()
            configForAircraft.update(module.Commands)
            return configForAircraft
        else:
            self.logger.debug('Config for %s not found. Using default commands.', aircraftIdentifier)
            return DefaultCommands
