import logging

FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT)

log = logging.getLogger('console')
log.setLevel('WARNING') # default log mode warning
