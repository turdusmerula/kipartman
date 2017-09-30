import json
import os
import wx
from kicad.pcb import Module
import rest
from kicad.pcb import Pcb

class BomException(BaseException):
    def __init__(self, error):
        self.error = error
        
class Bom(object):
    def __init__(self):
        self.filename = None
        self.parts = []
        self.part_modules = {}
        self.module_part = {}
        self.pcb = None
        self.saved = True

    def LoadFile(self, filename):
        print "Load BOM", filename
#        for part in self.parts:
#            self.parts.remove(part)
        self.part_modules = {}
        self.module_part = {}
        self.parts = []
        
        if(os.path.isfile(filename)==False):
            raise Exception("Error: %s does not exists" % filename)
        
        with open(filename, 'r') as infile:
            content = json.load(infile)
        
        # load associated pcb
        if self.pcb is None:
            self.pcb = Pcb()
            self.pcb.LoadFile(content['pcb'])
            
        part_not_found = []
        for part in content['parts']:
            # load part from server
            try:
                self.parts.append(rest.api.find_part(part['id']))
                self.part_modules[part['id']] = []
            except:
                print "Warning: part %d not found on server"%part['id']
                part_not_found.append(part)

        module_not_found= []
        part_id_not_found = []
        # load modules from BOM
        for part_id in content['modules']:
            part = None
            # get part from list
            for p in self.parts:
                if p.id==int(part_id):
                    part = p
                    break
            if part:
                # get modules from pcb
                for module in content['modules'][part_id]:
                    if self.part_modules.has_key(int(part_id)):
                        if self.pcb.ExistModule(module['timestamp']):
                            self.part_modules[int(part_id)].append(self.pcb.GetModule(module['timestamp']))
                            self.module_part[module['timestamp']] = part
                        else:
                            print "Warning: module %s does not exist in pcb"%module['timestamp']
                            module_not_found.append(module)
                    else:
                        print "Warning: part %d not found on bom"%part_id
                        part_id_not_found.append(int(part_id))
            else:
                print "Warning: part %d from BOM does not exist on server"%int(part_id)
                part_id_not_found.append(int(part_id))
            
        # TODO: show error messages from part_not_found, module_not_found and part_id_not_found
        self.filename = filename
        self.saved = True

    def pcbChanged(self):
        for part_id in self.part_modules:
            for module in self.part_modules[int(part_id)]:
                if self.pcb.ExistModule(module.timestamp)==False:
                    self.parts[int(part_id)].pop(module)
                    self.module_part.pop(module)
 
    def SaveFile(self, filename):
        print "Save BOM", filename
        with open(filename, 'w') as outfile:
            parts = []
            for part in self.parts:
                parts.append({'id': part.id, 'name': part.name, 'description': part.description})
            
            part_modules = {}
            for part_name in self.part_modules:
                if len(self.part_modules[part_name])>0:
                    part_modules[part_name] = []
                for module in self.part_modules[part_name]:
                    part_modules[part_name].append({'timestamp': module.timestamp, 'reference': module.reference, 'value': module.value}) 
            
            json.dump({ 'pcb': self.pcb.filename, 'parts': parts, 'modules': part_modules }, outfile, sort_keys=True,
                  indent=4, separators=(',', ': '))
        self.filename = filename
        self.saved = True

    def Save(self):
        self.SaveFile(self.filename)
    
    def Parts(self):
        return self.parts

    def ExistPart(self, part):
        for p in self.parts:
            if p.id==part.id:
                return True
        return False
    
#     def FindPartModule(self, module, part_id):
#         try:
#             part = self.module_part[module.timestamp]
#         except:
#             raise BomException("Module %s does not exist in BOM"%module.timestamp)
#         for part in 
    def AddPart(self, part):
        self.parts.append(part)
        self.part_modules[part.id] = []
        self.saved = False

    def AddPartModule(self, part, module):
        self.part_modules[part.id].append(module)
        self.module_part[module.timestamp] = part
        self.saved = False
    
    def RemovePart(self, part):
        self.parts.remove(part)
        for module in self.part_modules[part.id]:
            self.module_part.pop(module.timestamp)
        self.part_modules.pop(part.id)
        self.saved = False
        
    def RemovePartModule(self, module):
        part = self.module_part[module.timestamp]
        self.module_part.pop(module.timestamp)
        
        for part_module in self.part_modules[part.id]:
            if part_module.timestamp==module.timestamp:
                self.part_modules[part.id].remove(part_module)

        self.saved = False
    
    def NumModules(self, bom_part):
        num_modules = 0
        if self.part_modules.has_key(bom_part.id):
            num_modules = num_modules+len(self.part_modules[bom_part.id])
        return num_modules
    
