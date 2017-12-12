import wx
import os
from kicad_object import KicadObject
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
        self.Write(self.parent, 0)
        
        for node in self.parent.nodes:
            print node.header
            
        if self.onChanged:
            self.onChanged()

    def Render(self, filename):
        """
        Render to png file
        """
        pass
    
    def Write(self, obj, level=0):
        """
        Write to string buffer
        """
        pass
    
    def read_blocks(self, parent):
        pass
        
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
