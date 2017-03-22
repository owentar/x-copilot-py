import pkgutil
import importlib
from xcopilot.config import aircraft
from xcopilot.config.aircraft import *

DataRef = {
    'SET_ALTIMETER': ['sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot', 'sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot'],
    'SET_ALTITUDE': ['sim/cockpit2/autopilot/altitude_dial_ft'],
    'LANDING_LIGHTS': ['sim/cockpit2/switches/landing_lights_on'],
    'TAXI_LIGHT': ['sim/cockpit2/switches/taxi_light_on'],
    'NAVIGATION_LIGHTS': ['sim/cockpit2/switches/navigation_lights_on'],
    'STROBE_LIGHTS': ['sim/cockpit2/switches/strobe_lights_on'],
    'BEACON_LIGHT': ['sim/cockpit2/switches/beacon_on']
}

class CommandDataRefProvider:
    def __init__(self):
        self.dataRefPerAircraft = {}

        for moduleName in aircraft.__all__:
            module = globals()[moduleName]
            dataRefForAircraft = DataRef.copy()
            dataRefForAircraft.update(module.DataRef)
            key = (module.Identifier['author'], module.Identifier['description'], module.Identifier['ICAO'])
            self.dataRefPerAircraft[key] = dataRefForAircraft

    def get(self, aircraftIdentifier):
        return self.dataRefPerAircraft.get(aircraftIdentifier, DataRef)
