from functools import wraps

# utility tool to add member methods to a class
# usage:
#@add_method(MyClass)
#def my_method(self, params):
#    pass
def add_method(cls):
    def decorator(func):
        @wraps(func) 
        def wrapper(self, *args, **kwargs): 
            return func(self, *args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator

def overload_method(cls):
    def decorator(func):
        setattr(func, "_overload_", getattr(cls, func.__name__))
        
        @wraps(func) 
        def wrapper(self, *args, **kwargs): 
            
            return func(self, getattr(func, "_overload_"), *args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator
    