registry = {}
def register(cls):
    registry[cls.__name__] = cls
    return cls

def registered(cls):
    return registry.has_key(cls)

def registered_model(cls):
    return registry[cls]
