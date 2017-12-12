import Canvas 

class KicadObject(object):
    mapping = {}
    
    def __init__(self, header):
        self.header = header
        self.attributes = []
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

    def AddAttribute(self, attr):
        self.attributes.append(attr)

    def Attribute(self, index):
        if index<len(self.attributes):
            return self.attributes[index]
        return ''

    def Render(self, canvas, obj=None):
        for node in self.nodes:
            node.Render(canvas, obj)
