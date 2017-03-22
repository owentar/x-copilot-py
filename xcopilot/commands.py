import re
from xcopilot.parser import parseToFloat, parseToBoolean
from xcopilot.config import CommandConfig

VALUE_PARSER_MAP = {
    'custom': None,
    'float': parseToFloat,
    'boolean': parseToBoolean
}

class Command:
    def __init__(self, name, config):
        self.name = name
        self.regex = re.compile(config['regex'], re.IGNORECASE)
        self.parseValue = config.get('parseValue')
        self.type = config.get('type')
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
                    self.type = key
                else:
                    self.value = self.parseValue(match.group(key))

class CommandProcessor:
    def __init__(self):
        self.commands = []
        for name, config in CommandConfig.iteritems():
            self.commands.append(Command(name, config))

    def parseCommand(self, strCommand):
        for command in self.commands:
            if command.recognizeCommand(strCommand):
                command.parseCommand(strCommand)
                return command
        return None
