import wx
import os
from kicad_object import KicadObject
import Canvas
import re 
import math
import tempfile

def tab(level):
    res = ''
    for i in range(level):
        res = res+'  '
    return res

class EOL(object):
    pass

class EOF(object):
    pass

class KicadLibFile(object):
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
        self.line = ''
        self.buff = ''

        self.read_lines(self.parent) 
        #self.Write(self.parent, 0)
                    
        if self.onChanged:
            self.onChanged()
   
    def Load(self, content):
        """
        Load from string
        """
        if content is None:
            content = ''

        self.file = tempfile.NamedTemporaryFile()
        self.file.write(content)
        self.file.seek(0)

        self.filename = self.file.name
        self.line = ''
        self.buff = ''

        self.read_lines(self.parent) 
        #self.Write(self.parent, 0)
                    
        if self.onChanged:
            self.onChanged()
        
    def Render(self, filename, width=256, height=256):
        canvas = Canvas.LibraryCanvas()
        surface = canvas.Render(self.parent, width, height)
        surface.write_to_png (filename)
        
    def Write(self, obj, level=0):
        line = "%s%s"%(tab(level), obj.header)
        for attr in obj.attributes:
            line = line+" "+attr
        
        print(line, type(obj))
        if len(obj.nodes)>0:
            for node in obj.nodes:
                self.Write(node, level+1)

    def read_lines(self, parent):
        while self.next_line()!=EOF:
            # skip comment lines
            self._skip_spaces()
            c = self.observe(1)
            if c=='#':
                continue
            
            header = self._read_field()
            
            if header is None:
                continue
        
            obj = KicadLibObject.Instance(header)        
            parent.AddNode(obj)

            attr = self._read_field()
            while attr!=EOL:
                obj.AddAttribute(attr)
                attr = self._read_field()
         
            if re.compile("END.*").match(header):
                return obj
        
            if obj.category:
                self.read_lines(obj)

    def next_line(self):
        self.buff = self.file.readline()
        if self.buff=='':
            return EOF
        return self.buff
        
    def read(self, size):
        res = ''
        if len(self.buff)>size:
            res = self.buff[:size]
            self.buff = self.buff[size:]
        else:
            res = self.buff
            self.buff = ''
        return res

    def observe(self, size):
        if len(self.buff)>size:
            return self.buff[:size]
        return self.buff

    def _skip_spaces(self):
        """
        Jump to the next non space character
        """
        # read spaces
        c = self.observe(1)
        while c.isspace():
            self.read(1)
            c = self.observe(1)
    
    def _read_field(self):
        field = ''
        
        # read spaces
        self._skip_spaces()
        c = self.observe(1)

        if c=='':
            return EOL        
        elif c=='"':
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
            while c!='' and c.isspace()==False:
                field = field+c
                self.read(1)
                c = self.observe(1)

        return field

class KicadLibObject(KicadObject):
    def __init__(self, header, category=False):
        super(KicadLibObject, self).__init__(header)
        self.category = category

    @staticmethod
    def Instance(header):
        """
        Create an instance of object type if type registered, or KicadObject if not
        """
        for key in KicadObject.mapping:
            if re.compile(key).match(header):
                obj = KicadObject.mapping[key]()
                obj.header = header
                return obj
        return KicadLibObject(header)


class KicadDEF(KicadLibObject):
    def __init__(self):
        super(KicadDEF, self).__init__('DEF', True)
        KicadObject._register(self.header, KicadDEF)

class KicadF(KicadLibObject):
    def __init__(self):
        super(KicadF, self).__init__('^F[0-9]*$')
        KicadObject._register(self.header, KicadF)

    def Render(self, canvas, obj):
        if len(self.attributes)<5:
            return 

        font = Canvas.Font(Canvas.Point(float(self.Attribute(3)), float(self.Attribute(3))), canvas.to_view_width(2))
        text = Canvas.Text(self.Attribute(0))
        if self.Attribute(4)=='V':
            angle = 3*math.pi/2
        else:
            angle = 0
        text.anchor_x = 'center'
        text.anchor_y = 'center'
        text.at = Canvas.Position(float(self.Attribute(1)), -float(self.Attribute(2)), angle)
        canvas.SelectLayer("Label")
        canvas.SetFont(font)
        canvas.Draw(text)

class KicadDRAW(KicadLibObject):
    def __init__(self):
        super(KicadDRAW, self).__init__('DRAW', True)
        KicadObject._register(self.header, KicadDRAW)

class KicadC(KicadLibObject):
    def __init__(self):
        super(KicadC, self).__init__('C')
        KicadObject._register(self.header, KicadC)

    def Render(self, canvas, obj):
        if len(self.attributes)<3:
            return 

        canvas.SelectLayer("Drawing")
        start = Canvas.Point(float(self.Attribute(0)), -float(self.Attribute(1)))
        end = Canvas.Point(float(self.Attribute(0))+float(self.Attribute(2)), -float(self.Attribute(1)))
        if self.Attribute(len(self.attributes)-1)=='F':
            circle = Canvas.Circle(start, end, canvas.to_view_width(2), True)
        else:
            circle = Canvas.Circle(start, end, canvas.to_view_width(2), False)
        canvas.Draw(circle)

