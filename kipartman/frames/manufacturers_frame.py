from dialogs.panel_manufacturers import PanelManufacturers
from api.queries import ManufacturersQuery
from rest_client.exceptions import QueryError
import wx
import api.models

class ManufacturersFrame(PanelManufacturers): 
    def __init__(self, parent):
        super(ManufacturersFrame, self).__init__(parent)
        
        self.panel_edit_manufacturer.Enabled = False
        self.panel_manufacturers.Enabled = True
        
        self.load() 
        
    def _loadManufacturers(self):
        self.tree_manufacturers.DeleteAllItems()
        
        # root node
        self.tree_manufacturers.AddRoot('root')

        # retrieve categories
        manufacturers = ManufacturersQuery().get()

        for manufacturer in manufacturers:
            newitem = self.tree_manufacturers.AppendItem(parent=self.tree_manufacturers.GetRootItem(), text=manufacturer.name)
            self.tree_manufacturers.SetItemData(newitem, manufacturer)
        
        #self.footprint_categories_tree.sort()
    
    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self._loadManufacturers()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def ShowManufacturer(self, manufacturer):
        self.manufacturer = manufacturer
        
        if manufacturer:
            self.edit_manufacturer_name.Value = manufacturer.name
            self.edit_manufacturer_address.Value = manufacturer.address
            self.edit_manufacturer_website.Value = manufacturer.website
            self.edit_manufacturer_email.Value = manufacturer.email
            self.edit_manufacturer_phone.Value = manufacturer.phone
            self.edit_manufacturer_comment.Value = manufacturer.comment
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
        manufacturers = self.tree_manufacturers.GetItemData(item)
        self.ShowManufacturer(manufacturers)
        
        self.panel_edit_manufacturer.Enabled = True
        self.panel_manufacturers.Enabled = False

    def onButtonRemoveManufacturerClick( self, event ):
        item = self.tree_manufacturers.GetSelection()
        manufacturer = self.tree_manufacturers.GetItemData(item)
        ManufacturersQuery().delete(manufacturer)
        self.load()
        
    def onButtonRefreshManufacturersClick( self, event ):
        self.load()
    
    def onTreeManufacturersSelChanged( self, event ):
        item = self.tree_manufacturers.GetSelection()
        manufacturer = self.tree_manufacturers.GetItemData(item)
        self.ShowManufacturer(manufacturer)
    
    def onApplyButtonClick( self, event ):
        
        if self.manufacturer is None:
            manufacturer = api.models.Manufacturer()
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
                manufacturer = ManufacturersQuery().create(manufacturer)
            else:
                manufacturer = ManufacturersQuery().update(manufacturer)
            
            self. load()
            self.panel_edit_manufacturer.Enabled = False
            self.panel_manufacturers.Enabled = True
            
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        
    def onCancelButtonClick( self, event ):
        self.panel_edit_manufacturer.Enabled = False
        self.panel_manufacturers.Enabled = True

