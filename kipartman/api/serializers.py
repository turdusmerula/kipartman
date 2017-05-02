
class Field(object):
    def __init__(self):
        None

class BaseDeserializer(Field):
    def __init__(self, data):
        super(BaseDeserializer, self).__init__()

class CollectionDeserializer(BaseDeserializer):
    def __init__(self):
        super(CollectionDeserializer, self).__init__()

class PartCategoryDeserializer(BaseDeserializer):
    None