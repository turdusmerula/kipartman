import wx
import os
from kicad_object import KicadObject
import Canvas
import math

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

    def SaveFile(self, filename):
        with open(filename, 'w') as file:
            file.write(self.Write(self.parent))

    def Render(self, filename, width=256, height=256):
        canvas = Canvas.FootprintCanvas()
        canvas.Origin(width/2, height/2)
        canvas.Viewport(width, height)
        surface = canvas.RenderFit(self.parent)
        surface.write_to_png(filename)
        
    def Write(self, obj, level=0):
        line = ""
        if obj.inline==False:
            line = "%s"%(tab(level))
        else:
            line = " "
                    
        if obj.scoped:
            line = line+"(%s"%(obj.header)
        else:
            line = line+"%s"%(obj.header)
        
        for attr in obj.attributes:
            if ' ' in attr:
                line = line+' "'+attr+'"'
            elif attr=='':
                line = line+' ""'
            else:
                line = line+" "+attr
        
        if len(obj.nodes)>0:
            for node in obj.nodes:
                if node.inline==False:
                    line = line+'\n'
                line = line+self.Write(node, level+1)
#            print("%s)"%tab(level))
        if obj.scoped:
            line = line+")"
#            print(line)
        return line
    
    def read_blocks(self, parent, level=0):
        block_header = self._read_block_header()
        if block_header=='':
            return None
        obj = KicadObject.Instance(block_header)        
        parent.AddNode(obj)

#         tab = ''
#         for i in range(0, level):
#             tab = tab+'  '
#         print "{} **".format(tab), block_header

        attr = self._read_field()
        while attr is not None:
#             print "{}   ++".format(tab), attr
            obj.AddAttribute(attr)
            attr = self._read_field()
             
        self._skip_spaces()
        c = self.observe(1)
        while c!=')':
            if c=='(':
                self.read_blocks(obj, level+1)
            else:
                attr = self._read_field()
                if attr is not None:
#                     print "{}   **".format(tab), attr
                    obj.AddNode(KicadObject.Instance(attr))
                        
            self._skip_spaces()
            c = self.observe(1)
        
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

class KicadModuleObject(KicadObject):
    def __init__(self, header, inline=False, scoped=True):
        super(KicadModuleObject, self).__init__(header)
        self.inline = inline
        self.scoped = scoped
        
class KicadModule(KicadModuleObject):
    def __init__(self):
        super(KicadModule, self).__init__('module')
        KicadModuleObject._register(self.header, KicadModule)

    def GetName(self):
        return self.Attribute(0)

    def SetName(self, name):
        self.SetAttribute(0, name, '')
        
    def footprint(self):
        return self.Attribute(0)

class KicadFPLine(KicadModuleObject):
    def __init__(self):
        super(KicadFPLine, self).__init__('fp_line')
        KicadModuleObject._register(self.header, KicadFPLine)

    def Render(self, canvas, obj):
        line = Canvas.Line()
        super(KicadFPLine, self).Render(canvas, line)
        canvas.Draw(line)
        
class KicadPad(KicadModuleObject):
    def __init__(self):
        super(KicadPad, self).__init__('pad')
        KicadModuleObject._register(self.header, KicadPad)

    def GetType(self):
        return self.Attribute(1)

    def SetType(self, pad_type):
        self.SetAttribute(1, pad_type)
        
    def GetShape(self):
        return self.Attribute(2)

    def SetShape(self, shape):
        self.SetAttribute(2, shape)
    
    def GetName(self):
        return self.Attribute(0)

    def SetName(self, name):
        self.SetAttribute(0, name)
        
    def Render(self, canvas, obj):
        pad = Canvas.Pad()
        pad.type = self.GetType()
        pad.shape = self.GetShape()
                        
        super(KicadPad, self).Render(canvas, pad)
        canvas.Draw(pad)

class KicadFPText(KicadModuleObject):
    def __init__(self):
        super(KicadFPText, self).__init__('fp_text')
        KicadModuleObject._register(self.header, KicadFPText)

    def GetKind(self):
        return self.Attribute(0)
    
    def GetValue(self):
        return self.Attribute(1)

    def Render(self, canvas, obj):
        text = Canvas.Text(self.Attribute(1))
        super(KicadFPText, self).Render(canvas, text)
        if self.GetKind()=='value':
            canvas.Draw(text)

