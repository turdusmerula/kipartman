from dialogs.panel_distributors import PanelDistributors
from api.queries import DistributorsQuery
from rest_client.exceptions import QueryError
import wx
import api.models

class DistributorsFrame(PanelDistributors): 
    def __init__(self, parent):
        super(DistributorsFrame, self).__init__(parent)
        
        self.panel_edit_distributor.Enabled = False
        self.panel_distributors.Enabled = True
        
        self.load() 
        
    def _loadDistributors(self):
        self.tree_distributors.DeleteAllItems()
        
        # root node
        self.tree_distributors.AddRoot('root')

        # retrieve categories
        distributors = DistributorsQuery().get()

        for distributor in distributors:
            newitem = self.tree_distributors.AppendItem(parent=self.tree_distributors.GetRootItem(), text=distributor.name)
            self.tree_distributors.SetItemData(newitem, distributor)
        
        #self.footprint_categories_tree.sort()
    
    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self._loadDistributors()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def ShowDistributor(self, distributor):
        self.distributor = distributor
        
        if distributor:
            self.edit_distributor_name.Value = distributor.name
            self.edit_distributor_address.Value = distributor.address
            self.edit_distributor_website.Value = distributor.website
            self.edit_distributor_sku_url.Value = distributor.sku_url
            self.edit_distributor_email.Value = distributor.email
            self.edit_distributor_phone.Value = distributor.phone
            self.edit_distributor_comment.Value = distributor.comment
        else:
            self.edit_distributor_name.Value = ''
            self.edit_distributor_address.Value = ''
            self.edit_distributor_website.Value = ''
            self.edit_distributor_sku_url.Value = ''
            self.edit_distributor_email.Value = ''
            self.edit_distributor_phone.Value = ''
            self.edit_distributor_comment.Value = ''

    def onButtonAddDistributorClick( self, event ):
        self.ShowDistributor(None)
        self.panel_edit_distributor.Enabled = True
        self.panel_distributors.Enabled = False

    def onButtonEditDistributorClick( self, event ):
        item = self.tree_distributors.GetSelection()
        distributors = self.tree_distributors.GetItemData(item)
        self.ShowDistributor(distributors)
        
        self.panel_edit_distributor.Enabled = True
        self.panel_distributors.Enabled = False

    def onButtonRemoveDistributorClick( self, event ):
        item = self.tree_distributors.GetSelection()
        distributor = self.tree_distributors.GetItemData(item)
        DistributorsQuery().delete(distributor)
        self.load()
        
    def onButtonRefreshDistributorsClick( self, event ):
        self.load()
    
    def onTreeDistributorsSelChanged( self, event ):
        item = self.tree_distributors.GetSelection()
        distributor = self.tree_distributors.GetItemData(item)
        self.ShowDistributor(distributor)
    
    def onApplyButtonClick( self, event ):
        
        if self.distributor is None:
            distributor = api.models.Distributor()
        else:
            distributor = self.distributor
        
        distributor.name = self.edit_distributor_name.Value
        distributor.address = self.edit_distributor_address.Value
        distributor.website = self.edit_distributor_website.Value
        distributor.sku_url = self.edit_distributor_sku_url.Value
        distributor.email = self.edit_distributor_email.Value
        distributor.phone = self.edit_distributor_phone.Value
        distributor.comment = self.edit_distributor_comment.Value

        try:
            if self.distributor is None:
                distributor = DistributorsQuery().create(distributor)
            else:
                distributor = DistributorsQuery().update(distributor)
            
            self. load()
            self.panel_edit_distributor.Enabled = False
            self.panel_distributors.Enabled = True
            
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        
    def onCancelButtonClick( self, event ):
        self.panel_edit_distributor.Enabled = False
        self.panel_distributors.Enabled = True

