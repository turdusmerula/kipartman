import json
import urllib

# TODO: asynchronous load
# TODO: store previous values in database
class Currency(object):
    def __init__(self, base):
        self.base = base
        self.currencies = []
        self.load()
        
    def load(self):
        data = urllib.urlopen('http://api.fixer.io/latest?base='+self.base).read()
        self.currencies = json.loads(data)
        print("Currencies: ", self.currencies)
        return self.currencies
        
    def convert(self, value, source, target):
        rates = self.currencies['rates']
        
        if source==self.base:
            rate_source_base = 1
        else:
            rate_source_base = rates[source]
        if target==self.base:
            rate_source_target = 1
        else:
            rate_source_target = rates[target]
        
        res = 0
        # convert source to base
        res = value/rate_source_base
        # convert base to target
        res = res*rate_source_target
        
        return res