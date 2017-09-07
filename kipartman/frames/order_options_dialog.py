from dialogs.dialog_order_options import DialogOrderOptions

import wx
import helper.tree
import rest

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
            return True
        return False
    
class OrderOptionsDialog(DialogOrderOptions):
    def __init__(self, parent): 
        super(OrderOptionsDialog, self).__init__(parent)
        
        self.options = None
        
        self.tree_distributors_manager = helper.tree.TreeManager(self.tree_distributors)
        self.tree_distributors_manager.AddToggleColumn("Authorized")
        self.tree_distributors_manager.AddFloatColumn("Name")

        self.loadDistributors()
        
    def loadDistributors(self):
        distributors = rest.api.find_distributors()
        for distributor in distributors:
            if distributor.allowed:
                self.tree_distributors_manager.AppendItem(None, DataModelDistributor(distributor))
        
    def OnCancelButtonClick( self, event ):
        self.EndModal(wx.ID_CANCEL)
    
    def OnOKButtonClick( self, event ):
        self.options = {}
        self.options['clean'] = self.checkbox_clean.Value
        
        self.options['best_distributor'] = False
        if self.radiobox_distributors.GetSelection()==0:
            self.options['best_distributor'] = True
            
        self.options['best_prices'] = False
        if self.radiobox_distributors.GetSelection()==1:
            self.options['best_prices'] = True

        self.options['allowed_distributors'] = []
        for data in self.tree_distributors_manager.data:
            if data.distributor.allowed==True:
                self.options['allowed_distributors'].append(data.distributor)

        self.EndModal(wx.ID_OK)

    def onCheckSelectAll( self, event ):
        for data in self.tree_distributors_manager.data:
            data.distributor.allowed = True
            self.tree_distributors_manager.UpdateItem(data)
        self.check_select_all.Value = True

    def onCheckSelectNone( self, event ):
        for data in self.tree_distributors_manager.data:
            data.distributor.allowed = False
            self.tree_distributors_manager.UpdateItem(data)
        self.check_select_none.Value = False
