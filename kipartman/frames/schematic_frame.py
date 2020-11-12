from dialogs.panel_schematic import PanelSchematic
from frames.dropdown_dialog import DropdownDialog
from frames.select_part_frame import SelectPartFrame, EVT_SELECT_PART_OK_EVENT
import helper.tree
from kicad.kicad_schematic_file import KicadSchematicFile, KicadComp, KicadSheet, KicadAR
from frames.part_preview_data_frame import PartPreviewDataFrame
from kicad.kicad_file_manager import KicadFileManager
import wx
import re
import os
# from frames.part_parameters_frame import PartParameter
from bom.bom import Bom
from helper.exception import print_stack
from helper.unit import format_unit_prefix
from time import time
from helper.log import log

class Sheet(helper.tree.TreeContainerItem):
    def __init__(self, schematic, sheet):
        super(Sheet, self).__init__()
        self.schematic = schematic
        self.sheet = sheet
        
    def GetValue(self, col):
        if col==0:
            return self.sheet.fget_file()
        
        return "-"

class Part(helper.tree.TreeContainerItem):
    def __init__(self, schematic, component):
        super(Part, self).__init__()
        self.schematic = schematic
        self.component = component
        
    def GetValue(self, col):
        if col==0:
            return self.schematic.objects.get_timestamp_path(self.component.timestamp)
        elif col==1:
            if self.childs is None or len(self.childs)==0:
                return self.component.reference
            return '<'+str(len(self.childs))+' instances>'
        elif col==2:
            return self.component.value
        elif col==3:
            return self.component.kipart_sku
        elif col==4:
            return self.component.symbol
        elif col==5:
            return self.component.footprint
        elif col==6:
            return self.component.kipart_id
        elif col==7:
            return self.component.timestamp
        
        return "-"

class Instance(helper.tree.TreeItem):
    def __init__(self, schematic, component, instance):
        super(Instance, self).__init__()
        self.schematic = schematic
        self.component = component
        self.instance = instance
        
    def GetValue(self, col):
        if col==0:
            return self.schematic.objects.get_timestamp_path(self.instance.timestamp)
        elif col==1:
            return self.instance.reference
        elif col==2:
            return self.component.value
        elif col==3:
            return self.component.kipart_sku
        elif col==4:
            return self.component.symbol
        elif col==5:
            return self.component.footprint
        elif col==6:
            return self.component.kipart_id
        elif col==7:
            return self.instance.timestamp

        return "-"

class TreeManagerParts(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerParts, self).__init__(tree_view, *args, **kwargs)
        
        self.schematic = None
        
        self.AddTextColumn("Path")
        self.AddTextColumn("Reference")
        self.AddTextColumn("Value")
        self.AddTextColumn("Part")
        self.AddTextColumn("Symbol")
        self.AddTextColumn("Footprint")
        self.AddIntegerColumn("id")
        self.AddTextColumn("Timestamp")
        
    def Load(self):
        
        self.SaveState()

        if self.schematic is not None:
            
            self._load_nodes(None, self.schematic.parent.nodes)
            
            for sheet in self.schematic.objects.sheets:
                sheetobj = self.FindSheet(sheet)
                if sheetobj is None:
                    sheetobj = Sheet(self.schematic, sheet)
                    self.Append(None, sheetobj)
                else:
                    sheetobj.schematic = self.schematic
                    sheetobj.sheet = sheet
                    self.Update(sheetobj)
            
                if sheet.schematic is not None:
                    self._load_nodes(sheetobj, sheet.schematic.parent.nodes)
                
        self.PurgeState()

    def _load_nodes(self, sheetobj, nodes):
        sheet_timestamps = self.schematic.SheetTimetamps()
        
        for obj in nodes:
            if isinstance(obj, KicadComp):
                partobj = self.FindPart(obj)
                if partobj is None:
                    partobj = Part(self.schematic, obj)
                    self.Append(sheetobj, partobj)
                else:
                    partobj.schematic = self.schematic
                    partobj.component = obj
                    self.Update(partobj)
                
                for instobj in obj.nodes:
                    if isinstance(instobj, KicadAR):
                        sheet_timestamp = "/".join(instobj.timestamp.split('/')[:-1])
                        if sheet_timestamp in sheet_timestamps:
                            instanceobj = self.FindInstance(instobj)
                            if instanceobj is None:
                                instanceobj = Instance(self.schematic, obj, instobj)
                                self.Append(partobj, instanceobj)
                            else:
                                instanceobj.schematic = self.schematic
                                instanceobj.component = obj
                                instanceobj.instance = instobj
                                self.Update(instanceobj)
                        else:
                            print(f"Ignored {instobj.timestamp}")
                            
    def SetSchematic(self, schematic):
        self.schematic = schematic
        self.Clear()
        self.Load()

    def FindPart(self, component):
        for data in self.data:
            if isinstance(data, Part) and data.component.timestamp==component.timestamp:
                return data
        return None

    def FindInstance(self, instance):
        for data in self.data:
            if isinstance(data, Instance) and data.instance.timestamp==instance.timestamp:
                return data
        return None

    def FindSheet(self, sheet):
        for data in self.data:
            if isinstance(data, Sheet) and data.sheet.fget_file()==sheet.fget_file():
                return data
        return None

