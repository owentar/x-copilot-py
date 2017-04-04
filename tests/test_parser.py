import unittest
from xcopilot.parser import *

class ParserTest(unittest.TestCase):

    def test_sanitizeNumberValue(self):
        self.assertEqual(sanitizeNumberValue(' one    two three   '), '123')
        self.assertEqual(sanitizeNumberValue('zero one two three four five six seven eight nine'), '0123456789')

    def test_parseToFloat(self):
        self.assertEqual(parseToFloat('one five'), 15.0)

    def test_parseToBoolean(self):
        self.assertEqual(parseToBoolean('on'), 1)
        self.assertEqual(parseToBoolean('off'), 0)
        self.assertEqual(parseToBoolean('down'), 1)
        self.assertEqual(parseToBoolean('up'), 0)