class KicadA(KicadLibObject):
    def __init__(self):
        super(KicadA, self).__init__('A')
        KicadObject._register(self.header, KicadA)


class KicadT(KicadLibObject):
    def __init__(self):
        super(KicadT, self).__init__('T')
        KicadObject._register(self.header, KicadT)

    def Render(self, canvas, obj):
        if len(self.attributes)<4:
            return
        font = Canvas.Font(Canvas.Point(float(self.Attribute(3)), float(self.Attribute(3))), canvas.to_view_width(2))
        text = Canvas.Text(self.Attribute(7))
        if int(self.Attribute(0))>0:
            angle = 3*math.pi/2
        else:
            angle = 0
        text.anchor_x = 'center'
        text.anchor_y = 'center'
        text.at = Canvas.Position(float(self.Attribute(1)), -float(self.Attribute(2)), angle)
        canvas.SelectLayer("Label")
        canvas.SetFont(font)
        canvas.Draw(text)

class KicadP(KicadLibObject):
    def __init__(self):
        super(KicadP, self).__init__('P')
        KicadObject._register(self.header, KicadP)

    def Render(self, canvas, obj):
        if len(self.attributes)<4:
            return 

        num = int(self.Attribute(0))
        points = []
        for p in range(0, num*2, 2):
            points.append(Canvas.Point(float(self.Attribute(4+p)), -float(self.Attribute(5+p))))

        canvas.SelectLayer("Drawing")
        if float(self.Attribute(3))>0:
            width = float(self.Attribute(3))
        else:
            width = canvas.to_view_width(2)
        if self.Attribute(len(self.attributes)-1)=='F':
            polyline = Canvas.PolyLine(points, width, True)
        else:
            polyline = Canvas.PolyLine(points, width, False)
        canvas.Draw(polyline)

class KicadX(KicadLibObject):
    def __init__(self):
        super(KicadX, self).__init__('X')
        KicadObject._register(self.header, KicadX)

    def Render(self, canvas, obj):
        if len(self.attributes)<6:
            return 

        canvas.SelectLayer("Drawing")
        width = canvas.to_view_width(2)
        length = float(self.Attribute(4))
        if self.Attribute(5)=='U':
            angle = 3*math.pi/2
            text_angle = angle
            text_dx = -canvas.to_view_width(10)
            text_dy = -length/2
        elif self.Attribute(5)=='D':
            angle = math.pi/2
            text_angle = 3*math.pi/2
            text_dx = -canvas.to_view_width(10)
            text_dy = length/2
        elif self.Attribute(5)=='R':
            angle = 0
            text_angle = 0
            text_dx = length/2
            text_dy = -canvas.to_view_width(10)
        else:
            angle = math.pi
            text_angle = 0
            text_dx = -length/2
            text_dy = -canvas.to_view_width(10)
            
        start = Canvas.Point(float(self.Attribute(2)), -float(self.Attribute(3)))
        end = Canvas.Point(start.x+length*math.cos(angle), start.y+length*math.sin(angle))
        line = Canvas.Line(start, end, width)
        canvas.Draw(line)

        font = Canvas.Font(Canvas.Point(float(self.Attribute(6)), float(self.Attribute(7))), canvas.to_view_width(2))
        text = Canvas.Text(self.Attribute(1))
        text.anchor_x = 'center'
        text.anchor_y = ''
        text.at = Canvas.Position(start.x+text_dx, start.y+text_dy, text_angle)
        canvas.SelectLayer("Label")
        canvas.SetFont(font)
        canvas.Draw(text)

        circle = Canvas.Circle(start, Canvas.Point(start.x+10, start.y), canvas.to_view_width(1), False)
        canvas.Draw(circle)

class KicadS(KicadLibObject):
    def __init__(self):
        super(KicadS, self).__init__('S')
        KicadObject._register(self.header, KicadS)

    def Render(self, canvas, obj):
        if len(self.attributes)<4:
            return
        canvas.SelectLayer("Drawing")
        start = Canvas.Point(float(self.Attribute(0)), -float(self.Attribute(1)))
        end = Canvas.Point(float(self.Attribute(2)), -float(self.Attribute(3)))
        width = canvas.to_view_width(2)
        if self.Attribute(len(self.attributes)-1)=='F':
            rect = Canvas.Rect(start, end, width, True)
        else:
            rect = Canvas.Rect(start, end, width, False)
        canvas.Draw(rect)

"""
Instanciate at least one time to force objects registration
"""
KicadDEF()
KicadF()
KicadDRAW()
KicadP()
KicadC()
KicadX()
KicadS()
KicadA()
KicadT()
