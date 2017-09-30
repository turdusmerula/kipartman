import wx
import os

class Pcb(object):
    def __init__(self):
        self.filename = None
        self.modules = []
        self.onChanged = None
        
    def LoadFile(self, filename):
        if(os.path.isfile(filename)==False):
            self.filename = None
#            wx.MessageBox("Error: %s does not exists" % filename, "File error", wx.OK | wx.ICON_ERROR)
            raise Exception("Error: %s does not exists" % filename)

        self.filename = filename
        self.file = open(filename, 'r')
        self.buff = ''
        
        self.modules = []
        
        block_header = self._read_block_header()
        if block_header!='kicad_pcb':
            raise ValueError('Invalid file format, not a kicad_pcb file')
        
        block_header = self._read_block_header()
        while block_header!='':
            if block_header=='module':
                self.modules.append(self._read_module_block())
            else:
                self._read_block()
            block_header = self._read_block_header()
        
        if self.onChanged:
            self.onChanged()
    
    def ExistModule(self, timestamp):
        for module in self.modules:
            if module.timestamp==timestamp:
                return True
        return False
    
    def GetModule(self, timestamp):
        for module in self.modules:
            if module.timestamp==timestamp:
                return module
        return None

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
    
    def unread(self, buff):
        self.buff = buff+self.buff

    def GetModules(self):
        return self.modules

    def _read_block_header(self):
        """
        Read next block header
        """
        # read spaces
        c = self.observe(1)
        while c!='' and c!='(' and c!=')':
            c = self.observe(1)
            if c!='(' and c!=')':
                self.read(1)

        c = self.observe(1)
        if c==')':
            return ''
        elif c=='(':
            header = ''
            self.read(1)
            c = self.observe(1)
            while c!='' and c!=' ' and c!='(' and c!=')':
                c = self.observe(1)
                if c!='' and c!=' ' and c!='(' and c!=')':
                    header = header+c
                    self.read(1)

            return header
        return ""
    
    def _read_field(self):
        field = ''
        
        # read spaces
        c = self.observe(1)
        while c!='' and not c.isalnum() and c!='"':
            c = self.observe(1)
            if not c.isalnum() and c!='"':
                self.read(1)

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
            while c!='' and c!=' ' and c!='(' and c!=')':
                c = self.observe(1)
                if c!=' ' and c!='(' and c!=')':
                    field = field+c
                    c = self.read(1)

        return field
    
    def _read_block(self):
        """
        Read block until the end
        """
        inner = 1
        c = self.observe(1)
        while inner>0 and c!='':
            if c=='(':
                inner = inner+1
            elif c==')':
                inner = inner-1
            c = self.read(1)

    def _read_module_block(self):
        """
        Read a module block
        """
        print "# module"
        module = Module()
        module.footprint = self._read_field()
        print 'tstamp', module.footprint
        
        block_header = self._read_block_header()
        while block_header!='':
            if block_header=='tstamp':
                module.timestamp = self._read_field()
                print 'tstamp', module.timestamp
                self._read_block()
            elif block_header=='path':
                module.path = self._read_field()
                print 'path', module.path
                self._read_block()
            elif block_header=='fp_text':
                type = self._read_field()
                if type=='reference':
                    module.reference = self._read_field()
                    print 'reference', module.reference
                elif type=='value':
                    module.value = self._read_field()
                    print 'value', module.value
                self._read_block()
            else:
                self._read_block()
            block_header = self._read_block_header()
        self._read_block()
        
        return module

class Module(object):
    def __init__(self, timestamp='', reference='', value='', footprint='', path=''):
        self.timestamp = timestamp
        self.reference = reference
        self.value = value
        self.footprint = footprint
        self.path = path
