from dialogs.panel_bom import PanelBom
from frames.dropdown_dialog import DropdownDialog
from frames.select_part_frame import SelectPartFrame, EVT_SELECT_PART_OK_EVENT
from kicad.pcb import Pcb
from bom.bom import Bom
import wx.dataview
import os
from docutils.parsers.rst.directives import path
import helper.tree


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

class BomFrame(PanelBom): 
    def __init__(self, parent):
        super(BomFrame, self).__init__(parent)
        
        # create module list
        self.tree_modules_manager = helper.tree.TreeManager(self.tree_modules)
        self.tree_modules_manager.AddTextColumn("Reference")
        self.tree_modules_manager.AddTextColumn("Value")
        self.tree_modules_manager.AddTextColumn("Footprint")
        
        # create bom parts list
        self.tree_bom_parts_manager = helper.tree.TreeManager(self.tree_bom_parts)
        self.tree_bom_parts_manager.AddTextColumn("Id")
        self.tree_bom_parts_manager.AddTextColumn("Name")
        self.tree_bom_parts_manager.AddTextColumn("Description")
        self.tree_bom_parts_manager.AddTextColumn("Comment")
        self.tree_bom_parts_manager.AddTextColumn("Modules")

        # create bom modules list
        self.tree_bom_modules_manager = helper.tree.TreeManager(self.tree_bom_modules)
        self.tree_bom_modules_manager.AddTextColumn("Reference")
        self.tree_bom_modules_manager.AddTextColumn("Value")
        self.tree_bom_modules_manager.AddTextColumn("Footprint")

        self.bom = Bom()

        self.enableBom(False)
        self.enableBrd(False)

    def load(self):
        self.loadModules()
        self.loadBomParts()
        self.loadBomModules()
        
    def loadModules(self):
        self.tree_modules_manager.ClearItems()

        if self.bom:
            for module in self.bom.pcb.GetModules():
                if self.bom.module_part.has_key(module.timestamp)==False:
                    self.tree_modules_manager.AppendItem(None, DataModelModule(module))
    
    def loadBomParts(self):
        self.tree_bom_parts_manager.ClearItems()
        
        if self.bom:
            for bom_part in self.bom.Parts():
                self.tree_bom_parts_manager.AppendItem(None, DataModelBomPart(self.bom, bom_part))
    
    def loadBomModules(self):
        self.tree_bom_modules_manager.ClearItems()

        if self.bom:
            item = self.tree_bom_parts.GetSelection()
            bom_part = None
            if item.IsOk():
                bom_part = self.tree_bom_parts_manager.ItemToObject(item).bom_part
    
                for module in self.bom.part_modules[bom_part.id]:
                    self.tree_bom_modules_manager.AppendItem(None, DataModelBomModule(module))
    
    def enableBrd(self, enabled=True):
        self.tree_modules.Enabled = enabled
    
    def enableBom(self, enabled=True):
        self.button_add_bom_module.Enabled = enabled
        self.button_remove_bom_module.Enabled = enabled
        self.button_add_bom_part.Enabled = enabled
        self.button_remove_bom_part.Enabled = enabled
        self.toolbar_bom.Enabled = enabled
        self.tree_bom_parts.Enabled = enabled
        self.tree_bom_modules.Enabled = enabled

    # Virtual event handlers, overide them in your derived class
    def onButtonAddBomModuleClick( self, event ):
        item = self.tree_modules.GetSelection()
        if item.IsOk():
            module = self.tree_modules_manager.ItemToObject(item).module
        else:
            return
        
        item = self.tree_bom_parts.GetSelection()
        if item.IsOk():
            part = self.tree_bom_parts_manager.ItemToObject(item).bom_part
            self.bom.AddPartModule(part, module)

            self.loadBomModules()
            self.loadModules()

    def onButtonRemoveBomModuleClick( self, event ):
        item = self.tree_bom_modules.GetSelection()
        if item.IsOk():
            bom_module = self.tree_bom_modules_manager.ItemToObject(item).bom_module
            
            self.bom.RemovePartModule(bom_module)
            
            self.loadBomModules()
            self.loadModules()

    def onButtonAddBomPartClick( self, event ):
        dropdown = DropdownDialog(self.button_add_bom_part, SelectPartFrame, "")
        dropdown.panel.Bind( EVT_SELECT_PART_OK_EVENT, self.onSelectPartCallback )
        dropdown.Dropdown()
    
    def onButtonRemoveBomPartClick( self, event ):
        item = self.tree_bom_parts.GetSelection()
        if item.IsOk():
            bom_part = self.tree_bom_parts_manager.ItemToObject(item).bom_part
            self.bom.RemovePart(bom_part)

            self.load()
        
    def onSelectPartCallback(self, part_event):
        if self.bom.ExistPart(part_event.data)==True:
            wx.MessageDialog(self, "%s already added, skipped" % part_event.data.name, "Error adding part", wx.OK | wx.ICON_ERROR).ShowModal()
            return
        
        self.bom.AddPart(part_event.data)
        # refresh
        self.loadBomParts()
        self.loadBomModules()

        for data in self.tree_bom_parts_manager.data:
            if data.bom_part.id==part_event.data.id:
                self.tree_bom_parts.Select(self.tree_bom_parts_manager.ObjectToItem(data))

    def onTreeBomPartsSelectionChanged( self, event ):
        item = self.tree_bom_parts.GetSelection()
        if item.IsOk():
            self.loadBomModules()
    
    def get_project_name(self, file):
        return os.path.splitext(os.path.basename(file))[0]
    
    def get_project_path(self, file):
        return os.path.dirname(file)
    
    def onToolOpenBrdClicked( self, event ):
        if self.bom.saved==False:
            res = wx.MessageDialog(self, "%s modified, save it?" % self.bom.filename, "File not saved", wx.YES_NO | wx.ICON_QUESTION).ShowModal()
            if res == wx.ID_YES:
                self.onToolSaveBomClicked(event)
    
        dlg = wx.FileDialog(
            self, message="Choose a Kicad PCB file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard="Kicad PCB (*.kicad_pcb)|*.kicad_pcb",
                style=wx.FD_OPEN | wx.FD_MULTIPLE |
                wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                wx.FD_PREVIEW
        )
        dlg.SetFilterIndex(0)

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            pcb = Pcb()
            if pcb.LoadFile(dlg.GetPath())==False:
                wx.MessageDialog(self, "Error", "Error opening %s"%dlg.GetPath(), wx.OK | wx.ICON_ERROR).ShowModal()
                return
            self.enableBrd(True)
            
            self.bom = Bom()
            self.bom.pcb = pcb
            
            # open BOM
            bom_filename = os.path.join(self.get_project_path(dlg.GetPath()), self.get_project_name(dlg.GetPath())+".bom")
            if(os.path.isfile(bom_filename)==False):
                # by default open bom with same name as board
                self.bom.SaveFile(bom_filename)
                self.enableBom(True)
            else:
                # if it does not exists create it
                self.bom.LoadFile(bom_filename)
                self.enableBom(True)
            self.load()

    def onToolOpenBomClicked( self, event ):
        if self.bom.saved==False:
            res = wx.MessageDialog(self, "%s modified, save it?" % self.bom.filename, "File not saved", wx.YES_NO | wx.ICON_QUESTION).ShowModal()
            if res==wx.ID_YES:
                self.onToolSaveBomClicked(event)

        dlg = wx.FileDialog(
            self, message="Choose a Kipartman BOM file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard="Kipartman BOM (*.bom)|*.bom",
                style=wx.FD_OPEN | wx.FD_MULTIPLE |
                wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                wx.FD_PREVIEW
        )
        dlg.SetFilterIndex(0)

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            self.bom.LoadFile(dlg.GetPath())
            self.load()
            self.enableBom(True)
    
    def onToolSaveBomClicked( self, event ):
#         if self.bom.filename==None and self.bom.saved==False:
#             filename = ''
#             path = os.getcwd()
#             if self.bom.pcb.filename!=None:
#                 filename = os.path.basename(pcb.filename.replace('kicad_pcb', 'bom'))
#                 path = os.path.dirname(pcb.filename)
#     
#             dlg = wx.FileDialog(
#                 self, message="Save a Kiparman BOM file",
#                 defaultDir=path,
#                 defaultFile=filename,
#                 wildcard="Kipartman BOM (*.bom)|*.bom",
#                     style=wx.FD_SAVE | wx.FD_CHANGE_DIR
#             )
#             dlg.SetFilterIndex(0)
#             
#             # Show the dialog and retrieve the user response. If it is the OK response,
#             # process the data.
#             if dlg.ShowModal() == wx.ID_OK:
#                 try:
#                     filename = dlg.GetPath()
#                     if filename[-4:]!='.bom':
#                         filename = filename+'.bom'
#                     bom.SaveFile(filename)
#                 except:
#                     pass
#        elif bom.saved==False:
        self.bom.Save()

    def onToolRefreshBrd( self, event ):
        self.load()
    
