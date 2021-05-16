from dataclasses import asdict
from datetime import datetime

def from_redis(value, type=str):
    value = value.decode()
    if type is str:
        return value
    elif value=='':
        return None

    if type is datetime:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    elif type is int:
        return int(value)
    elif type is float:
        return float(value)
    elif type is bool:
        return int(value)>0
    return value

def from_dict(klass, dikt):
    fieldtypes = klass.__annotations__
#     dikt = { key.decode(): val.decode() for key, val in dikt.items() }
    res = {}
    for f, value in dikt.items():
        f = f.decode()
        res[f] = from_redis(value, fieldtypes[f])
    return klass(**res)
#     try:
#             
# #         return klass(**{f: fieldtypes[f](from_dict(fieldtypes[f], dikt[f])) for f in dikt})
#     except AttributeError:
#         if isinstance(dikt, (tuple, list)):
#             return [from_dict(klass.__args__[0], f) for f in dikt]
#         return dikt

def to_redis(value):
    if value is None:
        return ''
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, bool):
        return int(value)
    return value

def to_dict(obj):
    return { key: to_redis(val) for key, val in asdict(obj).items() }
