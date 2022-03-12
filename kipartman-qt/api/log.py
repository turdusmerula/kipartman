import io
import logging
import sys
import traceback

FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT)

class Logger():
    def __init__(self):
        self.log = logging.getLogger('console')
        self.log.setLevel('DEBUG') # default log mode warning

    def _sprint(self, *args, **kwargs):
        ss = io.StringIO()
        print(*args, **kwargs, file=ss)

        ss.seek(0)
        lines = [s.rstrip() for s in ss.readlines()]
        if len(lines)==0:
            return ""
        elif len(lines)==1:
            return lines[0]
        else:
            res = lines[0]
            for s in lines[1:]:
                res += "\n"+s
            return res
        
    def debug(self, *args, stack=False, **kwargs):
        if stack:
            tb = self.get_stack()
            if tb=="":
                s = self._sprint(*args, **kwargs)
            else:
                s = self._sprint(*args, f"\n  ----\n{stack}", **kwargs)
        else:
                s = self._sprint(*args, **kwargs)            
        self.log.debug(s)
    
    def info(self, *args, **kwargs):
        self.log.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.log.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        stack = self.get_stack()
        if stack=="":
            s = self._sprint(*args, **kwargs)
        else:
            s = self._sprint(*args, f"\n  ----\n{stack}", **kwargs)
        self.log.error(s)
        
    def fatal(self, *args, **kwargs):
        self.log.fatal(*args, **kwargs)

    
    def setLevel(self, level):
        self.log.setLevel(level)


    def print_stack(self):
        # if log.level==10:
    #        traceback.print_stack()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, file=sys.stderr, limit=None)
    
    def print_callstack(self):
        # if log.level==10:
        for line in traceback.format_stack()[:-2]:
            print(line.strip())
    
    def get_stack(self, prefix="", level=0, limit=None):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        ss = io.StringIO()
        if exc_traceback is not None:
            traceback.print_tb(exc_traceback, file=ss, limit=limit)
    
            ss.seek(0)
            lines = ss.readlines()
            return f"{prefix}".join(lines)
        else:
            stack = traceback.extract_stack(limit=limit)[:-2]
            # traceback.print_tb(stack, file=ss)
            return f"{prefix}".join(traceback.format_list(stack))
            # ss.seek(0)
            # lines = ss.readlines()
            # return f"{prefix}".join(lines)
        return ""
    
            # if limit is not None:
            #     lines = ss.readlines()[-level:limit]
        # else:
        #     lines = ss.readlines()[-level:]
            

log = Logger()
