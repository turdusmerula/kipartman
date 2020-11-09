
class Provider(object):
    providers = []
    
    name = None
    description = None
    
    # capabilities
    has_search_part = False
    
    def __init__(self):
        pass
    
    @classmethod
    def register(cls):
        Provider.providers.append(cls)
    
    @classmethod
    def get_provider(cls, name=None, description=None):
        for provider in cls.providers:
            if ( name is not None and provider.name==name ) or ( description is not None and provider.description==description ):
                return provider
        return None
    
    def CheckConnection(self):
        pass
    
    def SearchPart(self, text):
        return []

class Part(object):
    def __init__(self, data):
        self._data = data
        
    @property
    def name(self):
        return None
    
    @property
    def description(self):
        return None
    
    @property
    def manufacturer(self):
        return None
    
    @property
    def parameters(self):
        return None
    
    @property
    def offers(self):
        return None
    
    @property
    def uid(self):
        return None
    
    @property
    def provider(self):
        return None
    
class Parameter(object):
    def __init__(self, data):
        self._data = data
        
    @property
    def name(self):
        return None
    
    @property
    def value(self):
        return None

class Offer(object):
    def __init__(self, data):
        self._data = data
        
    @property
    def distributor(self):
        return None

    @property
    def sku(self):
        return None
    
    @property
    def stock(self):
        return None

    @property
    def currency(self):
        return None

    @property
    def prices(self):
        return None

class Price(object):
    def __init__(self, data):
        self._data = data

    @property
    def quantity(self):
        return None

    @property
    def price_per_item(self):
        return None
