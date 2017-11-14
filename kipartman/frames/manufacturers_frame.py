from dialogs.panel_manufacturers import PanelManufacturers
import wx
import rest
import helper.tree

def NoneValue(value, default):
    if value:
        return value
    return default

class DataModelManufacturer(helper.tree.TreeItem):
    def __init__(self, manufacturer):
        super(DataModelManufacturer, self).__init__()
        self.manufacturer = manufacturer
            
    def GetValue(self, col):
        vMap = { 
            0 : self.manufacturer.name,
        }
        return vMap[col]


class TreeManagerManufacturers(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerManufacturers, self).__init__(tree_view)

    def FindManufacturer(self, manufacturer_id):
        for data in self.data:
            if isinstance(data, DataModelManufacturer) and data.manufacturer.id==manufacturer_id:
                return data
        return None

    def UpdateManufacturer(self, manufacturer):
        manufacturerobj = self.FindManufacturer(manufacturer.id)
        if manufacturerobj is None:
            return
        self.UpdateItem(manufacturerobj)


class ManufacturersFrame(PanelManufacturers): 
    def __init__(self, parent):
        super(ManufacturersFrame, self).__init__(parent)
        
        # create manufacturers list
        self.tree_manufacturers_manager = TreeManagerManufacturers(self.tree_manufacturers)
        self.tree_manufacturers_manager.AddTextColumn("name")
        self.tree_manufacturers_manager.OnSelectionChanged = self.onTreeManufacturersSelChanged

        self.panel_edit_manufacturer.Enabled = False
        self.panel_manufacturers.Enabled = True
        
        self.load() 
        
    def loadManufacturers(self):
        self.tree_manufacturers_manager.ClearItems()
        
        # retrieve categories
        manufacturers = rest.api.find_manufacturers()

        for manufacturer in manufacturers:
            self.tree_manufacturers_manager.AppendItem(None, DataModelManufacturer(manufacturer))
    
    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self.loadManufacturers()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def ShowManufacturer(self, manufacturer):
        self.manufacturer = manufacturer
        
        if manufacturer:
            self.edit_manufacturer_name.Value = NoneValue(manufacturer.name, '')
            self.edit_manufacturer_address.Value = NoneValue(manufacturer.address, '')
            self.edit_manufacturer_website.Value = NoneValue(manufacturer.website, '')
            self.edit_manufacturer_email.Value = NoneValue(manufacturer.email, '')
            self.edit_manufacturer_phone.Value = NoneValue(manufacturer.phone, '')
            self.edit_manufacturer_comment.Value = NoneValue(manufacturer.comment, '')
        else:
            self.edit_manufacturer_name.Value = ''
            self.edit_manufacturer_address.Value = ''
            self.edit_manufacturer_website.Value = ''
            self.edit_manufacturer_email.Value = ''
            self.edit_manufacturer_phone.Value = ''
            self.edit_manufacturer_comment.Value = ''

    def onButtonAddManufacturerClick( self, event ):
        self.ShowManufacturer(None)
        self.panel_edit_manufacturer.Enabled = True
        self.panel_manufacturers.Enabled = False

    def onButtonEditManufacturerClick( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if item.IsOk()==False:
            return 
        manufacturer = self.tree_manufacturers_manager.ItemToObject(item)
        self.ShowManufacturer(manufacturer.manufacturer)
        
        self.panel_edit_manufacturer.Enabled = True
        self.panel_manufacturers.Enabled = False

    def onButtonRemoveManufacturerClick( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if item.IsOk()==False:
            return
        manufacturer = self.tree_manufacturers_manager.ItemToObject(item)
        rest.api.delete_manufacturer(manufacturer.manufacturer.id)
        self.tree_manufacturers_manager.DeleteItem(None, manufacturer)
        
    def onButtonRefreshManufacturersClick( self, event ):
        self.load()
    
    def onTreeManufacturersSelChanged( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if item.IsOk()==False:
            return
        manufacturer = self.tree_manufacturers_manager.ItemToObject(item)
        self.ShowManufacturer(manufacturer.manufacturer)
    
    def onApplyButtonClick( self, event ):
        
        if self.manufacturer is None:
            manufacturer = rest.model.ManufacturerNew()
        else:
            manufacturer = self.manufacturer
        
        manufacturer.name = self.edit_manufacturer_name.Value
        manufacturer.address = self.edit_manufacturer_address.Value
        manufacturer.website = self.edit_manufacturer_website.Value
        manufacturer.email = self.edit_manufacturer_email.Value
        manufacturer.phone = self.edit_manufacturer_phone.Value
        manufacturer.comment = self.edit_manufacturer_comment.Value

        try:
            if self.manufacturer is None:
                manufacturer = rest.api.add_manufacturer(manufacturer)
                self.tree_manufacturers_manager.AppendItem(None, DataModelManufacturer(manufacturer))
            else:
                manufacturer = rest.api.update_manufacturer(manufacturer.id, manufacturer)
                self.tree_manufacturers_manager.UpdateManufacturer(manufacturer)

            self.panel_edit_manufacturer.Enabled = False
            self.panel_manufacturers.Enabled = True
            
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        
    def onCancelButtonClick( self, event ):
        self.panel_edit_manufacturer.Enabled = False
        self.panel_manufacturers.Enabled = True

