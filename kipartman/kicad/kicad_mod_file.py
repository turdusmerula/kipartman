import wx
import os
from kicad_object import KicadObject
import Canvas

def tab(level):
    res = ''
    for i in range(level):
        res = res+'  '
    return res

class KicadModFile(object):
    def __init__(self):
        self.filename = None
        self.onChanged = None
        self.parent = KicadObject('')

    def LoadFile(self, filename):
        """
        Load file
        """
        if(os.path.isfile(filename)==False):
            self.filename = None
#            wx.MessageBox("Error: %s does not exists" % filename, "File error", wx.OK | wx.ICON_ERROR)
            raise Exception("Error: %s does not exists" % filename)

        self.filename = filename
        self.file = open(filename, 'r')
        self.buff = ''

        self.read_blocks(self.parent) 
        #self.Write(self.parent, 0)
                    
        if self.onChanged:
            self.onChanged()

    def Render(self, filename, width=256, height=256):
        canvas = Canvas.FootprintCanvas()
        surface = canvas.Render(self.parent, width, height)
        surface.write_to_png (filename)
        
    def Write(self, obj, level=0):
        line = "%s(%s"%(tab(level), obj.header)
        for attr in obj.attributes:
            line = line+" "+attr
        
        if len(obj.nodes)>0:
            print(line)
            for node in obj.nodes:
                self.Write(node, level+1)
            print("%s)"%tab(level))
        else:
            line = line+")"
            print(line)
    
    def read_blocks(self, parent):
        block_header = self._read_block_header()
        if block_header=='':
            return None
        obj = KicadObject.Instance(block_header)        
        parent.AddNode(obj)

        attr = self._read_field()
        while attr!=None:
            obj.AddAttribute(attr)
            attr = self._read_field()
        
        node = self.read_blocks(obj)
        while node:
            node = self.read_blocks(obj)
        
        self._skip_spaces()
        c = self.observe(1)
        if c==')':
            self.read(1)

        return obj

    def _skip_spaces(self):
        """
        Jump to the next non space character
        """
        # read spaces
        c = self.observe(1)
        while c.isspace():
            self.read(1)
            c = self.observe(1)
        
    def read(self, size):
        res = ''
        if len(self.buff)>size:
            res = self.buff[:size]
            self.buff = self.buff[size:]
        else:
            res = self.buff+self.file.read(size-len(self.buff))
            self.buff = ''
        return res
    
    def observe(self, size):
        if len(self.buff)>size:
            return self.buff[:size]
        else:
            self.buff = self.buff+self.file.read(size-len(self.buff))
        return self.buff
         
    def _read_block_header(self):
        """
        Read next block header
        """
        # read spaces
        self._skip_spaces()

        c = self.observe(1)
        if c=='(':
            self.read(1)
            return self._read_field()
        return ""
    
    def _read_field(self):
        field = ''
        
        # read spaces
        self._skip_spaces()
        c = self.observe(1)
        
        if c=='(' or c==')':
            return None
        
        if c=='"':
            self.read(1)
            c = self.observe(1)
            while c!='"':
                c = self.observe(1)
                if c!='"':
                    field = field+c
                    c = self.read(1)
            self.read(1)
        else:
            c = self.observe(1)
            while c!='' and c.isspace()==False and c!='(' and c!=')':
                field = field+c
                self.read(1)
                c = self.observe(1)

        return field


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
            pad.smd = True
        elif self.Attribute(1)=='np_thru_hole':
            pad.thru_hole = True
        elif self.Attribute(1)=='thru_hole':
            pad.thru_hole = True
            
        if self.Attribute(2)=='rect':
            pad.rect = True
        elif self.Attribute(2)=='oval':
            pad.oval = True
        elif self.Attribute(2)=='circle':
            pad.oval = True
            
        super(KicadPad, self).Render(canvas, pad)
        canvas.Draw(pad)

