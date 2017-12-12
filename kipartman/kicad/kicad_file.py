import wx
import os
from kicad_objects import *
import Canvas

def tab(level):
    res = ''
    for i in range(level):
        res = res+'  '
    return res

class KicadFile(object):
    def __init__(self):
        self.filename = None
        self.onChanged = None
        self.parent = KicadObject('')
        
    def LoadFile(self, filename):
        if(os.path.isfile(filename)==False):
            self.filename = None
#            wx.MessageBox("Error: %s does not exists" % filename, "File error", wx.OK | wx.ICON_ERROR)
            raise Exception("Error: %s does not exists" % filename)

        self.filename = filename
        self.file = open(filename, 'r')
        self.buff = ''
        
        self.read_blocks(self.parent) 
        self.Write(self.parent, 0)
        
        for node in self.parent.nodes:
            print node.header
            
        if self.onChanged:
            self.onChanged()
    
    def Render(self, filename):
        canvas = Canvas.FootprintCanvas()
        surface = canvas.Render(self.parent)
        surface.write_to_png (filename)
        
    def Write(self, obj, level=0):
        line = "%s(%s"%(tab(level), obj.header)
        for attr in obj.attributes:
            line = line+" "+attr
        
        if len(obj.nodes)>0:
            print line
            for node in obj.nodes:
                self.Write(node, level+1)
            print "%s)"%tab(level)
        else:
            line = line+")"
            print line
    
    def read_blocks(self, parent):
        block_header = self._read_block_header()
        if block_header=='':
            return None
        obj = KicadObject.Instance(block_header)        
        parent.AddNode(obj)

        attr = self._read_field()
        while attr!='':
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
            return ''
        
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
