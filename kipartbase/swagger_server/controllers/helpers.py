from swagger_server.models.error import Error

class ControllerError(BaseException):
    def __init__(self, error):
        self.error = error
        
def raise_on_error(value):
    if isinstance(value, Error):
        print value
        raise ControllerError(value)
    return value