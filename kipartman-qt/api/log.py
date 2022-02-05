import logging
import sys

FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT)

log = logging.getLogger('console')
log.setLevel('FATAL') # default log mode warning