class SchematicFrame(PanelSchematic): 
    def __init__(self, parent, file):
        super(SchematicFrame, self).__init__(parent)
        
        # create module list
        self.tree_parts_manager = TreeManagerParts(self.tree_parts, context_menu=self.menu_parts)
        self.tree_parts_manager.OnSelectionChanged = self.onTreePartsSelChanged
        self.tree_parts_manager.OnItemBeforeContextMenu = self.onTreePartsBeforeContextMenu

        self.file = file
        self.schematic = KicadSchematicFile()
        self.file_manager = KicadFileManager(os.path.dirname(self.file))

        self.data_frame = PartPreviewDataFrame(self.panel_preview)
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.panel_preview.SetSizer( sizer )
        sizer.Fit( self.panel_preview )
        sizer.Add(self.data_frame, 0, wx.ALL|wx.EXPAND, 0)
        self.panel_preview.Layout()

        # used to know if reload dialog is already shown
        self.has_reload_dialog = False
        
        self._load_schematic()
        self.tree_parts_manager.SetSchematic(self.schematic)

    def activate(self):
        pass
    
    def GetMenus(self):
        return None
    
#     def load(self):
#         self.loadSchematic()
#     
#     def loadParts(self):
#         # load one time to improve performances
#         self.parts = rest.api.find_parts(with_parameters=True)
#         
    def _load_schematic(self):
        self.schematic.LoadFile(self.file)
        # TODO add file watchdog
        self.schematic.DebugWrite(self.schematic.parent)

#         # load parts
#         print("---", self.schematic.Components())
#         for comp in self.schematic.Components():
#             component = comp[0]
#             instance = comp[1]
#             if component.kipart_id!='':
#                 part_id = int(component.kipart_id)
#                 part = None
#                 for p in self.parts:
#                     if p.id==part_id:
#                         part = p
#                         break
#                 if part:
#                     self.associate_part(component, part)
 
#         self.schematic.Save()
#  
#         self.tree_parts_manager.SaveState()
#          
#         # load schematic parts
#         for comp in self.schematic.Components():
#             component = comp[0]
#             instance = comp[1]
#  
#             partobj = self.tree_parts_manager.FindPart(component)
#             if partobj:
#                 partobj.component = component
#  
#             show = True
#             if self.tool_show_all.IsToggled() and 'hidden' in component.kipart_status:
#                 show = False
#  
#             if show==False:
#                 try:
#                     self.tree_parts_manager.DeleteItem(None, partobj)
#                 except:
#                     pass
#              
#             if self.tree_parts_manager.DropStateObject(partobj)==False and partobj is None:
#                 if show==True:
#                     self.tree_parts_manager.AppendPart(self.schematic, component)
#  
#             instanceobj = None
#             if instance:
#                 instanceobj = self.tree_parts_manager.FindInstance(instance)
#                 if instanceobj:
#                     instanceobj.component = component
#                     instanceobj.instance = instance
#              
#             if self.tree_parts_manager.DropStateObject(instanceobj)==False and instance and instanceobj is None:
#                 if show==True:
#                     self.tree_parts_manager.AppendInstance(self.schematic, component, instance)
#  
#         self.tree_parts_manager.PurgeState()

#     def reload(self):
#         if self.has_reload_dialog:
#             # reload dialog already pending
#             return
# 
#         if self.schematic and self.schematic.Modified():
#             self.has_reload_dialog = True
#             res = wx.MessageDialog(self, "%s modified, reload it?" % self.file, "File changed", wx.YES_NO | wx.ICON_QUESTION).ShowModal()
#             if res == wx.ID_YES:
#                 self.loadParts()
#                 self.load()
#             self.has_reload_dialog = False
#     
    def onTreePartsBeforeContextMenu( self, event ):
#         item = self.tree_parts.GetSelection()
#         if item.IsOk()==False:
#             return    
#         obj = self.tree_parts_manager.ItemToObject(item)
# 
#         self.menu_parts_link.Enable(True)
#         self.menu_parts_unlink.Enable(True)
#         self.menu_parts_hide.Enable(True)
#         self.menu_parts_show.Enable(True)
#         self.menu_parts_remove_instance.Enable(True)
#         if isinstance(obj, Part):
#             self.menu_parts_remove_instance.Enable(False)
#         else:
#             self.menu_parts_link.Enable(False)
#             self.menu_parts_unlink.Enable(False)
#             self.menu_parts_hide.Enable(False)
#             self.menu_parts_show.Enable(False)
        event.Skip()
         
    def onToolRefreshSchematic( self, event ):
        self._load_schematic()
        self.tree_parts_manager.Load()

    def onTreePartsSelChanged( self, event ):
