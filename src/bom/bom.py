import json
import os
import wx
from kicad.pcb import Module
from api.queries import PartsQuery

class Bom(object):
    def __init__(self, pcb):
        self.filename = None
        self.parts = []
        self.part_modules = {}
        self.module_part = {}
        self.pcb = pcb
        self.saved = True
        pcb.onChanged = self.pcbChanged

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
        
        part_not_found = []
        for part in content['parts']:
            # load part from server
            try:
                self.parts.append(PartsQuery().get(part['id'])[0])
                self.part_modules[part['id']] = []
            except:
                part_not_found.append(part)

        module_not_found= []
        for part_id in content['modules']:
            # get part from list
            for part in self.parts:
                if part.id==part_id:
                    break

            # get modules from pcb
            for module in content['modules'][part_id]:
                if self.pcb.ExistModule(module['timestamp']):
                    print "----", module['timestamp']
                    self.part_modules[int(part_id)].append(self.pcb.GetModule(module['timestamp']))
                    self.module_part[module['timestamp']] = part
                else:
                    module_not_found.append(module)
             
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
            
            json.dump({ 'parts': parts, 'modules': part_modules }, outfile, sort_keys=True,
                  indent=4, separators=(',', ': '))
        self.saved = True

    def Save(self):
        self.SaveFile(self.filename)
    
    def Parts(self):
        return self.parts

    def AddPart(self, part):
        self.parts.append(part)
        self.part_modules[part.id] = []
        self.saved = False

    def AddModule(self, part, module):
        self.part_modules[part.id].append(module)
        self.module_part[module.timestamp] = part
        self.saved = False
    
    def RemovePart(self, part):
        self.parts.remove(part)
        for module in self.part_modules[part.id]:
            self.module_part.pop(module.timestamp)
        self.part_modules.pop(part.id)
        self.saved = False
        
    def RemoveModule(self, module):
        part = self.module_part[module.timestamp]
        self.module_part.pop(module.timestamp)
        self.part_modules[part.id].remove(module)
        self.saved = False