import json
import urllib
import re
# TODO: asynchronous load
# TODO: store previous values in database
class Currency(object):
    def __init__(self):
        self.base = 'EUR'
        self.currencies = {}
        self.load()
        
    def load(self):
        data = urllib.urlopen('http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml').read()
        self.currencies = {}
        for line in data.split('\n'):
            if 'currency=' in line:
                m = re.match(".*currency='(.*)' rate='(.*)'.*", line)
                if m:
                    currency = m.group(1)
                    rate = float(m.group(2))
                    self.currencies[currency] = rate
        print("Currencies: ", self.currencies)
        return self.currencies
        
    def convert(self, value, source, target):
        if source==self.base:
            rate_source_base = 1
        else:
            rate_source_base = self.currencies[source]
        if target==self.base:
            rate_source_target = 1
        else:
            rate_source_target = self.currencies[target]
        
        res = 0
        # convert source to base
        res = value/rate_source_base
        # convert base to target
        res = res*rate_source_target
        
        return res