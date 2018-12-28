from urllib.request import urlopen
import re
# TODO: asynchronous load
# TODO: store previous values in database
class Currency(object):
    def __init__(self):
        self.base = 'EUR'
        self.currencies = {}
        self.load()
        
    def load(self):
        data = ''
        with urlopen('http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml') as url:
            data = str(url.read())

        self.currencies = {}
        
        # add EUR
        self.currencies['EUR'] = 1.
        
        # add others
        for line in data.split('\\n'):
            if 'currency=' in line:
                currency = None
                rate = None
                m = re.match(".*currency=.*'([A-Z][A-Z]*).*'", line)
                if m:
                    currency = m.group(1)
                m = re.match(".*rate=.*'([0-9.][0-9.]*).*'", line)
                if m:
                    rate = float(m.group(1))
                if currency and rate:
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