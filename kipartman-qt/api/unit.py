from pint import UnitRegistry, set_application_registry

# https://pint.readthedocs.io/en/stable/tutorial.html

# ureg = UnitRegistry(system='SI')
ureg = UnitRegistry()
ureg.default_format = "P~"
# Q_ = ureg.Quantity

set_application_registry(ureg)

class UnitValue():
    def __init__(self, value=None, unit=None):
        self.value = value
        self.unit = unit
        
    def from_dict(self, d):
        if 'value' in d:
            self.value = d['value']
        if 'unit' in d:
            self.unit = d['unit']
    
    def from_str(self, s):
        self.value = ureq.quantity(s).quantity
        self.unit = ureq.quantity(s).unit
        
    def to_dict(self):
        return {'value': self.value, 'unit': self.unit}

    def __str__(self):
        if self.unit is not None:
            return str(ureg.Quantity(self.value, self.unit))
        else:
            return str(self.value)

class UnitRange():
    def __init__(self, min: UnitValue=None, max: UnitValue=None):
        self.min = value
        self.max = unit
    
class UnitList():
    def __init__(self, values=[]):
        self.values = values
    
    def __len__(self):
        return len(self.values)

