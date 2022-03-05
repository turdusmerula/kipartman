import subprocess
import sys

def raised(func, *args, **kwargs):
    res = False
    try:
        func(*args,**kwargs)
    except Exception as e:
        res = [type(e), f"{e}"]
        print(f"Raised {type(e)}: {e}")
    return res

def run(command, merge=False):
    if merge:
        res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = res.stdout.decode().split('\n')
        if stdout[-1]=='':
            stdout = stdout[:-1]
        return res.returncode, stdout
    else:
        res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = res.stdout.decode().split('\n')
        if stdout[-1]=='':
            stdout = stdout[:-1]
        stderr = res.stderr.decode().split('\n')
        if stderr[-1]=='':
            stderr = stderr[:-1]
        return res.returncode, stdout, stderr

class redirect_stdout(object): 
    def __init__(self, dest_stream): 
        self.dest_stream = dest_stream
        
    def __enter__(self):
        sys.stdout = self.dest_stream
        
    def __exit__(self, exc_type, exc_value, tb): 
        sys.stdout = sys.__stdout__

class redirect_stderr(object): 
    def __init__(self, dest_stream): 
        self.dest_stream = dest_stream
        
    def __enter__(self):
        sys.stderr = self.dest_stream
        
    def __exit__(self, exc_type, exc_value, tb): 
        sys.stderr = sys.__stderr__
