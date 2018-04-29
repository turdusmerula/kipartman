import traceback
import datetime, logging
def debugprint(msg):
    stack = [l for l in traceback.extract_stack() if not('debugger.py' in l[0])]
    #print('DEBUG: {}, message:{}'.format(stack[-3][3], msg))
    try:
        if 'logging' in globals():logging.debug(
                "{:%H:%M:%S.%f} STACKTRACE: {}, message:{}".format(
                        datetime.datetime.now(),
                        stack[-3][3], msg
                        ))
    except:
        pass