class KicadFPText(KicadObject):
    def __init__(self):
        super(KicadFPText, self).__init__('fp_text')
        KicadObject._register(self.header, KicadFPText)

    def Render(self, canvas, obj):
        text = Canvas.Text(self.Attribute(1))
        super(KicadFPText, self).Render(canvas, text)
        if self.Attribute(0)=='value':
            canvas.Draw(text)

class KicadFPCircle(KicadObject):
    def __init__(self):
        super(KicadFPCircle, self).__init__('fp_circle')
        KicadObject._register(self.header, KicadFPCircle)

    def Render(self, canvas, obj):
        circle = Canvas.Circle()
        super(KicadFPCircle, self).Render(canvas, circle)
        canvas.Draw(circle)

class KicadAt(KicadObject):
    def __init__(self):
        super(KicadAt, self).__init__('at')
        KicadObject._register(self.header, KicadAt)

    def Render(self, canvas, obj):
        if obj:
            if self.Attribute(0)=='':
                obj.at = Canvas.Position()
            else:
                obj.at = Canvas.Position(float(self.Attribute(0)), float(self.Attribute(1)))
                if self.Attribute(2)!='':
                    obj.at.angle = float(self.Attribute(2))
        super(KicadAt, self).Render(canvas, obj)

class KicadStart(KicadObject):
    def __init__(self):
        super(KicadStart, self).__init__('start')
        KicadObject._register(self.header, KicadStart)

    def Render(self, canvas, obj):
        if obj:
            obj.start = Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
        super(KicadStart, self).Render(canvas, obj)
        
class KicadEnd(KicadObject):
    def __init__(self):
        super(KicadEnd, self).__init__('end')
        KicadObject._register(self.header, KicadEnd)

    def Render(self, canvas, obj):
        if obj:
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
        canvas.SelectLayers(self.attributes)
        super(KicadLayers, self).Render(canvas, obj)

class KicadWidth(KicadObject):
    def __init__(self):
        super(KicadWidth, self).__init__('width')
        KicadObject._register(self.header, KicadWidth)

    def Render(self, canvas, obj):
        if obj:
            obj.width = float(self.Attribute(0))
        super(KicadWidth, self).Render(canvas, obj)

class KicadSize(KicadObject):
    def __init__(self):
        super(KicadSize, self).__init__('size')
        KicadObject._register(self.header, KicadSize)

    def Render(self, canvas, obj):
        if obj:
            obj.size = Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
        super(KicadSize, self).Render(canvas, obj)

class KicadDrill(KicadObject):
    def __init__(self):
        super(KicadDrill, self).__init__('drill')
        KicadObject._register(self.header, KicadDrill)

    def Render(self, canvas, obj):
        if obj:
            obj.drill = float(self.Attribute(0))
        super(KicadDrill, self).Render(canvas, obj)

class KicadFont(KicadObject):
    def __init__(self):
        super(KicadFont, self).__init__('font')
        KicadObject._register(self.header, KicadFont)

    def Render(self, canvas, obj):
        font = Canvas.Font()
        canvas.SetFont(font)
        super(KicadFont, self).Render(canvas, font)

class KicadThickness(KicadObject):
    def __init__(self):
        super(KicadThickness, self).__init__('thickness')
        KicadObject._register(self.header, KicadThickness)

    def Render(self, canvas, obj):
        if obj:
            obj.thickness = float(self.Attribute(0))
        super(KicadThickness, self).Render(canvas, obj)

class KicadCenter(KicadObject):
    def __init__(self):
        super(KicadCenter, self).__init__('center')
        KicadObject._register(self.header, KicadCenter)

    def Render(self, canvas, obj):
        if obj:
            obj.size = Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
        super(KicadCenter, self).Render(canvas, obj)

"""
Instanciate at least one time to force objects registration
"""
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
KicadFont()
KicadThickness()
KicadFPCircle()
KicadCenter()