class KicadFPCircle(KicadModuleObject):
    def __init__(self):
        super(KicadFPCircle, self).__init__('fp_circle')
        KicadModuleObject._register(self.header, KicadFPCircle)

    def Render(self, canvas, obj):
        circle = Canvas.Circle()
        super(KicadFPCircle, self).Render(canvas, circle)
        canvas.Draw(circle)

class KicadFPArc(KicadModuleObject):
    def __init__(self):
        super(KicadFPArc, self).__init__('fp_arc')
        KicadModuleObject._register(self.header, KicadFPArc)

    def Render(self, canvas, obj):
        arc = Canvas.Arc()
        super(KicadFPArc, self).Render(canvas, arc)
        canvas.Draw(arc)

class KicadAt(KicadModuleObject):
    def __init__(self):
        super(KicadAt, self).__init__('at', True)
        KicadModuleObject._register(self.header, KicadAt)

    def GetAt(self):
        if self.Attribute(0)=='':
            at = Canvas.Position()
        else:
            at = Canvas.Position(float(self.Attribute(0)), float(self.Attribute(1)))
            if self.Attribute(2)!='':
                at.angle = float(self.Attribute(2))
        return at
    
    def Render(self, canvas, obj):
        if obj:
            at = self.GetAt()
            obj.at.x = canvas.xmm2px(at.x)
            obj.at.y = canvas.ymm2px(at.y)
        super(KicadAt, self).Render(canvas, obj)

class KicadStart(KicadModuleObject):
    def __init__(self):
        super(KicadStart, self).__init__('start', True)
        KicadModuleObject._register(self.header, KicadStart)

    def GetStart(self):
        return Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
    
    def Render(self, canvas, obj):
        # TODO
#         if obj:
#             start = self.GetStart()
#             obj.start.x = canvas.xmm2px(start.x)
#             obj.start.y = canvas.ymm2px(start.y)
        super(KicadStart, self).Render(canvas, obj)
        
class KicadEnd(KicadModuleObject):
    def __init__(self):
        super(KicadEnd, self).__init__('end', True)
        KicadModuleObject._register(self.header, KicadEnd)

    def GetEnd(self):
        return Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))

    def Render(self, canvas, obj):
        #TODO
#         if obj:
#             end = self.GetEnd()
#             obj.end.x = canvas.xmm2px(end.x)
#             obj.end.y = canvas.ymm2px(end.y)
        super(KicadEnd, self).Render(canvas, obj)

class KicadOffset(KicadModuleObject):
    def __init__(self):
        super(KicadOffset, self).__init__('offset', True)
        KicadModuleObject._register(self.header, KicadOffset)

    def GetOffset(self):
        return Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))

    def Render(self, canvas, obj):
        #TODO
#         if obj:
#             end = self.GetEnd()
#             obj.end.x = canvas.xmm2px(end.x)
#             obj.end.y = canvas.ymm2px(end.y)
        super(KicadOffset, self).Render(canvas, obj)

class KicadLayer(KicadModuleObject):
    def __init__(self):
        super(KicadLayer, self).__init__('layer', True)
        KicadModuleObject._register(self.header, KicadLayer)

    def GetLayer(self):
        return self.Attribute(0)
    
    def SetLayer(self, layer):
        self.AddAttribute(layer)
    
    def Render(self, canvas, obj):
        canvas.SelectLayer(self.Attribute(0))
        super(KicadLayer, self).Render(canvas, obj)

class KicadLayers(KicadModuleObject):
    def __init__(self):
        super(KicadLayers, self).__init__('layers', True)
        KicadModuleObject._register(self.header, KicadLayers)

    def GetLayers(self):
        return self.attributes
    
    def Render(self, canvas, obj):
        canvas.SelectLayers(self.attributes)
        super(KicadLayers, self).Render(canvas, obj)

class KicadWidth(KicadModuleObject):
    def __init__(self):
        super(KicadWidth, self).__init__('width', True)
        KicadModuleObject._register(self.header, KicadWidth)

    def GetWidth(self):
        return float(self.Attribute(0))
    
    def Render(self, canvas, obj):
        if obj:
            obj.width = self.GetWidth()
        super(KicadWidth, self).Render(canvas, obj)

class KicadSize(KicadModuleObject):
    def __init__(self):
        super(KicadSize, self).__init__('size', True)
        KicadModuleObject._register(self.header, KicadSize)

    def GetSize(self):
        return Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
    
    def Render(self, canvas, obj):
        if obj:
            obj.size = self.GetSize()
        super(KicadSize, self).Render(canvas, obj)

