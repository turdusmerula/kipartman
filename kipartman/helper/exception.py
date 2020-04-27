from configuration import configuration
import sys, traceback


def print_stack():
    if configuration.debug:
#        traceback.print_stack()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, file=sys.stdout)

def print_callstack():
    for line in traceback.format_stack()[:-2]:
        print(line.strip())
