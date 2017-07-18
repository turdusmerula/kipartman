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
        self.tree_manufacturers_manager = helper.tree.TreeManager(self.tree_manufacturers)
        self.tree_manufacturers_manager.AddTextColumn("Manufacturer")
        self.tree_manufacturers_manager.AddTextColumn("Part Name")

        self.enable(False)
        
    def SetPart(self, part):
        self.part = part
        self.showManufacturers()

    def enable(self, enabled=True):
        self.button_add_manufacturer.Enabled = enabled
        self.button_edit_manufacturer.Enabled = enabled
        self.button_remove_manufacturer.Enabled = enabled

    def AddManufacturer(self, manufacturer):
        """
        Add a manufacturer to the part
        """
        # add manufacturer
        self.part.manufacturers.append(manufacturer)
        self.create_list.append(manufacturer)
        self._showManufacturers()

    def RemoveManufacturer(self, name):
        """
        Remove a manufacturer using its name
        """
        for manufacturer in self.part.manufacturers:
            if manufacturer.manufacturer and manufacturer.manufacturer.name==name:
                if manufacturer.id!=-1:
                    self.remove_list.append(manufacturer)
                    self.part.manufacturers.remove(manufacturer)
                    # remove it from update list if present
                    try:
                        # remove it if already exists
                        self.update_list.remove(manufacturer)
                    except:
                        pass
                else:
                    self.part.manufacturers.remove(manufacturer)
                    

    def showManufacturers(self):
        self.tree_manufacturers_manager.ClearItems()

        if self.part and self.part.manufacturers:
            for manufacturer in self.part.manufacturers:
                self.tree_manufacturers_manager.AppendItem(None, DataModelPartManufacturer(manufacturer))
            
    def onButtonAddManufacturerClick( self, event ):
        manufacturer = EditPartManufacturerFrame(self).AddManufacturer(self.part)
        if manufacturer:
            if self.part.manufacturers is None:
                self.part.manufacturers = []
            self.part.manufacturers.append(manufacturer)
            self.tree_manufacturers_manager.AppendItem(None, DataModelPartManufacturer(manufacturer))
             
    def onButtonEditManufacturerClick( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if not item.IsOk():
            return 
        manufacturerobj = self.tree_manufacturers_manager.ItemToObject(item)
        EditPartManufacturerFrame(self).EditManufacturer(self.part, manufacturerobj.manufacturer)
        self.tree_manufacturers_manager.UpdateItem(manufacturerobj)
    
    def onButtonRemoveManufacturerClick( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if not item:
            return
        manufacturerobj = self.tree_manufacturers_manager.ItemToObject(item)
        self.part.manufacturers.remove(manufacturerobj.manufacturer)
        self.tree_manufacturers_manager.DeleteItem(None, manufacturerobj)

        