class KicadDrill(KicadModuleObject):
    def __init__(self):
        super(KicadDrill, self).__init__('drill', True)
        KicadModuleObject._register(self.header, KicadDrill)

    def IsOval(self):
        if self.HasAttribute(0) and self.Attribute(0)=='oval':
            return True
        return False
    
    def GetDrill(self):
        drill = Canvas.Point()
        if self.IsOval():
            if self.HasAttribute(1):
                drill.x = float(self.Attribute(1))
            if self.HasAttribute(2):
                drill.y = float(self.Attribute(2))
        else:
            if self.HasAttribute(0):
                drill.x = float(self.Attribute(0))
        return drill
    
    def Render(self, canvas, obj):
        #TODO
#         if obj:
#             if self.GetDrill():
#                 obj.drill = self.GetDrill()
            
        super(KicadDrill, self).Render(canvas, obj)

class KicadFont(KicadModuleObject):
    def __init__(self):
        super(KicadFont, self).__init__('font')
        KicadModuleObject._register(self.header, KicadFont)

    def Render(self, canvas, obj):
        font = Canvas.Font()
        canvas.SetFont(font)
        super(KicadFont, self).Render(canvas, font)

class KicadThickness(KicadModuleObject):
    def __init__(self):
        super(KicadThickness, self).__init__('thickness', True)
        KicadModuleObject._register(self.header, KicadThickness)

    def GetThickness(self):
        return float(self.Attribute(0))
    
    def Render(self, canvas, obj):
        if obj:
            obj.thickness = float(self.Attribute(0))
        super(KicadThickness, self).Render(canvas, obj)

class KicadCenter(KicadModuleObject):
    def __init__(self):
        super(KicadCenter, self).__init__('center', True)
        KicadModuleObject._register(self.header, KicadCenter)

    def GetCenter(self):
        return Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
    
    def Render(self, canvas, obj):
        if obj:
            obj.size = Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
        super(KicadCenter, self).Render(canvas, obj)

class KicadAngle(KicadModuleObject):
    def __init__(self):
        super(KicadAngle, self).__init__('angle', True)
        KicadModuleObject._register(self.header, KicadAngle)

    def GetAngle(self):
        return float(self.Attribute(0))*math.pi/180.
    
    def Render(self, canvas, obj):
        # TODO
        pass

class KicadTEdit(KicadModuleObject):
    def __init__(self):
        super(KicadTEdit, self).__init__('tedit', True)
        KicadModuleObject._register(self.header, KicadTEdit)

    def GetTimestamp(self):
        return self.Attribute(0)
    
    def SetTimestamp(self, timestamp):
        self.SetAttribute(0, timestamp)

    def Render(self, canvas, obj):
        pass

class KicadDescr(KicadModuleObject):
    def __init__(self):
        super(KicadDescr, self).__init__('descr')
        KicadModuleObject._register(self.header, KicadDescr)

    def GetDescr(self):
        return self.Attribute(0)
    
    def SetDescr(self, descr):
        self.SetAttribute(0, descr)

    def Render(self, canvas, obj):
        pass

class KicadTags(KicadModuleObject):
    def __init__(self):
        super(KicadTags, self).__init__('tags')
        KicadModuleObject._register(self.header, KicadTags)

    def GetTags(self):
        return self.attributes
    
    def AddTag(self, tag):
        self.AddAttribute(tag)

    def Render(self, canvas, obj):
        pass

class KicadAttr(KicadModuleObject):
    def __init__(self):
        super(KicadAttr, self).__init__('attr')
        KicadModuleObject._register(self.header, KicadAttr)

    def GetAttr(self):
        return self.Attribute(0)
    
    def SetAttr(self, attr):
        self.SetAttribute(0, attr)

    def Render(self, canvas, obj):
        pass

class KicadDieLength(KicadModuleObject):
    def __init__(self):
        super(KicadDieLength, self).__init__('die_length')
        KicadModuleObject._register(self.header, KicadDieLength)

    def GetDieLength(self):
        return float(self.Attribute(0))
    
    def SetDieLength(self, die_length):
        self.SetAttribute(0, die_length)

    def Render(self, canvas, obj):
        pass

class KicadRectDelta(KicadModuleObject):
    def __init__(self):
        super(KicadRectDelta, self).__init__('rect_delta', True)
        KicadModuleObject._register(self.header, KicadRectDelta)

    def GetRectDelta(self):
        return Canvas.Point(float(self.Attribute(0)), float(self.Attribute(1)))
    
    def Render(self, canvas, obj):
        pass

