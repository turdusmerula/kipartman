from dialogs.panel_schematic import PanelSchematic
from frames.dropdown_dialog import DropdownDialog
from frames.select_part_frame import SelectPartFrame, EVT_SELECT_PART_OK_EVENT
import helper.tree
from kicad.kicad_lib_file import KicadLibFile

class DataModelModule(helper.tree.TreeItem):
    def __init__(self, module):
        super(DataModelModule, self).__init__()
        self.module = module
        
    def GetValue(self, col):
        vMap = { 
            0 : self.module.reference,
            1 : self.module.value,
            2 : self.module.footprint,
        }
        return vMap[col]

class DataModelBomPart(helper.tree.TreeItem):
    def __init__(self, bom, bom_part):
        super(DataModelBomPart, self).__init__()
        self.bom = bom
        self.bom_part = bom_part
        
    def GetValue(self, col):
        num_modules = 0
        if self.bom.part_modules.has_key(self.bom_part.id):
            num_modules = len(self.bom.part_modules[self.bom_part.id])
        vMap = { 
            0 : str(self.bom_part.id),
            1 : self.bom_part.name,
            2 : self.bom_part.description,
            3 : self.bom_part.comment,
            4 : str(num_modules)
        }
        return vMap[col]

class DataModelBomModule(helper.tree.TreeItem):
    def __init__(self, bom_module):
        super(DataModelBomModule, self).__init__()
        self.bom_module = bom_module
        
    def GetValue(self, col):
        vMap = { 
            0 : self.bom_module.reference,
            1 : self.bom_module.value,
            2 : self.bom_module.footprint
        }
        return vMap[col]

class SchematicFrame(PanelSchematic): 
    def __init__(self, parent, file):
        super(SchematicFrame, self).__init__(parent)
        
        # create module list
        self.tree_parts_manager = helper.tree.TreeManager(self.tree_parts)
        self.tree_parts_manager.AddTextColumn("Reference")
        self.tree_parts_manager.AddTextColumn("Value")
        self.tree_parts_manager.AddTextColumn("Footprint")

        self.file = file
        self.schematic = KicadLibFile()
        
        
    def load(self):
        self.loadSchematic()
        
    def loadSchematic(self):
        self.LoadFile(self.file)
        
        self.tree_parts_manager.ClearItems()
    

    def onToolRefreshSchematic( self, event ):
        self.load()
    
