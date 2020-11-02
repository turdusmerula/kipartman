from dialogs.panel_part_manufacturers import PanelPartManufacturers
from frames.edit_part_manufacturer_frame import EditPartManufacturerFrame
import helper.tree

class PartManufacturer(helper.tree.TreeContainerItem):
    def __init__(self, part_manufacturer):
        super(PartManufacturer, self).__init__()
        self.part_manufacturer = part_manufacturer

    def GetValue(self, col):
        if col==0:
            return self.part_manufacturer.manufacturer.name
        elif col==1:
            return self.part_manufacturer.part_name

        return ""

    def GetAttr(self, col, attr):
        res = False
        if self.part_manufacturer.id is None:
            attr.SetColour(helper.colors.GREEN_NEW_ITEM)
            res = True
        if self.part_manufacturer.removed_pending():
            attr.SetStrikethrough(True)
            res = True
        return res

class TreeManagerPartManufacturer(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerPartManufacturer, self).__init__(tree_view, *args, **kwargs)

        self.part = None
        
        self.AddTextColumn("manufacturer")
        self.AddTextColumn("part name")
        
    def Load(self):
        
        self.SaveState()
        
        if self.part is not None:
            for part_manufacturer in self.part.manufacturers.all():
                part_manufacturerobj = self.FindManufacturer(part_manufacturer)
                if part_manufacturerobj is None:
                    part_manufacturerobj = PartManufacturer(part_manufacturer)
                    self.Append(None, part_manufacturerobj)
                else:
                    # all() extracts from database, fields are not updated to avoid discarding changes
                    self.Update(part_manufacturerobj)

            # add not yet persisted data
            for part_manufacturer in self.part.manufacturers.pendings():
                part_manufacturerobj = self.FindManufacturer(part_manufacturer)
                if part_manufacturerobj is None:
                    part_manufacturerobj = PartManufacturer(part_manufacturer)
                    self.Append(None, part_manufacturerobj)
                else:
                    self.Update(part_manufacturerobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Load()
        
    def FindManufacturer(self, part_manufacturer):
        for data in self.data:
            if isinstance(data, PartManufacturer) and data.part_manufacturer.id==part_manufacturer.id:
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
        EditPartManufacturerFrame(self).AddManufacturer(self.part)
        self.tree_manufacturers_manager.Load()
            
    def onMenuManufacturerEditManufacturer( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if not item.IsOk():
            return 
        part_manufacturerobj = self.tree_manufacturers_manager.ItemToObject(item)
        EditPartManufacturerFrame(self).EditManufacturer(self.part, part_manufacturerobj.part_manufacturer)
        self.tree_manufacturers_manager.Load()

    def onMenuManufacturerRemoveManufacturer( self, event ):
        manufacturers = []
        for item in self.tree_manufacturers.GetSelections():
            obj = self.tree_manufacturers_manager.ItemToObject(item)
            if isinstance(obj, PartManufacturer):
                manufacturers.append(obj)
        for manufacturerobj in manufacturers:
            self.part.manufacturers.remove_pending(manufacturerobj.part_manufacturer)
        self.tree_manufacturers_manager.Load()
        