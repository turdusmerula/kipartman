import urllib.request
from configuration import configuration

class ConnectionException(Exception):
    def __init__(self, error):
        super(ConnectionException, self).__init__(error)

def check_backend(throw_error=True):
    try:
        data = urllib.request.urlopen(configuration.kipartbase+"/api/swagger.json")
    except:
        raise ConnectionException("Error connecting to "+configuration.kipartbase)
    
def check_url(url, throw_error=True):
    pass

def check_octopart(url, throw_error=True):
    pass

def check_snapeda(url, throw_error=True):
    pass
