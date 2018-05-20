import os
from kicad_object import *
import re 
import math
import tempfile
import io

class KicadSchematicFile(object):
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
        self.file = io.open(filename, "rb")
        self.line = ''
        self.buff = ''

        self.parent = KicadObject('')
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

        self.parent = KicadObject('')
        self.read_lines(self.parent) 
        #self.Write(self.parent, 0)
                    
        if self.onChanged:
            self.onChanged()
        
    def Render(self, filename, width=256, height=256):
        canvas = Canvas.LibraryCanvas()
        surface = canvas.Render(self.parent, width, height)
        surface.write_to_png (filename)
    
    def Save(self):
        self.SaveAs(self.filename)

    def SaveAs(self, filename):
        with io.open(filename, "w", encoding='utf-8') as f:
            if len(self.parent.nodes)>0:
                for node in self.parent.nodes:
                    self.Write(f, node)
    
    @staticmethod
    def to_utf8(text):
        try:
            return unicode(text, 'utf-8')
        except TypeError:
            return text
        
    def Write(self, file, obj, level=0):
        line = "%s%s"%(tab(level), obj.header)
        i = 0
        for attr in obj.attributes:
            if obj.attribute_types[i]=='string':
                line = line+' "'+attr+'"'
            else:
                line = line+" "+attr
            i = i + 1
        
        try:
            l = self.to_utf8(line)+u'\n'
            file.write(l)
        except Exception as e:
            print "Error during file write:", line 
            print format(e)
            
        if len(obj.nodes)>0:
            for node in obj.nodes:
                self.Write(file, node) #, level+1)
        
    def DebugWrite(self, obj, level=0):
        line = "%s%s"%(tab(level), obj.header)
        for attr in obj.attributes:
            line = line+" "+attr
        
        print "++", line, type(obj)
        if len(obj.nodes)>0:
            for node in obj.nodes:
                self.DebugWrite(node, level+1)

    def read_lines(self, parent):
        while self.next_line()!=EOF:
            # skip comment lines
            c = self.observe(1)
            if c=='#':
                continue
            
            header, attr_type = self._read_field()
            
            if header is None:
                continue
        
            obj = KicadSchematicObject.Instance(header)
            parent.AddNode(obj)
            
            attr, attr_type = self._read_field()
            while attr!=EOL:
                obj.AddAttribute(attr, attr_type)
                attr, attr_type = self._read_field()

            if header.startswith('$End'):
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

        attr_type = ''
        if c=='':
            return EOL, ''
        elif c=='"':
            attr_type = 'string'
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

        return field, attr_type

    def Components(self):
        components = []
        for obj in self.parent.nodes:
            if isinstance(obj, KicadComp):
                components.append(obj)
        return components
        

class KicadSchematicObject(KicadObject):
    def __init__(self, header, category=False):
        super(KicadSchematicObject, self).__init__(header)
        self.category = category
        
    @staticmethod
    def Instance(header):
        """
        Create an instance of object type if type registered, or KicadSchematicObject if not
        """
        for key in KicadObject.mapping:
            if re.compile(key).match(header):
                obj = KicadObject.mapping[key]()
                obj.header = header
                return obj
        return KicadSchematicObject(header)
    
class KicadDescr(KicadSchematicObject):
    def __init__(self):
        super(KicadDescr, self).__init__('\$Descr', True)
        KicadObject._register(self.header, KicadDescr)


class KicadComp(KicadSchematicObject):
    def __init__(self):
        super(KicadComp, self).__init__('\$Comp', True)
        KicadObject._register(self.header, KicadComp)

    def getL(self):
        for node in self.nodes:
            if isinstance(node, KicadL):
                return node
        return None
    
    def getF(self, index):
        for node in self.nodes:
            if isinstance(node, KicadF) and node.attributes[0]==str(index):
                return node
        return None

    def getF_Name(self, name):
        for node in self.nodes:
            if isinstance(node, KicadF) and len(node.attributes)>9 and node.attributes[9]==name:
                return node
        return None


    def fget_symbol(self):
        l = self.getL()
        if l:
            return l.Attribute(0)
        return ''
    
    def fset_symbol(self, value):
        l = self.getL()
        l.SetAttribute(0, value)    


    def fget_reference(self):
        l = self.getL()
        if l:
            return l.Attribute(1)
        return ''
    
    def fset_reference(self, value):
        l = self.getL()
        l.SetAttribute(1, value)    
        
        f = self.getF(0)
        f.SetAttribute(1, value, 'string')    


    def fget_value(self):
        f = self.getF(1)
        if f:
            return f.Attribute(1)
        return ''
    
    def fset_value(self, value):
        f = self.getF(1)
        f.SetAttribute(1, value, 'string')    


    def fget_footprint(self):
        f = self.getF(2)
        if f:
            return f.Attribute(1)
        return ''
    
    def fset_footprint(self, value):
        f = self.getF(2)
        f.SetAttribute(1, value, 'string')    


    def fget_kipart_id(self):
        f = self.getF_Name('kipart_id')
        if f:
            return f.Attribute(1)
        return ''
    
    def fset_kipart_id(self, value):
        f = self.getF_Name('kipart_id')
        if not f:
            f = KicadF(parent=self)
            f.add_attributes()
            f.SetAttribute(9, 'kipart_id', 'string')    
        f.SetAttribute(1, value, 'string')    


    def fget_kipart_sku(self):
        f = self.getF_Name('kipart_sku')
        if f:
            return f.Attribute(1)
        return ''
    
    def fset_kipart_sku(self, value):
        f = self.getF_Name('kipart_sku')
        if not f:
            f = KicadF(parent=self)
            f.add_attributes()
            f.SetAttribute(9, 'kipart_sku', 'string')    
        f.SetAttribute(1, value, 'string')    

    symbol = property(fget=fget_symbol, fset=fset_symbol)
    reference = property(fget=fget_reference, fset=fset_reference)
    value = property(fget=fget_value, fset=fset_value)
    footprint = property(fget=fget_footprint, fset=fset_footprint)
    kipart_id = property(fget=fget_kipart_id, fset=fset_kipart_id)
    kipart_sku = property(fget=fget_kipart_sku, fset=fset_kipart_sku)


class KicadF(KicadSchematicObject):
    def __init__(self, parent=None):
        super(KicadF, self).__init__('F')
        KicadObject._register(self.header, KicadF)
        self.parent = parent
        
        if parent:
            index = 0
            findex = 0
            for node in self.parent.nodes:
                if isinstance(node, KicadF):
                    findex = index
                index = index + 1
            parent.InsertNode(findex+1, self)
    
    def add_attributes(self):
        index = 0
        for node in self.parent.nodes:
            if isinstance(node, KicadF) and node!=self:
                index = index + 1
            elif isinstance(node, KicadF) and node==self:
                break
        
        self.SetAttribute(0, str(index))
        self.SetAttribute(1, '', 'string')
        self.SetAttribute(2, 'H')
        self.SetAttribute(3, '0')
        self.SetAttribute(4, '0')
        self.SetAttribute(5, '0')
        self.SetAttribute(6, '0001')
        self.SetAttribute(7, 'C')
        self.SetAttribute(8, 'CNN')
        
class KicadL(KicadSchematicObject):
    def __init__(self):
        super(KicadL, self).__init__('L')
        KicadObject._register(self.header, KicadL)
        

"""
Instanciate at least one time to force objects registration
"""
KicadDescr()
KicadComp()
KicadF()
KicadL()
