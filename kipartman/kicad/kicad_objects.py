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

class KicadPcb(KicadObject):
    def __init__(self):
        super(KicadPcb, self).__init__('kicad_pcb')
        KicadObject._register(self.header, KicadPcb)
        
class KicadModule(KicadObject):
    def __init__(self):
        super(KicadModule, self).__init__('module')
        KicadObject._register(self.header, KicadModule)

    def footprint(self):
        return self.Attribute(0)

class KicadFPLine(KicadObject):
    def __init__(self):
        super(KicadFPLine, self).__init__('fp_line')
        KicadObject._register(self.header, KicadFPLine)

    def Render(self, canvas, obj):
        line = Canvas.Line()
        super(KicadFPLine, self).Render(canvas, line)
        canvas.Draw(line)
        
class KicadPad(KicadObject):
    def __init__(self):
        super(KicadPad, self).__init__('pad')
        KicadObject._register(self.header, KicadPad)

    def Render(self, canvas, obj):
        pad = Canvas.Pad()
        if self.Attribute(1)=='smd':
            if self.Attribute(2)=='rect':
                pad.smd = True
                pad.rect = True
        super(KicadPad, self).Render(canvas, pad)
        canvas.Draw(pad)

class KicadFPText(KicadObject):
    def __init__(self):
        super(KicadFPText, self).__init__('fp_text')
        KicadObject._register(self.header, KicadFPText)

    def Render(self, canvas, obj):
        text = Canvas.Text()
        super(KicadFPText, self).Render(canvas, text)
        canvas.Draw(text)

class KicadAt(KicadObject):
    def __init__(self):
        super(KicadAt, self).__init__('at')
        KicadObject._register(self.header, KicadAt)

    def Render(self, canvas, obj):
        obj.at = Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
        super(KicadAt, self).Render(canvas, obj)

class KicadStart(KicadObject):
    def __init__(self):
        super(KicadStart, self).__init__('start')
        KicadObject._register(self.header, KicadStart)

    def Render(self, canvas, obj):
        obj.start = Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
        super(KicadStart, self).Render(canvas, obj)
        
class KicadEnd(KicadObject):
    def __init__(self):
        super(KicadEnd, self).__init__('end')
        KicadObject._register(self.header, KicadEnd)

    def Render(self, canvas, obj):
        obj.end = Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
        super(KicadEnd, self).Render(canvas, obj)

class KicadLayer(KicadObject):
    def __init__(self):
        super(KicadLayer, self).__init__('layer')
        KicadObject._register(self.header, KicadLayer)

    def Render(self, canvas, obj):
        canvas.SelectLayer(self.Attribute(0))
        super(KicadLayer, self).Render(canvas, obj)

class KicadLayers(KicadObject):
    def __init__(self):
        super(KicadLayers, self).__init__('layers')
        KicadObject._register(self.header, KicadLayers)

    def Render(self, canvas, obj):
        print self.attributes
        canvas.SelectLayers(self.attributes)
        super(KicadLayers, self).Render(canvas, obj)

class KicadWidth(KicadObject):
    def __init__(self):
        super(KicadWidth, self).__init__('width')
        KicadObject._register(self.header, KicadWidth)

    def Render(self, canvas, obj):
        obj.width = float(self.Attribute(0))
        super(KicadWidth, self).Render(canvas, obj)

class KicadSize(KicadObject):
    def __init__(self):
        super(KicadSize, self).__init__('size')
        KicadObject._register(self.header, KicadSize)

    def Render(self, canvas, obj):
        obj.size = Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
        super(KicadSize, self).Render(canvas, obj)

class KicadDrill(KicadObject):
    def __init__(self):
        super(KicadDrill, self).__init__('drill')
        KicadObject._register(self.header, KicadDrill)

    def Render(self, canvas, obj):
        obj.drill = float(self.Attribute(0))
        super(KicadDrill, self).Render(canvas, obj)

"""
Instanciate at least one time to force objects registration
"""
KicadPcb()
KicadModule()
KicadFPLine()
KicadFPText()
KicadPad()
KicadAt()
KicadStart()
KicadEnd()
KicadLayer()
KicadLayers()
KicadWidth()
KicadSize()
KicadDrill()
