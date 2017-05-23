from rest_client import exceptions
from rfc3987 import parse
import requests
from rest_client import registry

class Field(object):

    def __init__(self, read_only=False):
        self._read_only = read_only
        
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value

    def serialize(self):
        return self.get_value()

    def is_read_only(self):
        return self._read_only

class IntegerField(Field):
    def __init__(self, default=0, **kwargs):
        self.set_value(default)
        super(IntegerField, self).__init__(**kwargs)

    def set_value(self, value):
        try:
            self.value = int(value)
        except Exception:
            raise exceptions.FieldError('%s: invalid integer' % (value))


class BooleanField(Field):
    def __init__(self, default=False, **kwargs):
        self.set_value(default)
        super(BooleanField, self).__init__(**kwargs)

    def set_value(self, value):
        try:
            self.value = bool(value)
        except Exception:
            raise exceptions.FieldError('%s: invalid boolean' % (value))


class TextField(Field):
    def __init__(self, default='', **kwargs):
        self.set_value(default)
        super(TextField, self).__init__(**kwargs)


class ListField(Field):
    def __init__(self, model=None, default=[], **kwargs):
        self.set_value(default)
        self.model = model
        super(ListField, self).__init__(**kwargs)


class HyperlinkField(Field):
    def __init__(self, model, **kwargs):
        #TODO: check that model exists
        self.model = model
        self.url = None
        self.loaded = False
        self.value = None
        super(HyperlinkField, self).__init__(**kwargs)
        
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
