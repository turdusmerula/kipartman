
from profiling.tracing import TracingProfiler
from profiling.sampling import SamplingProfiler

# To use the profiler:
#    with Trace()
#        # some code
#        # some code

class Trace(object):
    def __enter__(self, title='profile'):
        self.profiler = TracingProfiler()
        self.title = title
        self.profiler.start()
        return self.profiler 
    
    def __exit__(self, type, value, traceback):
        self.profiler.stop()
        self.profiler.run_viewer(self.title)
