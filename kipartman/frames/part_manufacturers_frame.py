from dialogs.panel_part_manufacturers import PanelPartManufacturers
from frames.edit_part_manufacturer_frame import EditPartManufacturerFrame
import helper.tree

class PartManufacturer(helper.tree.TreeContainerItem):
    def __init__(self, manufacturer):
        super(PartManufacturer, self).__init__()
        self.manufacturer = manufacturer

    def GetValue(self, col):
        if col==0:
            return self.manufacturer.manufacturer.name
        elif col==1:
            return self.manufacturer.part_name

        return ""

class TreeManagerPartManufacturer(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerPartManufacturer, self).__init__(tree_view, *args, **kwargs)

        self.part = None
        
        self.AddTextColumn("manufacturer")
        self.AddTextColumn("part name")
        
    def Load(self):
        
        self.SaveState()
        
        if self.part is not None:
            for manufacturer in self.part.manufacturers.all():
                manufacturerobj = self.FindManufacturer(manufacturer)
                if manufacturerobj is None:
                    manufacturerobj = PartManufacturer(manufacturer)
                    self.Append(None, manufacturerobj)
                else:
                    manufacturerobj.part_manufacturer = manufacturer
                    self.Update(manufacturerobj)

#             # add not yet persisted data
#             for parameter in self.part.parameters.pendings():
#                 parameterobj = self.FindParameter(parameter)
#                 if parameterobj is None:
#                     parameterobj = PartParameter(parameter.part, parameter)
#                     self.Append(None, parameterobj)
#                 else:
#                     parameterobj.part = self.part
#                     parameterobj.part_parameter = parameter
#                     self.Update(parameterobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Load()
        
    def FindManufacturer(self, manufacturer):
        for data in self.data:
            if isinstance(data, PartManufacturer) and data.manufacturer.id==manufacturer.id:
                return data
        return None

class PartManufacturersFrame(PanelPartManufacturers):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartManufacturersFrame, self).__init__(parent)

        # create octoparts list
        self.tree_manufacturers_manager = TreeManagerPartManufacturer(self.tree_manufacturers, context_menu=self.menu_manufacturers)
        self.tree_manufacturers_manager.OnItemBeforeContextMenu = self.onTreeManufacturersBeforeContextMenu

        self.tree_manufacturers_manager.Clear()
        self.SetPart(None)

        self._enable(False)
        
    def SetPart(self, part):
        self.part = part
        self.tree_manufacturers_manager.SetPart(part)
        self._enable(False)
        
    def EditPart(self, part):
        self.part = part
        self.tree_manufacturers_manager.SetPart(part)
        self._enable(True)

    def _enable(self, enabled=True):
        self.enabled = enabled

    def Save(self, part):
        pass
            
    def onTreeManufacturersBeforeContextMenu( self, event ):
        self.menu_manufacturer_add_manufacturer.Enable(True)
        self.menu_manufacturer_edit_manufacturer.Enable(True)
        self.menu_manufacturer_remove_manufacturer.Enable(True)
        if len(self.tree_manufacturers.GetSelections())==0:
            self.menu_manufacturer_edit_manufacturer.Enable(False)
            self.menu_manufacturer_remove_manufacturer.Enable(False)
        if len(self.tree_manufacturers.GetSelections())>1:
            self.menu_manufacturer_edit_manufacturer.Enable(False)
        
        if self.enabled==False:
            self.menu_manufacturer_add_manufacturer.Enable(False)
            self.menu_manufacturer_edit_manufacturer.Enable(False)
            self.menu_manufacturer_remove_manufacturer.Enable(False)
            

    # Virtual event handlers, overide them in your derived class
    def onMenuManufacturerAddManufacturer( self, event ):
        manufacturer = EditPartManufacturerFrame(self).AddManufacturer(self.part)
        if manufacturer:
            if self.part.manufacturers is None:
                self.part.manufacturers = []
            self.part.manufacturers.append(manufacturer)
            self.tree_manufacturers_manager.AppendItem(None, PartManufacturer(manufacturer))

    def onMenuManufacturerEditManufacturer( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if not item.IsOk():
            return 
        manufacturerobj = self.tree_manufacturers_manager.ItemToObject(item)
        EditPartManufacturerFrame(self).EditManufacturer(self.part, manufacturerobj.manufacturer)
        self.tree_manufacturers_manager.UpdateItem(manufacturerobj)

    def onMenuManufacturerRemoveManufacturer( self, event ):
        manufacturers = []
        for item in self.tree_manufacturers.GetSelections():
            obj = self.tree_manufacturers_manager.ItemToObject(item)
            if isinstance(obj, PartManufacturer):
                manufacturers.append(obj)
        for manufacturerobj in manufacturers:
            self.part.manufacturers.remove(manufacturerobj.manufacturer)
            self.tree_manufacturers_manager.DeleteItem(None, manufacturerobj)

        