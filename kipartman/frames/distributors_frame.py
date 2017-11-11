from dialogs.panel_distributors import PanelDistributors
import wx
import rest
import helper.tree

def NoneValue(value, default):
    if value:
        return value
    return default

class DataModelDistributor(helper.tree.TreeItem):
    def __init__(self, distributor):
        super(DataModelDistributor, self).__init__()
        self.distributor = distributor
            
    def GetValue(self, col):
        vMap = { 
            0 : self.distributor.allowed,
            1 : self.distributor.name,
        }
        return vMap[col]

    def SetValue(self, value, col):
        if col==0:
            self.distributor.allowed = value
            self.distributor = rest.api.update_distributor(self.distributor.id, self.distributor)
            return True
        return False

class TreeManagerDistributors(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerDistributors, self).__init__(tree_view)

    def FindDistributor(self, distributor_id):
        for data in self.data:
            if isinstance(data, DataModelDistributor) and data.distributor.id==distributor_id:
                return data
        return None

    def UpdateDistributor(self, distributor):
        distributorobj = self.FindDistributor(distributor.id)
        if distributorobj is None:
            return
        self.UpdateItem(distributorobj)

class DistributorsFrame(PanelDistributors): 
    def __init__(self, parent):
        super(DistributorsFrame, self).__init__(parent)
        
        # create distributors list
        self.tree_distributors_manager = TreeManagerDistributors(self.tree_distributors)
        self.tree_distributors_manager.AddToggleColumn("Allowed")
        self.tree_distributors_manager.AddTextColumn("Name")
        self.tree_distributors_manager.OnSelectionChanged = self.onTreeDistributorsSelChanged

        self.panel_edit_distributor.Enabled = False
        self.panel_distributors.Enabled = True
        
        self.load() 
        
    def loadDistributors(self):
        self.tree_distributors_manager.ClearItems()
        
        # retrieve categories
        distributors = rest.api.find_distributors()

        for distributor in distributors:
            self.tree_distributors_manager.AppendItem(None, DataModelDistributor(distributor))
    
    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self.loadDistributors()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def ShowDistributor(self, distributor):
        self.distributor = distributor
        
        if distributor:
            self.edit_distributor_name.Value = NoneValue(distributor.name, '')
            self.edit_distributor_address.Value = NoneValue(distributor.address, '')
            self.edit_distributor_website.Value = NoneValue(distributor.website, '')
            self.edit_distributor_sku_url.Value = NoneValue(distributor.sku_url, '')
            self.edit_distributor_email.Value = NoneValue(distributor.email, '')
            self.edit_distributor_phone.Value = NoneValue(distributor.phone, '')
            self.edit_distributor_comment.Value = NoneValue(distributor.comment, '')
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
        if item.IsOk()==False:
            return 
        distributor = self.tree_distributors_manager.ItemToObject(item)
        self.ShowDistributor(distributor.distributor)
        
        self.panel_edit_distributor.Enabled = True
        self.panel_distributors.Enabled = False

    def onButtonRemoveDistributorClick( self, event ):
        item = self.tree_distributors.GetSelection()
        if item.IsOk()==False:
            return
        distributor = self.tree_distributors_manager.ItemToObject(item)
        rest.api.delete_distributor(distributor.distributor.id)
        self.tree_distributors_manager.DeleteItem(None, distributor)
        
    def onButtonRefreshDistributorsClick( self, event ):
        self.load()
    
    def onTreeDistributorsSelChanged( self, event ):
        item = self.tree_distributors.GetSelection()
        if item.IsOk()==False:
            return
        distributor = self.tree_distributors_manager.ItemToObject(item)
        self.ShowDistributor(distributor.distributor)
    
    def onApplyButtonClick( self, event ):
        
        if self.distributor is None:
            distributor = rest.model.DistributorNew()
            distributor.allowed = True
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
                distributor = rest.api.add_distributor(distributor)
                self.tree_distributors_manager.AppendItem(None, DataModelDistributor(distributor))
            else:
                distributor = rest.api.update_distributor(distributor.id, distributor)
                self.tree_distributors_manager.UpdateDistributor(distributor)
                
            self.panel_edit_distributor.Enabled = False
            self.panel_distributors.Enabled = True
            
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        
    def onCancelButtonClick( self, event ):
        self.panel_edit_distributor.Enabled = False
        self.panel_distributors.Enabled = True