#         self.data_frame.SetPart(None)
#         if len(self.tree_parts.GetSelections())>1:
#             return
#         item = self.tree_parts.GetSelection()
#         if item.IsOk():
#             partobj = self.tree_parts_manager.ItemToObject(item)
#             part = None            
#             try:
#                 if partobj.component.kipart_id!='': 
#                     part = rest.api.find_part(partobj.component.kipart_id)
#             except Exception as e:
#                 print_stack()
#                 log.error(format(e))
#             self.data_frame.SetPart(part)
        event.Skip()
        
#     def onMenuPartsLinkSelection( self, event ):
#         dropdown = DropdownDialog(self.tree_parts, SelectPartFrame, "")
#         dropdown.panel.Bind( EVT_SELECT_PART_OK_EVENT, self.onSelectPartCallback )
#         dropdown.Dropdown()
# 
#     def get_symbol(self, path):
#         return re.sub(r".*\.lib/", "", path).replace(".mod", "")
#     
#     def get_footprint(self, path):
#         lib = os.path.basename(os.path.dirname(path)).replace(".pretty", "")
#         footprint = os.path.basename(path).replace(".kicad_mod", "")
#         return lib+":"+footprint
#     
#     def associate_part(self, component, part):
#         symbol = None
#         if part.symbol:
#             unit_symbol = self.get_symbol(part.symbol.source_path)
#             
#         footprint = None
#         if part.footprint:
#             footprint = self.get_footprint(part.footprint.source_path)
#         
#         if symbol:
#             component.symbol = symbol
#         if footprint:
#             component.footprint = footprint
#         if part.value_parameter:
#             for parameter in part.parameters:
#                 if parameter.name==part.value_parameter:
#                     if parameter.nom_value:
#                         unit = ''
#                         if parameter.unit:
#                             unit = parameter.unit.symbol
#                         component.value = format_unit_prefix(parameter.nom_value, unit)
#                     else:
#                         component.value = ''
#         
#         component.kipart_id = str(part.id)
#         component.kipart_sku = str(part.name)
#     
#     def onSelectPartCallback(self, part_event):
#         part = part_event.data
#         
#         items = self.tree_parts.GetSelections()
#         if items:
#             for item in items:
#                 partobj = self.tree_parts_manager.ItemToObject(item)
#                 self.associate_part(partobj.component, part)
#                     
#         self.schematic.Save()
# 
#         self.load()
# 
#     def onToolExportBomClicked( self, event ):
#         path = os.getcwd()
#         dlg = wx.FileDialog(
#             self, message="Save a bom file",
#             defaultDir=os.path.dirname(os.path.abspath(self.file)),
#             defaultFile=re.sub('\..*', '.bom', os.path.basename(os.path.abspath(self.file))),
#             wildcard="Kipartman bom (*.bom)|*.bom",
#                 style=wx.FD_SAVE | wx.FD_CHANGE_DIR
#         )
#         dlg.SetFilterIndex(0)
#         if dlg.ShowModal() == wx.ID_OK:
#             filename = dlg.GetPath()
#             
#             bom = Bom()            
#             try:
#                 bom.SetSchematic(self.file)
#                 bom.SaveFile(filename)
#             except Exception as e:
#                 print_stack()
#                 wx.MessageBox(format(e), 'Error saving %s'%filename, wx.OK | wx.ICON_ERROR)
# 
#     
#     def onMenuPartsUnlinkSelection( self, event ):
#         items = self.tree_parts.GetSelections()
#         if items:
#             for item in items:
#                 partobj = self.tree_parts_manager.ItemToObject(item)
#                 component = partobj.component
#                 component.kipart_id = ''
#                 component.kipart_sku = ''
#         self.load()
# 
#     def onMenuPartsHideSelection( self, event ):
#         items = self.tree_parts.GetSelections()
#         if items:
#             for item in items:
#                 partobj = self.tree_parts_manager.ItemToObject(item)
#                 component = partobj.component
#                 component.kipart_status = 'hidden'
#         self.schematic.Save()
#         self.load()
#     
#     def onMenuPartsShowSelection( self, event ):
#         items = self.tree_parts.GetSelections()
#         if items:
#             for item in items:
#                 partobj = self.tree_parts_manager.ItemToObject(item)
#                 component = partobj.component
#                 component.kipart_status = ''
#         self.schematic.Save()
#         self.load()
# 
#     def onToolShowAllClicked( self, event ):
#         self.load()
