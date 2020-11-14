import json
import os
from kicad.kicad_schematic_file import KicadSchematicFile, KicadComp, KicadAR
from helper.exception import print_stack
# from helper.parts_cache import PartsCache
from helper.log import log
import api.data.part

class BomException(BaseException):
    def __init__(self, error):
        self.error = error
        
class Bom(object):
    def __init__(self):
        self.filename = None
        self.parts = []
        self.part_components = {}
        self.component_part = {}
        self.schematic = None
        self.saved = True
        
    def LoadFile(self, filename):
        log.info(f"Load BOM {filename}")
        
        self.part_components = {}
        self.component_part = {}
        self.parts = []
        
        if(os.path.isfile(filename)==False):
            raise Exception("Error: %s does not exists" % filename)
        
        with open(filename, 'r', encoding='utf-8') as infile:
            content = json.load(infile)
        
        # load associated schematic
        self.schematic = KicadSchematicFile()
        self.schematic.LoadFile(content['schematic'])
            
        part_not_found = []
        for part in content['parts']:
            # load part from server
            try:
                self.parts.append(self.parts_cache.Find(part['id']))
                self.part_components[part['id']] = []
            except:
                print_stack()
                log.warning(f"part {part['id']} not found on server")
                part_not_found.append(part)

        component_not_found= []
        part_id_not_found = []
        # load components from BOM
        for part_id in content['components']:
            part = None
            # get part from list
            for p in self.parts:
                if p.id==int(part_id):
                    part = p
                    break
            if part:
                schematic_components = self.schematic.Components()
                # get components from schematic
                for component in content['components'][part_id]:
                    if int(part_id) in self.part_components:
                        if self.schematic.ExistComponent(component['timestamp']):
                            self.part_components[int(part_id)].append(self.schematic.GetComponent(component['timestamp']))
                            self.component_part[component['timestamp']] = part
                        else:
                            log.warning(f"component {component['timestamp']} does not exist in schematic")
                            component_not_found.append(component)
                    else:
                        log.warning(f"part {part_id} not found on bom")
                        part_id_not_found.append(int(part_id))
            else:
                log.warning(f"part {part_id} from BOM does not exist on server")
                part_id_not_found.append(int(part_id))
            
        # TODO: show error messages from part_not_found, component_not_found and part_id_not_found
        self.filename = filename
        self.saved = True
 
    def byteify(self, input):
        if isinstance(input, dict):
            return {self.byteify(key): self.byteify(value)
                    for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        else:
            return input.encode('utf-8')
        
    def SaveFile(self, filename):
        log.info(f"Save BOM {filename}")
        
        with open(filename, 'w', encoding='utf-8') as outfile:
            parts = []
            for part in self.parts:
                parts.append({'id': part.id, 'name': part.name, 'description': part.description})
            
            part_components = {}
            for part_name in self.part_components:
                if len(self.part_components[part_name])>0:
                    part_components[part_name] = []
                for component, instance in self.part_components[part_name]:
                    if instance:
                        part_components[part_name].append({'timestamp': instance.timestamp, 'reference': instance.reference, 'value': component.value}) 
                    else:
                        part_components[part_name].append({'timestamp': component.timestamp, 'reference': component.reference, 'value': component.value}) 
                        
            
            input = { 'schematic': self.schematic.filename, 'parts': parts, 'components': part_components }
#            json_string = json.dumps(input, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')).encode('utf8')
            json_string = json.dumps(input, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
            outfile.write(json_string)
#            json.dump(self.byteify(input), outfile, sort_keys=True,
#                  indent=4, separators=(',', ': '))
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
    
#     def FindPartComponent(self, component, part_id):
#         try:
#             part = self.component_part[component.timestamp]
#         except:
#             raise BomException("Component %s does not exist in BOM"%component.timestamp)
#         for part in 

    def SetSchematic(self, file):
        self.schematic = KicadSchematicFile()
        self.schematic.LoadFile(file)

        if self.schematic is not None and self.schematic.objects is not None:
            self._load_nodes(self.schematic.parent.nodes)
            
            for sheet in self.schematic.objects.sheets:
                if sheet.schematic is not None:
                    self._load_nodes(sheet.schematic.parent.nodes)

    def _load_nodes(self, nodes):
        sheet_timestamps = self.schematic.SheetTimetamps()
        
        for obj in nodes:
            if isinstance(obj, KicadComp):
                if obj.kipart_id:
                    try:
                        parts = api.data.part.find([api.data.part.FilterPartId(int(obj.kipart_id))])
                        if len(parts)>0:
                            part = parts[0]
                            self.AddPart(part)
                        
                            instances = 0
                            for instobj in obj.nodes:
                                if isinstance(instobj, KicadAR):
                                    sheet_timestamp = "/".join(instobj.timestamp.split('/')[:-1])
                                    if sheet_timestamp in sheet_timestamps:
                                        instances += 1
                                        self.AddPartComponent(part, obj, instobj)
                                    else:
                                        print(f"Ignored {instobj.timestamp}")
                            if instances==0:
                                self.AddPartComponent(part, obj, None)
                                
                        else:
                            print(f"part id {obj.kipart_id} not found")
                    except Exception as e:
                        print_stack()
                        print(e)
                        
#         for component, ar in self.schematic.Components():
#             if component.kipart_id:
#                 # this is an instance of component
#                 part = None
#                 try:
#                     part = self.parts_cache.Find(component.kipart_id)
#                     self.AddPart(part)
#                     self.AddPartComponent(part, component, ar)
#                 except Exception as e:
#                     print_stack()
#                     log.error(format(e))
        
    def AddPart(self, part):
        if part not in self.parts:
            self.parts.append(part)
            self.part_components[part.id] = []
        self.saved = False

    def AddPartComponent(self, part, component, instance):
        self.part_components[part.id].append([component, instance])
        if instance:
            self.component_part[instance.timestamp] = part
        else:
            self.component_part[component.timestamp] = part
            
        self.saved = False
    
    def RemovePart(self, part):
        self.parts.remove(part)
        for component in self.part_components[part.id]:
            self.component_part.pop(component.timestamp)
        self.part_components.pop(part.id)
        self.saved = False
        
    def RemovePartComponent(self, component):
        part = self.component_part[component.timestamp]
        self.component_part.pop(component.timestamp)
        
        for part_component in self.part_components[part.id]:
            if part_component.timestamp==component.timestamp:
                self.part_components[part.id].remove(part_component)

        self.saved = False
    
    def NumComponents(self, bom_part):
        num_components = 0
        if bom_part.id in self.part_components:
            num_components = num_components+len(self.part_components[bom_part.id])
        return num_components
    
