import threading
import multiprocessing
from helper.debugtools import print_callstack

# TODO implement https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing

class Lock(object):
    def __init__(self):
        self._lock = threading.RLock()
        
    def __enter__(self):
#         print_callstack()
#         print(f"-> {self}: lock")
        self._lock.acquire()
        return self
          
    def __exit__(self, *args):
#         print(f"<- {self}: unlock")
        self._lock.release()


class ObjectLock(object):
    def __init__(self, obj):
        self._lock = threading.RLock()
        self._obj = obj
        
    def __enter__(self):
        self._lock.acquire()
        return self._obj
          
    def __exit__(self, *args):
        self._lock.release()

class Thread(threading.Thread):
    def __init__(self):
        super(Thread, self).__init__()
        self._stop_event = threading.Event() 
        self._lock = Lock()

    def __del__(self):
        self.stop()
        
    def stop(self): 
        self._stop_event.set()
        
    def stopped(self): 
        return self._stop_event.isSet() 
 
    def pause(self): 
        self._lock.acquire()

    def resume(self):
        self._lock.release()

        
    def init(self):
        """ executed inside thread """
        """ to override to provide thread initialization """
        pass

    def step(self):
        """ executed inside thread """
        """ to override to provide thread behavior """
        pass
    
    def run(self):
        self.init()
        
        while self.stopped()==False:
            with self._lock:    # if lock is taken thread is paused
                self.step()