class KicadSolderMaskMargin(KicadModuleObject):
    def __init__(self):
        super(KicadSolderMaskMargin, self).__init__('solder_mask_margin', True)
        KicadModuleObject._register(self.header, KicadSolderMaskMargin)

    def GetSolderMaskMargin(self):
        return float(self.Attribute(0))
    
    def SetSolderMaskMargin(self, solder_mask_margin):
        self.SetAttribute(0, solder_mask_margin)

    def Render(self, canvas, obj):
        pass

class KicadSolderPasteMargin(KicadModuleObject):
    def __init__(self):
        super(KicadSolderPasteMargin, self).__init__('solder_paste_margin', True)
        KicadModuleObject._register(self.header, KicadSolderPasteMargin)

    def GetSolderPasteMargin(self):
        return float(self.Attribute(0))
    
    def SetSolderPasteMargin(self, solder_paste_margin):
        self.SetAttribute(0, solder_paste_margin)

    def Render(self, canvas, obj):
        pass

class KicadClearance(KicadModuleObject):
    def __init__(self):
        super(KicadClearance, self).__init__('clearance', True)
        KicadModuleObject._register(self.header, KicadClearance)

    def GetClearance(self):
        return float(self.Attribute(0))
    
    def SetClearance(self, clearance):
        self.SetAttribute(0, clearance)

    def Render(self, canvas, obj):
        pass

class KicadThermalWidth(KicadModuleObject):
    def __init__(self):
        super(KicadThermalWidth, self).__init__('thermal_width', True)
        KicadModuleObject._register(self.header, KicadThermalWidth)

    def GetThermalWidth(self):
        return float(self.Attribute(0))
    
    def SetThermalWidth(self, thermal_width):
        self.SetAttribute(0, thermal_width)

    def Render(self, canvas, obj):
        pass

class KicadThermalGap(KicadModuleObject):
    def __init__(self):
        super(KicadThermalGap, self).__init__('thermal_gap', True)
        KicadModuleObject._register(self.header, KicadThermalGap)

    def GetThermalGap(self):
        return float(self.Attribute(0))
    
    def SetThermalGap(self, thermal_gap):
        self.SetAttribute(0, thermal_gap)

    def Render(self, canvas, obj):
        pass

class KicadZoneConnect(KicadModuleObject):
    def __init__(self):
        super(KicadZoneConnect, self).__init__('zone_connect', True)
        KicadModuleObject._register(self.header, KicadZoneConnect)

    def GetZoneConnect(self):
        return int(self.Attribute(0))
    
    def SetZoneConnect(self, zone_connect):
        self.SetAttribute(0, zone_connect)

    def Render(self, canvas, obj):
        pass

class KicadSolderPasteMarginRatio(KicadModuleObject):
    def __init__(self):
        super(KicadSolderPasteMarginRatio, self).__init__('solder_paste_margin_ratio', True)
        KicadModuleObject._register(self.header, KicadSolderPasteMarginRatio)

    def GetSolderPasteMarginRatio(self):
        return float(self.Attribute(0))
    
    def SetSolderPasteMarginRatio(self, solder_paste_margin_ratio):
        self.SetAttribute(0, solder_paste_margin_ratio)

    def Render(self, canvas, obj):
        pass

class KicadEffects(KicadModuleObject):
    def __init__(self):
        super(KicadEffects, self).__init__('effects', True)
        KicadModuleObject._register(self.header, KicadEffects)

    def Render(self, canvas, obj):
        pass

class KicadHide(KicadModuleObject):
    def __init__(self):
        super(KicadHide, self).__init__('hide', True, False)
        KicadModuleObject._register(self.header, KicadHide)

    def Render(self, canvas, obj):
        pass

class KicadItalic(KicadModuleObject):
    def __init__(self):
        super(KicadItalic, self).__init__('italic', True, False)
        KicadModuleObject._register(self.header, KicadItalic)

    def Render(self, canvas, obj):
        pass

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
KicadFPArc()
KicadCenter()
KicadAngle()
KicadTEdit()
KicadDescr()
KicadTags()
KicadAttr()
KicadOffset()
KicadDieLength()
KicadRectDelta()
KicadSolderMaskMargin()
KicadSolderPasteMargin()
KicadClearance()
KicadThermalWidth()
KicadThermalGap()
KicadSolderPasteMarginRatio()
KicadZoneConnect()
KicadEffects()
KicadHide()
KicadItalic()