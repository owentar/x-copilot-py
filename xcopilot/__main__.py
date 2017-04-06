from xcopilot.main import XCopilot
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
xcopilot = XCopilot()
xcopilot.configureForAircraft()
logger.info('Say a command...')
result = xcopilot.recordCommand()
