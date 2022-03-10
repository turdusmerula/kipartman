import pint

# https://pint.readthedocs.io/en/stable/tutorial.html

def _fix_percent(x: str) -> str:
    return x.replace("%%", " per_mille ").replace("%", " percent ")

class UnitRegistry(pint.UnitRegistry):
    def __call__(self, input_string, **kwargs):
        """Hack around `pint#429 <https://github.com/hgrecco/pint/issues/429>`_
        to support % sign
        """
        return super().__call__(_fix_percent(input_string), **kwargs)

    def parse_expression(self, input_string, *args, **kwargs):
        """Allow % sign
        """
        return super().parse_expression(_fix_percent(input_string), *args, **kwargs)

    def parse_units(self, input_string, *args, **kwargs):
        """Allow % sign
        """
        return super().parse_units(_fix_percent(input_string), *args, **kwargs)


# ureg = UnitRegistry(system='SI')
ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)
# ureg.default_format = "P~"
ureg.default_format = "~#P"
# Q_ = ureg.Quantity

# add dimensionless units
ureg.define('percent = 0.01*count = %')

pint.set_application_registry(ureg)

def format_float(v, digits=3, trailing_zeros=False):
    epsilon = 1e-5  

    if v<0:
        sign = -1
    else:
        sign = 1
    v = abs(v)
    
    dec = int(v+0.5)
    frac = abs(v-dec) 
    if frac<epsilon:
        return str(dec*sign) ;
    else:
        s = str(int(round(v, 0)))
        if digits is not None:
            if len(s)<digits:
                s = f"{{:.{digits-len(s)}f}}".format(v*sign)
        if trailing_zeros==False and '.' in s:
            while(s[-1]=='0'):
                s = s[:-1]
        return s

class Quantity():
    def __init__(self, value, base_unit=None, integer=False):
        self._base_unit = None
        if base_unit is not None:
            self._base_unit = ureg.Quantity(base_unit).u
        self.integer = integer
        
        self.value = ureg.Quantity(value)

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, v):
        self._value = ureg.Quantity(v)
        if self._value.unitless and self._base_unit is not None:
            self._value = ureg.Quantity(self._value.m, self._base_unit)

    @property
    def base_unit(self):
        return self._base_unit
    
    @base_unit.setter
    def base_unit(self, u):
        if u is None:
            self._base_unit = u
        else:
            self._base_unit = ureg.Quantity(u).u
            if self.value.unitless:
                self.value = ureg.Quantity(self.value.m, self._base_unit)

    def _quantity(self, value):
        # if value.
        pass
        
    @staticmethod
    def from_dict(d, base_unit=None):
        if 'value' in d:
            res = Quantity(d['value'])
        else:
            res = 0

        if 'unit' in d and d['unit'] is not None:
            res._value = ureg.Quantity(d['value'], d['unit'])
        if 'show_as' in d and d['show_as'] is not None:
            res._value = res._value.to(d['show_as'])
            res._base_unit = ureg.Quantity(d['unit']).u
        if 'integer' in d:
            res.integer = d['integer']
            
        if base_unit is not None and base_unit!="":
            res._base_unit = base_unit
        return res
    
    def to_dict(self):
        res = {}
        if self._base_unit is None:
            res['value'] = self.value.m
            if self.value.unitless==False:
                res['unit'] = str(self.value.u)
        else:
            res['value'] = self.value.m_as(self._base_unit)
            res['unit'] = str(self.base_unit)
            if self.base_unit!=self.value.u:
                res['show_as'] = str(self.value.u)
        res['integer'] = self.integer

        return res

    @property
    def magnitude(self):
        if self.base_unit is not None:
            return self.value.to(self.base_unit).m
        else:
            return self.value.m

    @property
    def unit(self):
        return self.value.u
        
    def __str__(self):
        s = ""
        if self.integer:
            s += str(int(self.value.m))
        else:
            s += format_float(self.value.m, 3)
        if self.value.unitless==False:
            s += " "+str(self.value.u)
            
        return s

class QuantityRange():
    def __init__(self, min: Quantity=None, max: Quantity=None, base_unit=None, integer=False):
        self._min = min
        self._max = max
        self._base_unit = base_unit
        self._integer = integer
        
    @property
    def min(self):
        return self._min
    
    @min.setter
    def min(self, value):
        self._min = value
        if value is not None:
            self._min.base_unit = self._base_unit

    @property
    def max(self):
        return self._max
    
    @max.setter
    def max(self, value):
        self._max = value
        if value is not None:
            self._max.base_unit = self._base_unit

    @property
    def base_unit(self):
        return self._base_unit
    
    @base_unit.setter
    def base_unit(self, value):
        if value is None:
            self._base_unit = value
        else:
            self._base_unit = ureg.Quantity(value).u

        if self._min is not None:
            self._min.base_unit = value
        if self._max is not None:
            self._max.base_unit = value

    @property
    def integer(self):
        return self._integer
    
    @integer.setter
    def integer(self, v):
        if self._min is not None:
            self._min.integer = self.integer
        if self._max is not None:
            self._min.integer = self.integer
        
    @staticmethod
    def from_dict(d, base_unit=None):
        res = QuantityRange()
        
        if 'min' in d:
            res.min = Quantity.from_dict(d['min'])
        if 'max' in d:
            res.max = Quantity.from_dict(d['max'])
        if 'base_unit' in d:
            res.base_unit = ureg.Quantity(d['base_unit']).u
        return res
    
    def to_dict(self):
        res = {}
        if self._min is not None:
            res['min'] = self.min.to_dict()
        if self._max is not None:
            res['max'] = self.max.to_dict()
        if self._base_unit is not None:
            res['base_unit'] = str(self.base_unit)
        return res
    
    def __str__(self):
        res = ""
        if self.min is None:
            res = '*'
        else:
            res = str(self.min)
        res += " - "
        if self.max is None:
            res += "*"
        else:
            res += str(self.max)
        return res

class UnitList():
    def __init__(self, values=[]):
        self.values = values
    
    def __len__(self):
        return len(self.values)

