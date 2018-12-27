

def format_unit_prefix(v, unit=''):
    epsilon = 1e-5  
    dprefix = ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'] 
    fprefix = ['', 'm', 'µ', 'n', 'p', 'f', 'a', 'y'] 

    res = ''
    
    vin = v
    sign = 1
    if v<0:
        sign = -1 
        v = -v

    if unit=='':
        dec = int(v)
        frac = v-dec 
        if frac<epsilon:
            return str(dec) ;
    if v>=1:
        p = False
        for si in dprefix:
            if v<1000:
                res = "{0:.2f}".format(v*sign)+' '+si
                p = True ;
                break ;
            else:
                v = v/1000. ;
        if p==False:
            res = str(vin)+' '
        res = res+unit
    else:
        p = False 
        for si in fprefix:
            if v>0.9:
                res = "{0:.2f}".format(v*sign)+' '+si
                p = True 
                break
            else:
                v = v*1000.
        if p==False:
            res = str(vin)+' '
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