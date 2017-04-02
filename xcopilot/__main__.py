from xcopilot.main import XCopilot
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
xcopilot = XCopilot()
xcopilot.configureForAircraft()
logger.info('Say a command!')
result = xcopilot.recordCommand()
