from dialogs.panel_part_manufacturers import PanelPartManufacturers
from frames.edit_part_manufacturer_frame import EditPartManufacturerFrame
from frames.dropdown_dialog import DropdownDialog
import wx.dataview
import api.queries
 
class PartManufacturersDataModel(wx.dataview.PyDataViewModel):
    def __init__(self, part):
        super(PartManufacturersDataModel, self).__init__()
        if part:
            self.data = part.manufacturers
        else:
            self.data = []
            
    def GetColumnCount(self):
        return 2

    def GetColumnType(self, col):
        mapper = { 
            0 : 'string',
            1 : 'string',
         }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for octopart in self.data:
                children.append(self.ObjectToItem(octopart))
            return len(self.data)
        return 0
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        if obj.manufacturer:
            manufacturer = obj.manufacturer.name
        else:
            manufacturer = ''
        vMap = { 
            0 : manufacturer,
            1 : str(obj.part_name),
        }
            
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        return False

#     def HasDefaultCompare(self):
#         return False
#     
#     def Compare(self, item1, item2, column, ascending):
        #TODO allow sort integer columns properly
            
class PartManufacturersFrame(PanelPartManufacturers):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartManufacturersFrame, self).__init__(parent)

        # create octoparts list
        self.manufacturers_model = PartManufacturersDataModel(None)
        self.tree_manufacturers.AssociateModel(self.manufacturers_model)
        # add default columns
        self.tree_manufacturers.AppendTextColumn("Manufacturer", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_manufacturers.AppendTextColumn("Part Name", 1, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_manufacturers.Columns:
            c.Sortable = True

        self.enable(False)
        
    def SetPart(self, part):
        # array of changes to apply
        self.create_list = []
        self.update_list = []
        self.remove_list = []

        self.part = part
        self._showManufacturers()

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
                    

    def _showManufacturers(self):
        # apply new filter and reload
        self.manufacturers_model.Cleared()
        self.manufacturers_model = PartManufacturersDataModel(self.part)
        self.tree_manufacturers.AssociateModel(self.manufacturers_model)
    
    def ApplyChanges(self, part):
        for manufacturer in self.remove_list:
            manufacturer.part = part
            api.queries.PartManufacturersQuery().delete(manufacturer)
        self.remove_list = []

        # apply changes to current part
        for manufacturer in self.create_list:
            manufacturer.part = part
            api.queries.PartManufacturersQuery().create(manufacturer)
        self.create_list = []
        
        for manufacturer in self.update_list:
            manufacturer.part = part
            api.queries.PartManufacturersQuery().update(manufacturer)
        self.update_list = []
        
    def onButtonAddManufacturerClick( self, event ):
        manufacturer = EditPartManufacturerFrame(self).AddManufacturer(self.part)
        if not manufacturer is None:
            self.part.manufacturers.append(manufacturer)
            self.create_list.append(manufacturer)
        self._showManufacturers()
             
    def onButtonEditManufacturerClick( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if item is None:
            return 
        manufacturer = self.manufacturers_model.ItemToObject(item)
        if not manufacturer:
            return 
        if EditPartManufacturerFrame(self).EditManufacturer(self.part, manufacturer) and manufacturer.id!=-1:
            # set manufacturer to be updated
            try:
                # remove it from update list to avoid multiple update
                self.update_list.remove(manufacturer)
            except:
                pass
            self.update_list.append(manufacturer)
        self._showManufacturers()
    
    def onButtonRemoveManufacturerClick( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if not item:
            return
        manufacturer = self.manufacturers_model.ItemToObject(item)
        self.part.manufacturers.remove(manufacturer)
        # set manufacturer to be removed
        if manufacturer.id!=-1:
            self.remove_list.append(manufacturer)
            try:
                # remove it from update list if present
                self.update_list.remove(manufacturer)
            except:
                pass

        self._showManufacturers()
