import logging

FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT)

log = logging.getLogger('console')
log.setLevel('ERROR') # default log mode warning

def get_log_level():
    if log.level==10:
        return "debug"
    elif log.level==20:
        return "info"
    elif log.level==30:
        return "warning"
    elif log.level==40:
        return "error"
    else:
        return "fatal"

def set_log_level(level):
    if level is None or level=='fatal':
        log.setLevel('CRITICAL')        
    elif level=='error':
        log.setLevel('ERROR')
    elif level=='warning':
        log.setLevel('WARNING')
    elif level=='info':
        log.setLevel('INFO')
    elif level=='debug':
        log.setLevel('DEBUG')
            