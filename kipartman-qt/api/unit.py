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
ureg = UnitRegistry() #autoconvert_offset_to_baseunit=True)
# ureg.default_format = "P~"
ureg.default_format = "~#P"
# Q_ = ureg.Quantity

# add dimensionless units
ureg.define('percent = 0.01*count = %')
ureg.define('ppm = count*10**-6')

pint.set_application_registry(ureg)


class Quantity():
    def __init__(self, value, base_unit=None, integer=False):
        
        self._base_unit = None
        if base_unit is not None:
            try:
                self._base_unit = ureg.Quantity(base_unit).u
            except pint.OffsetUnitCalculusError as e:
                self._base_unit = ureg.parse_units(base_unit)
 
        self.integer = integer
 
        self.offset = False # indicate if unit
        try:
            self.value = ureg.Quantity(value)
        except pint.OffsetUnitCalculusError as e:
            # we can't initialize an instance of an offset quantity from a string,
            # we cut it in half and do the init with the two chuncks
            if isinstance(value, str):
                v, u = self._cut_value(value)
                if v is None:
                    self.value = ureg.Quantity(value)
                else:
                    self.value = ureg.Quantity(float(v), u)
            else:
                raise e

    @property
    def value(self):
        """ return the value to format ureg.Quantity """
        return self._value
    
    @value.setter
    def value(self, v):
        self._value = ureg.Quantity(v)
        if self._value.unitless and self._base_unit is not None:
            self._value = ureg.Quantity(self._value.m, self._base_unit)

    @property
    def base_unit(self):
        """ return a string with base unit or None """
        if self._base_unit is None:
            return self._base_unit
        return str(self._base_unit).replace("Δ", "")
    
    @base_unit.setter
    def base_unit(self, u):
        if u is None:
            self._base_unit = u
        else:
            self._base_unit = ureg.Quantity(u).u
            if self.value.unitless:
                self.value = ureg.Quantity(self.value.m, self._base_unit)

    @property
    def magnitude(self):
        """ return the magnitude converted to base unit """
        if self.base_unit is not None:
            if self.value.dimensionless:
                return self.value.m
            else:
                return self.value.to(self.base_unit).m
        else:
            return self.value.m

    @property
    def unit(self):
        """ return unit expressed in string """
        return str(self.value.u).replace("Δ", "")

    def to(self, unit):
        return Quantity(self.value.to(unit), base_unit=self.base_unit, integer=self.integer)

    @staticmethod
    def from_dict(d, base_unit=None):
        if 'value' in d:
            res = Quantity(d['value'])
        else:
            res = 0

        if 'unit' in d and d['unit'] is not None:
            res._value = ureg.Quantity(d['value'], d['unit'])
        if 'show_as' in d and d['show_as'] is not None:
            if res._value.dimensionless:
                res._value = ureg.Quantity(d['value'], d['show_as'])
            else:
                res._value = res._value.to(d['show_as'])
            try:
                res._base_unit = ureg.Quantity(d['unit']).u
            except pint.OffsetUnitCalculusError as e:
                res._base_unit = ureg.parse_units(d['unit'])
        if 'integer' in d:
            res.integer = d['integer']
            
        if base_unit is not None and base_unit!="":
            res._base_unit = base_unit
        return res
    
    def to_dict(self):
        res = {}
        if self._base_unit is None:
            res['value'] = self.magnitude
            if self.value.unitless==False:
                res['unit'] = str(self.unit)
        else:
            res['value'] = self.magnitude
            res['unit'] = self.base_unit
            if self.base_unit!=self.unit:
                res['show_as'] = self.unit
        res['integer'] = self.integer

        return res

    def _cut_value(self, value):
        value = value.strip()
        n = len(value)
        v = None
        u = None
        while n>0:
            s = value[0:n]
            try:
                check = float(s)
                v = s
                u = value[n-1:]
                return v, u
            except:
                pass
            n -= 1
        return None, None

    def format(self, digits=3, trailing_zeros=True):
        def format_float(v):
            epsilon = 1e-5  
        
            if v<0:
                sign = -1
            else:
                sign = 1
            v = abs(v)
            
            dec = int(v+0.5)
            frac = abs(v-dec) 
            if frac<epsilon:
                return str(dec*sign)
            else:
                s = str(int(round(v, 0)))
                if digits is not None:
                    if len(s)<digits:
                        s = f"{{:.{digits-len(s)}f}}".format(v*sign)
                if trailing_zeros==False and '.' in s:
                    while(s[-1]=='0'):
                        s = s[:-1]
                return s
        
        s = ""
        if self.integer==True:
            s += str(int(self.value.m))
        else:
            s += format_float(self.value.m)
        if self.value.unitless==False:
            s += " "+str(self.value.u)
        return s.replace("Δ", "")

    def __str__(self):
        s = ""
        if self.integer:
            s += str(int(self.value.m))
        else:
            s += str(float(self.value.m))
        if self.value.unitless==False:
            s += " "+str(self.value.u)
        return s.replace("Δ", "")

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

    def format(self, digits=3, trailing_zeros=True):
        res = ""
        if self.min is None:
            res = '*'
        else:
            res = self.min.format(digits, trailing_zeros)
        res += " - "
        if self.max is None:
            res += "*"
        else:
            res += self.max.format(digits, trailing_zeros)
        return res

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

