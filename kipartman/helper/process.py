import multiprocessing
from helper.debugtools import print_callstack

# TODO implement https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing
try:
    multiprocessing.set_start_method('forkserver')
except:
    pass

class Lock(object):
    def __init__(self):
        self._lock = multiprocessing.RLock()
        
    def __enter__(self):
#         print_callstack()
#         print(f"-> {self}: lock")
        self._lock.acquire()
        return self
          
    def __exit__(self, *args):
#         print(f"<- {self}: unlock")
        self._lock.release()


class Process(multiprocessing.Process):
    def __init__(self, *argv, **kwargs):
        self._stop_event = multiprocessing.Event() 
        self._pause_lock = Lock()
        
        super(Process, self).__init__(*argv, target=self._run, args=(self._stop_event, self._pause_lock), **kwargs)

    def __del__(self):
        self.stop()
        
    def stop(self): 
        self._stop_event.set()

    def stopped(self): 
        return self._stop_event.is_set() 
 
    def pause(self): 
        self._pause_lock.acquire()

    def resume(self):
        self._pause_lock.release()
        
    def init(self):
        pass

    def step(self):
        pass
    
    def _run(self, stop_event, pause_lock, *args, **kwargs):
        self._stop_event = stop_event
        self._pause_lock = pause_lock
        
        self.init(*args, **kwargs)
        
        while self.stopped()==False:
            with self._pause_lock:    # if lock is taken process is paused
                self.step()
