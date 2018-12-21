import hashlib

def md5(value):
    if not issubclass(type(value), bytes):
        return hashlib.md5(bytes(value, 'utf-8'))
    else:
        return hashlib.md5(value)
    