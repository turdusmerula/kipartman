from dialogs.panel_part_manufacturers import PanelPartManufacturers
from frames.edit_part_manufacturer_frame import EditPartManufacturerFrame
import helper.tree

class DataModelPartManufacturer(helper.tree.TreeContainerItem):
    def __init__(self, manufacturer):
        super(DataModelPartManufacturer, self).__init__()
        self.manufacturer = manufacturer

    def GetValue(self, col):
        vMap = { 
            0 : self.manufacturer.name,
            1 : self.manufacturer.part_name,
        }
        return vMap[col]

    def IsContainer(self):
        return False

            
class PartManufacturersFrame(PanelPartManufacturers):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartManufacturersFrame, self).__init__(parent)

        # create octoparts list
        self.tree_manufacturers_manager = helper.tree.TreeManager(self.tree_manufacturers, context_menu=self.menu_manufacturers)
        self.tree_manufacturers_manager.AddTextColumn("Manufacturer")
        self.tree_manufacturers_manager.AddTextColumn("Part Name")
        self.tree_manufacturers_manager.OnItemBeforeContextMenu = self.onTreeManufacturersBeforeContextMenu

        self.enable(False)
        
    def SetPart(self, part):
        self.part = part
        self.showManufacturers()

    def enable(self, enabled=True):
        self.enabled = enabled

    def FindManufacturer(self, name):
        for data in self.tree_manufacturers_manager.data:
            if data.manufacturer.name==name:
                return data
        return None

    def AddManufacturer(self, manufacturer):
        """
        Add a manufacturer to the part
        """
        if self.part.manufacturers is None:
            self.part.manufacturers = []
        # add manufacturer
        self.part.manufacturers.append(manufacturer)
        self.tree_manufacturers_manager.AppendItem(None, DataModelPartManufacturer(manufacturer))

    def RemoveManufacturer(self, name):
        """
        Remove a manufacturer using its name
        """
        if self.part.manufacturers is None or len(self.part.manufacturers) == 0:
            return
        manufacturerobj = self.FindManufacturer(name)
        self.part.manufacturers.remove(manufacturerobj)
        self.tree_manufacturers_manager.DeleteItem(None, manufacturerobj)

    def showManufacturers(self):
        self.tree_manufacturers_manager.ClearItems()

        if self.part and self.part.manufacturers:
            for manufacturer in self.part.manufacturers:
                self.tree_manufacturers_manager.AppendItem(None, DataModelPartManufacturer(manufacturer))
            
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
            self.tree_manufacturers_manager.AppendItem(None, DataModelPartManufacturer(manufacturer))

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
            if isinstance(obj, DataModelPartManufacturer):
                manufacturers.append(obj)
        for manufacturerobj in manufacturers:
            self.part.manufacturers.remove(manufacturerobj.manufacturer)
            self.tree_manufacturers_manager.DeleteItem(None, manufacturerobj)

        