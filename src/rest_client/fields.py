from rest_client import exceptions
from rfc3987 import parse
import requests
from rest_client import registry
from urllib2 import urlopen
import os

class Field(object):

    def __init__(self, read_only=False, null=False, as_file=False):
        self._read_only = read_only
        self.null = null
        self.as_file = as_file
        
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        if value is None and self.null==False:
            raise exceptions.FieldError('None encountered')
        self.value = value

    def serialize(self):
        return self.get_value()

    def file(self):
        return None

    def is_read_only(self):
        return self._read_only

class IntegerField(Field):
    def __init__(self, default=0, **kwargs):
        super(IntegerField, self).__init__(**kwargs)
        self.set_value(default)

    def set_value(self, value):
        try:
            self.value = int(value)
        except Exception:
            raise exceptions.FieldError('%s: invalid integer' % (value))


class ModelField(Field):
    def __init__(self, model, default=None, **kwargs):
        super(ModelField, self).__init__(**kwargs)
        self.model = model
        self.set_value(default)

    def set_value(self, value):
        if value and isinstance(value, self.model)==False:
            raise exceptions.FieldError('%s: invalid, %s requested ' % (type(value), self.model))
        super(ModelField, self).set_value(value)

    def serialize(self):
        return self.id

class BooleanField(Field):
    def __init__(self, default=False, **kwargs):
        super(BooleanField, self).__init__(**kwargs)
        self.set_value(default)

    def set_value(self, value):
        try:
            self.value = bool(value)
        except Exception:
            raise exceptions.FieldError('%s: invalid boolean' % (value))


class FloatField(Field):
    def __init__(self, default=False, **kwargs):
        super(FloatField, self).__init__(**kwargs)
        self.set_value(default)

    def set_value(self, value):
        try:
            if value is None:
                super(FloatField, self).set_value(value)
            else:
                self.value = float(value)
        except Exception:
            raise exceptions.FieldError('%s: invalid float' % (value))


class TextField(Field):
    def __init__(self, default='', **kwargs):
        super(TextField, self).__init__(**kwargs)
        self.set_value(default)


class IndexListField(Field):
    def __init__(self, model=None, default=[], **kwargs):
        super(IndexListField, self).__init__(**kwargs)
        self.set_value(default)
        self.model = model
    
    def remove(self, item):
        self.get_value(self).remove(item)


class ListField(Field):
    def __init__(self, model=None, default=[], **kwargs):
        super(ListField, self).__init__(**kwargs)
        self.set_value(default)
        self.model = model
    
    def remove(self, item):
        self.get_value(self).remove(item)

    def set_value(self, value):
        try:
            self.value = []
            for v in value:
                self.value.append(registry.registered_model(self.model)(**v))
        except Exception as e:
            raise exceptions.FieldError('%s: invalid list for model (%s)' % (value, format(e)))

class HyperlinkField(Field):
    def __init__(self, model, **kwargs):
        super(HyperlinkField, self).__init__(**kwargs)
        #TODO: check that model exists
        self.model = model
        self.url = None
        self.loaded = False
        self.value = None
        
    def get_value(self):
        if self.loaded==True:
            return self.value
        else:
            if self.url==None:
                return None
            else:
                #read from server
                try:
                    content = requests.get(self.url)
                    content.raise_for_status()
                except requests.exceptions.RequestException as e:
                    raise exceptions.FieldError("HyperlinkField: %s" % (e))
                # read json content and create a new model object from it
                self.value = registry.registered_model(self.model)(**content.json())
                self.loaded = True
                return self.value

    def set_value(self, value):
        if isinstance(value, basestring): 
            # assume hyperlink is loaded with an URL
            try:
                parse(value)
            except ValueError:
                raise exceptions.FieldError("HyperlinkField: '%s' is not a valid url")
            self.url = value
            self.loaded = False
            self.value = None
        else:
        #issubclass(type(value), vars()[self.model]):
            self.loaded = True
            self.value = value
            if not value is None: 
                self.url = value.path
#        else:
#            raise exceptions.FieldError("HyperlinkField: value is not an URL nor a %s" % (self.model))

    def serialize(self):
        if self.url is None:
            return ""
        else:
            return self.url


class FileField(Field):
    def __init__(self, **kwargs):
        super(FileField, self).__init__(as_file=True, **kwargs)
        self.set_value(None)

    def file(self):
        try:
            urlopen(self.get_value())
            # object contains an URL, return None 
            return None
        except ValueError:  # invalid URL
            # Object contains a file, open it
            return (os.path.basename(self.get_value()), open(self.get_value(), 'rb'), 'application/octet-stream')
        except:
            return None
        
class ImageField(FileField):
    pass
