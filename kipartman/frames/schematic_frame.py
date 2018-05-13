from dialogs.panel_schematic import PanelSchematic
from frames.dropdown_dialog import DropdownDialog
from frames.select_part_frame import SelectPartFrame, EVT_SELECT_PART_OK_EVENT
import helper.tree
from kicad.kicad_schematic_file import KicadSchematicFile
from frames.part_preview_data_frame import PartPreviewDataFrame
import wx
import re
import os
from part_parameters_frame import DataModelPartParameter
import tempfile
import hashlib
from pathlib2 import Path

class DataModelPart(helper.tree.TreeItem):
    def __init__(self, component):
        super(DataModelPart, self).__init__()
        self.component = component
        
    def GetValue(self, col):
        vMap = { 
            0 : self.component.reference,
            1 : self.component.value,
            2: self.component.kicad_sku,
            3: self.component.symbol,
            4: self.component.footprint
        }
        return vMap[col]

class TreeManagerParts(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerParts, self).__init__(tree_view, *args, **kwargs)
                
    def FindPart(self, component):
        for data in self.data:
            if isinstance(data, DataModelPart) and data.component.reference==component.reference:
                return data
        return None

    def AppendPart(self, component):
        partobj = DataModelPart(component)
        self.AppendItem(None, partobj)
        return partobj


class SchematicFrame(PanelSchematic): 
    def __init__(self, parent, file):
        super(SchematicFrame, self).__init__(parent)
        
        # create module list
        self.tree_parts_manager = TreeManagerParts(self.tree_parts, context_menu=self.menu_parts)
        self.tree_parts_manager.AddTextColumn("Reference")
        self.tree_parts_manager.AddTextColumn("Value")
        self.tree_parts_manager.AddTextColumn("Part")
        self.tree_parts_manager.AddTextColumn("Symbol")
        self.tree_parts_manager.AddTextColumn("Footprint")
        self.tree_parts_manager.OnSelectionChanged = self.onTreePartsSelChanged

        self.file = file
        self.schematic = KicadSchematicFile()
        
        self.data_frame = PartPreviewDataFrame(self.panel_preview)
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.panel_preview.SetSizer( sizer )
        sizer.Fit( self.panel_preview )
        sizer.Add(self.data_frame, 0, wx.ALL|wx.EXPAND, 0)
        self.panel_preview.Layout()
                
        # used to know if reload dialog is already shown
        self.has_reload_dialog = False
        
        self.load()

    def load(self):
        self.loadSchematic()
        
    def loadSchematic(self):
        self.schematic.LoadFile(self.file)
        self.schematic.Save()
        #self.schematic.DebugWrite(self.schematic.parent)
        
        self.tree_parts_manager.SaveState()
        
        # load schematic parts
        for component in self.schematic.Components():
            partobj = self.tree_parts_manager.FindPart(component)
            if partobj:
                partobj.component = component
            
            if self.tree_parts_manager.DropStateObject(partobj)==False:
                self.tree_parts_manager.AppendPart(component)
            
        self.tree_parts_manager.PurgeState()
    
    def reload(self):
        if self.has_reload_dialog:
            # reload dialog already pending
            return

        tmp_file = tempfile.NamedTemporaryFile()
        self.schematic.SaveAs(tmp_file.name)
        content = ''
        with open(tmp_file.name, 'rb') as f:
            content = f.read()
        src_md5 = hashlib.md5(content).hexdigest()
        
        content = ''
        with open(self.file, 'rb') as f:
            content = f.read()
        dst_md5 = hashlib.md5(content).hexdigest()
        
        if src_md5!=dst_md5:
            self.has_reload_dialog = True
            res = wx.MessageDialog(self, "%s modified, reload it?" % self.file, "File changed", wx.YES_NO | wx.ICON_QUESTION).ShowModal()
            if res == wx.ID_YES:
                self.load()
            self.has_reload_dialog = False
    
    def onToolRefreshSchematic( self, event ):
        self.load()
    
    def onTreePartsSelChanged( self, event ):
        items = self.tree_parts.GetSelections()

    def onMenuPartsLinkSelection( self, event ):
        dropdown = DropdownDialog(self.tree_parts, SelectPartFrame, "")
        dropdown.panel.Bind( EVT_SELECT_PART_OK_EVENT, self.onSelectPartCallback )
        dropdown.Dropdown()

    def get_symbol(self, path):
        return re.sub(r".*\.lib/", "", path).replace(".mod", "")
    
    def get_footprint(self, path):
        lib = os.path.basename(os.path.dirname(path)).replace(".pretty", "")
        footprint = os.path.basename(path).replace(".kicad_mod", "")
        return lib+":"+footprint
    
    def onSelectPartCallback(self, part_event):
        part = part_event.data

        symbol = None
        if part.symbol:
            symbol = self.get_symbol(part.symbol.source_path)
            
        footprint = None
        if part.footprint:
            footprint = self.get_footprint(part.footprint.source_path)
        
        items = self.tree_parts.GetSelections()
        if items:
            for item in items:
                if item.IsOk():
                    partobj = self.tree_parts_manager.ItemToObject(item)
                    if symbol:
                        partobj.component.symbol = symbol
                    if footprint:
                        partobj.component.footprint = footprint
                    if part.value_parameter:
                        for parameter in part.parameters:
                            if parameter.name==part.value_parameter:
                                paramobj = DataModelPartParameter(part, parameter)
                                partobj.component.value = paramobj.nom_string()
                    partobj.component.kicad_part = unicode(part.id)
                    partobj.component.kicad_sku = unicode(part.name)
                    
                    self.schematic.Save()

        self.load()

