from dialogs.panel_bom import PanelBom
from frames.dropdown_dialog import DropdownDialog
from frames.select_part_frame import SelectPartFrame, EVT_SELECT_PART_OK_EVENT
from kicad.pcb import Pcb
from bom.bom import Bom
import wx.dataview
import os
from docutils.parsers.rst.directives import path

pcb = Pcb()
bom = Bom(pcb)

class ModuleModel(wx.dataview.PyDataViewModel):
    def __init__(self):
        super(ModuleModel, self).__init__()

        self.modules = pcb.GetModules()
        
    def GetColumnCount(self):
        return 2

    def GetColumnType(self, col):
        mapper = { 
            0 : 'string',
            1 : 'string',
            2 : 'string',
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        num = 0
        if not parent:
            for module in self.modules:
                if bom.module_part.has_key(module.timestamp)==False:    
                    children.append(self.ObjectToItem(module))
                    num = num + 1
            return num
        return 0
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)

        vMap = { 
            0 : obj.reference,
            1 : obj.value,
            2 : obj.footprint,
        }
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        if col == 0:
            attr.Bold = True
            return True
        return False


class BomPartsModel(wx.dataview.PyDataViewModel):
    def __init__(self):
        super(BomPartsModel, self).__init__()
    
        self.parts = bom.Parts()
        
    def GetColumnCount(self):
        return 4

    def GetColumnType(self, col):
        mapper = { 
            0 : 'long',
            1 : 'string',
            2 : 'string',
            3 : 'string',
            4 : 'long'
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for part in self.parts:
                children.append(self.ObjectToItem(part))
            return len(self.parts)
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        num_modules = 0
        if bom.part_modules.has_key(obj.id):
            num_modules = len(bom.part_modules[obj.id])
        vMap = { 
            0 : str(obj.id),
            1 : obj.name,
            2 : obj.description,
            3 : obj.comment,
            4 : str(num_modules)
        }
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        return False


class BomModulesModel(wx.dataview.PyDataViewModel):
    def __init__(self, part):
        super(BomModulesModel, self).__init__()
        self.part = part


    def GetColumnCount(self):
        return 4

    def GetColumnType(self, col):
        mapper = { 
            0 : 'string',
            1 : 'string',
            2 : 'string'
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        if self.part is None:
            return 0
        
        # check root node
        if not parent:
            for module in bom.part_modules[self.part.id]:
                children.append(self.ObjectToItem(module))
            return len(bom.part_modules[self.part.id])
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        vMap = { 
            0 : obj.reference,
            1 : obj.value,
            2 : obj.footprint
        }
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        return False


class BomFrame(PanelBom): 
    def __init__(self, parent):
        super(BomFrame, self).__init__(parent)

        # create module list
        self.module_model = ModuleModel()
        self.tree_modules.AssociateModel(self.module_model)
        # add default columns
        self.tree_modules.AppendTextColumn("Reference", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_modules.AppendTextColumn("Value", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_modules.AppendTextColumn("Footprint", 2, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_modules.Columns:
            c.Sortable = True
        
        # create bom parts list
        self.bom_parts_model = BomPartsModel()
        self.tree_bom_parts.AssociateModel(self.bom_parts_model)
        # add default columns
        self.tree_bom_parts.AppendTextColumn("Id", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_parts.AppendTextColumn("Name", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_parts.AppendTextColumn("Description", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_parts.AppendTextColumn("Comment", 3, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_parts.AppendTextColumn("Modules", 4, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_bom_parts.Columns:
            c.Sortable = True

        # create bom modules list
        self.bom_modules_model = BomModulesModel(None)
        self.tree_bom_modules.AssociateModel(self.bom_modules_model)
        # add default columns
        self.tree_bom_modules.AppendTextColumn("Reference", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_modules.AppendTextColumn("Value", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_modules.AppendTextColumn("Footprint", 2, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_bom_modules.Columns:
            c.Sortable = True

        self.enableBom(False)
        self.enableBrd(False)

    def load(self):
        self.loadModules()
        self.loadBomParts()
        self.loadBomModules()
    
    def loadModules(self):
        self.module_model.Cleared()
        self.module_model = ModuleModel()
        self.tree_modules.AssociateModel(self.module_model)
    
    def loadBomParts(self):
        self.bom_parts_model.Cleared()
        self.bom_parts_model = BomPartsModel()
        self.tree_bom_parts.AssociateModel(self.bom_parts_model)
    
    def loadBomModules(self):
        item = self.tree_bom_parts.GetSelection()
        part = None
        if item:
            part = self.bom_parts_model.ItemToObject(item)

        self.bom_modules_model.Cleared()
        self.bom_modules_model = BomModulesModel(part)
        self.tree_bom_modules.AssociateModel(self.bom_modules_model)
    
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
        if item:
            module = self.module_model.ItemToObject(item)
        else:
            return
        
        item = self.tree_bom_parts.GetSelection()
        if item:
            part = self.bom_parts_model.ItemToObject(item)
            bom.AddModule(part, module)

            self.loadBomModules()
            self.loadModules()

    def onButtonRemoveBomModuleClick( self, event ):
        item = self.tree_bom_modules.GetSelection()
        if item:
            bom_module = self.bom_modules_model.ItemToObject(item)
            
            bom.RemoveModule(bom_module)
            
            self.loadBomModules()
            self.loadModules()

    def onButtonAddBomPartClick( self, event ):
        dropdown = DropdownDialog(self.button_add_bom_part, SelectPartFrame, "")
        dropdown.panel.Bind( EVT_SELECT_PART_OK_EVENT, self.onSelectPartCallback )
        dropdown.Dropdown()
    
    def onButtonRemoveBomPartClick( self, event ):
        item = self.tree_bom_parts.GetSelection()
        if item:
            part = self.bom_parts_model.ItemToObject(item)
            bom.RemovePart(part)

            self.load()
        
    def onSelectPartCallback(self, part):
        if bom.ExistPart(part.data)==True:
            wx.MessageDialog(self, "%s already added, skipped" % part.data.name, "Error adding part", wx.OK | wx.ICON_ERROR).ShowModal()
            return
        
        bom.AddPart(part.data)
        # refresh
        self.loadBomParts()
        self.loadBomModules()
         
    def onTreeBomPartsSelectionChanged( self, event ):
        item = self.tree_bom_parts.GetSelection()
        if item:
            part = self.bom_parts_model.ItemToObject(item)
            
            self.loadBomModules()
    
    def onToolOpenBrdClicked( self, event ):
        if bom.saved==False:
            res = wx.MessageDialog(self, "%s modified, save it?" % bom.filename, "File not saved", wx.YES_NO | wx.ICON_QUESTION).ShowModal()
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
            pcb_filename = dlg.GetPath()
            pcb.LoadFile(pcb_filename)
            self.enableBrd(True)
            
            # open BOM
            bom_filename = pcb_filename.replace('kicad_pcb', 'bom')
            if(os.path.isfile(bom_filename)==False):
                bom_filename = None
                self.enableBom(False)
            else:
                bom.LoadFile(bom_filename)
                self.enableBom(True)
            self.load()

    def onToolOpenBomClicked( self, event ):
        if bom.saved==False:
            res = wx.MessageDialog(self, "%s modified, save it?" % bom.filename, "File not saved", wx.YES_NO | wx.ICON_QUESTION).ShowModal()
            print res
            if res==wx.ID_YES:
                print "-----"
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
            bom.LoadFile(dlg.GetPath())
            self.load()
            self.enableBom(True)
    
    def onToolSaveBomClicked( self, event ):
        if bom.filename==None and bom.saved==False:
            filename = ''
            path = os.getcwd()
            if pcb.filename!=None:
                filename = os.path.basename(pcb.filename.replace('kicad_pcb', 'bom'))
                path = os.path.dirname(pcb.filename)
    
            dlg = wx.FileDialog(
                self, message="Save a Kiparman BOM file",
                defaultDir=path,
                defaultFile=filename,
                wildcard="Kipartman BOM (*.bom)|*.bom",
                    style=wx.FD_SAVE | wx.FD_CHANGE_DIR
            )
            dlg.SetFilterIndex(0)
            
            # Show the dialog and retrieve the user response. If it is the OK response,
            # process the data.
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    filename = dlg.GetPath()
                    if filename[-4:]!='.bom':
                        filename = filename+'.bom'
                    bom.SaveFile(filename)
                except:
                    pass
        elif bom.saved==False:
            bom.Save()

    def onToolRefreshBrd( self, event ):
        self.load()
    
