import re
from xcopilot.parser import parseToFloat, parseToBoolean

VALUE_PARSER_MAP = {
    'custom': None,
    'float': parseToFloat,
    'boolean': parseToBoolean
}

class Command:
    def __init__(self, name, config):
        self.name = name
        self.regex = re.compile(config['regex'], re.IGNORECASE)
        self.dataRefs = config['dataRefs']
        self.parseValue = config.get('parseValue')
        self.value = None

    def recognizeCommand(self, strCommand):
        return self.regex.match(strCommand) is not None

    def parseCommand(self, strCommand):
        match = self.regex.match(strCommand)
        for key in self.regex.groupindex:
            if key in VALUE_PARSER_MAP:
                if (self.parseValue is None):
                    valueParser = VALUE_PARSER_MAP[key]
                    self.value = valueParser(match.group(key))
                else:
                    self.value = self.parseValue(match.group(key))

class CommandProcessor:
    def __init__(self):
        self.commands = []

    def setConfig(self, aircraftConfig):
        self.commands = []
        for name, config in aircraftConfig.iteritems():
            self.commands.append(Command(name, config))

    def parseCommand(self, strCommand):
        for command in self.commands:
            if command.recognizeCommand(strCommand):
                command.parseCommand(strCommand)
                return command
        return None
