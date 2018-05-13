import Canvas 

def tab(level):
    res = ''
    for i in range(level):
        res = res+'  '
    return res

class EOL(object):
    pass

class EOF(object):
    pass

class KicadObject(object):
    mapping = {}
    
    def __init__(self, header):
        self.header = header
        self.attributes = []
        self.attribute_types = []
        self.nodes = []
    
    @staticmethod
    def _register(header, obj):
        """
        Register a new object type
        """
        if KicadObject.mapping.has_key(header)==False:
            KicadObject.mapping[header] = obj

    @staticmethod
    def Instance(header):
        """
        Create an instance of object type if type registered, or KicadObject if not
        """
        if KicadObject.mapping.has_key(header):
            return  KicadObject.mapping[header]()
        return KicadObject(header)
    
    def AddNode(self, node):
        self.nodes.append(node)
        return node

    def InsertNode(self, index, node):
        self.nodes.insert(index, node)
        return node

    def AddAttribute(self, attr, attr_type=''):
        self.attributes.append(attr)
        self.attribute_types.append(attr_type)
        return attr
    
    def SetAttribute(self, index, attr, attr_type=''):
        while index>=len(self.attributes):
            self.AddAttribute('0', type)
        self.attributes[index] = attr
        self.attribute_types[index] = attr_type
        return attr

    def Attribute(self, index):
        if index<len(self.attributes):
            return self.attributes[index]
        return ''

    def Render(self, canvas, obj=None):
        for node in self.nodes:
            node.Render(canvas, obj)

    