from swagger_server.models.error import Error

class ControllerError(BaseException):
    def __init__(self, error):
        self.error = error
        
def raise_on_error(value):
    v = value
    if type(value) is tuple:
        v = value[0]
        
    if isinstance(v, Error):
        print(v)
        raise ControllerError(v)


    return value