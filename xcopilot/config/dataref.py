import pkgutil
import importlib
from xcopilot.config import aircraft
from xcopilot.config.aircraft import *
import logging

DataRef = {
    'SET_ALTIMETER': [
        { 'name': 'sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot', 'type': 'float' },
        { 'name': 'sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot', 'type': 'float' }
    ],
    'SET_ALTITUDE': [{ 'name': 'sim/cockpit2/autopilot/altitude_dial_ft', 'type': 'float' }],
    'LANDING_GEAR': [{ 'name': 'sim/cockpit2/controls/gear_handle_down', 'type': 'boolean' }],
    'LANDING_LIGHTS': [{ 'name': 'sim/cockpit2/switches/landing_lights_on', 'type': 'int' }],
    'TAXI_LIGHT': [{ 'name': 'sim/cockpit2/switches/taxi_light_on', 'type': 'int' }],
    'NAV_LIGHTS': [{ 'name': 'sim/cockpit2/switches/navigation_lights_on', 'type': 'int' }],
    'STROBE_LIGHTS': [{ 'name': 'sim/cockpit2/switches/strobe_lights_on', 'type': 'int' }],
    'BEACON_LIGHTS': [{ 'name': 'sim/cockpit2/switches/beacon_on', 'type': 'int' }]
}

class DataRefProvider:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.dataRefPerAircraft = {}

        for moduleName in aircraft.__all__:
            module = globals()[moduleName]
            dataRefForAircraft = DataRef.copy()
            dataRefForAircraft.update(module.DataRef)
            key = (module.Identifier['author'], module.Identifier['description'], module.Identifier['ICAO'])
            self.dataRefPerAircraft[key] = dataRefForAircraft

    def get(self, aircraftIdentifier):
        self.logger.debug('Found aircraft config: %s', self.dataRefPerAircraft.has_key(aircraftIdentifier))
        return self.dataRefPerAircraft.get(aircraftIdentifier, DataRef)
