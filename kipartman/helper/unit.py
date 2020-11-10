from curses.ascii import isalnum
import re
import api.data.unit

class UnitException(Exception):
    def __init__(self, error):
        super(UnitException, self).__init__(error)

symbol_power={
    "Y": 1E24,
    "Z": 1E21,
    "E": 1E18,
    "P": 1E15,
    "T": 1E12,
    "G": 1E9,
    "M": 1E6,
    "k": 1E3,
    "h": 1E2,
    "da": 1E1,
    "": 1E0,
    "d": 1E-1,
    "c": 1E-2,
    "m": 1E-3,
    "µ": 1E-6,
    "n": 1E-9,
    "p": 1E-12,
    "f": 1E-15,
    "a": 1E-18,
    "y": 1E-24,
    "Ki": 1024,
    "Mi": 1024^2,
    "Gi": 1024^3,
    "Ti": 1024^4,
    "Pi": 1024^5,
    "Ei": 1024^6,
    "Zi": 1024^7,
    "Yi": 1024^8,
    }

def cut_unit_value(value):
    # remove whitespaces
    value = re.sub(r"\s+", '', value)
    
    
    # extract number part from value
    num = ""
    s = ""
    for c in value:
        s += c
        try:
            v = float(s)
            num = s
        except:
            pass
    
    if num=="":
        raise UnitException(f"Invalid number {value}")
    
    value = re.sub(f'^{num}', '', value)

    # extract unit part
    units = api.data.unit.find()
    
    unit = value
    prefix = ""
    
    error = False
    if unit!="":
        found_unit = False
        while found_unit==False and error==False:
            for _unit in units:
                if unit==_unit.symbol:
                    found_unit = True
                    break
            if found_unit==False:
                prefix += unit[0]
                if len(unit)==1:
                    error = True
                else:
                    unit = unit[1:]
            else:
                if prefix!="" and prefix not in symbol_power:
                    prefix += value[0]
                    if len(unit)==1:
                        error = True
                    else:
                        unit = unit[1:]

    if error==True:
        raise UnitException(f"Unknown unit {value}")

    return (num, prefix, unit)

def expand_prefix(value, prefix):
    if prefix not in symbol_power:
        raise UnitException(f"Invalid prefix {prefix}")
    return value*symbol_power[prefix]

def format_float(v, digits=3):
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
        if len(s)<digits:
            format = f"{{:.{digits-len(s)}f}}"
            return format.format(v*sign)
        else:
            return s
   
def format_unit_prefix(v, unit='', prefix=None):
    """
    Format a number with unit
    If prefix is None the prefix is chosen automaticaly depending on v
    """
    dprefix = ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'] 
    fprefix = ['', 'm', 'µ', 'n', 'p', 'f', 'a', 'y'] 

    res = ''
    
    if prefix is None:
        vin = v
        sign = 1
        if v<0:
            sign = -1 
            v = -v
    
        if v>=1:
            p = False
            for si in dprefix:
                if v<1000:
                    res = format_float(v*sign)+si
                    p = True ;
                    break ;
                else:
                    v = v/1000. ;
            if p==False:
                res = str(vin)
        else:
            p = False 
            for si in fprefix:
                if v>0.9:
                    res = format_float(v*sign)+si
                    p = True 
                    break
                else:
                    v = v*1000.
            if p==False:
                res = str(vin)
    else:
        if prefix in symbol_power:
            v = v/symbol_power[prefix]
        else:
            raise UnitException(f"Unknown unit prefix {prefix}")
        res = format_float(v)+prefix

    res = res+unit

    return res

def unit_prefix_value(v, prefix=''):
    symbols = ['y',  'a',   'f',    'p',   'n',  'µ',  'm', 'c',  'd',   '', 'da', 'h', 'k', 'M', 'G', 'T',  'P',  'E', 'Z',  'Y'] 
    powers =  [1E-24, 1E-18, 1E-15, 1E-12, 1E-9, 1E-6, 1E-3, 1E-2, 1E-1, 1E0, 1E1, 1E2, 1E3, 1E6, 1E9, 1E12, 1E15, 1E18, 1E21, 1E24]
    
    i = 0
    for symbol in symbols:
        if symbol==prefix:
            return v*powers[i]
        i = i+1
    return v

