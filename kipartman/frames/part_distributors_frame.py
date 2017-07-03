from dialogs.panel_part_distributors import PanelPartDistributors
from frames.edit_part_distributor_frame import EditPartDistributorFrame
from frames.dropdown_dialog import DropdownDialog
import wx.dataview
import api.queries
 
class PartDistributorsDataModel(wx.dataview.PyDataViewModel):
    def __init__(self, part):
        super(PartDistributorsDataModel, self).__init__()
        if part:
            self.data = part.distributors
        else:
            self.data = []
            
    def GetColumnCount(self):
        return 6

    def GetColumnType(self, col):
        mapper = { 
            0 : 'string',
            1 : 'long',
            2 : 'long',
            3 : 'float',
            4 : 'float',
            5 : 'string',
            6 : 'string',
         }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for distributor in self.data:
                children.append(self.ObjectToItem(distributor))
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
        if obj.distributor:
            distributor = obj.distributor.name
        else:
            distributor = ''
        vMap = { 
            0 : distributor,
            1 : str(obj.packaging_unit),
            2 : str(obj.quantity),
            3 : str(obj.item_price()),
            4 : str(obj.unit_price),
            5 : obj.currency,
            6 : obj.sku,
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
            
class PartDistributorsFrame(PanelPartDistributors):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartDistributorsFrame, self).__init__(parent)

        # create octoparts list
        self.distributors_model = PartDistributorsDataModel(None)
        self.tree_distributors.AssociateModel(self.distributors_model)
        # add default columns
        self.tree_distributors.AppendTextColumn("Distributor", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Packaging Unit", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Quantity", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Price", 3, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Price per Item", 4, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Currency", 5, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("SKU", 6, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_distributors.Columns:
            c.Sortable = True

        self.enable(False)
        
    def SetPart(self, part):
        # array of changes to apply
        self.create_list = []
        self.update_list = []
        self.remove_list = []

        self.part = part
        self._showDistributors()

    def enable(self, enabled=True):
        self.button_add_distributor.Enabled = enabled
        self.button_edit_distributor.Enabled = enabled
        self.button_remove_distributor.Enabled = enabled

    def AddDistributor(self, distributor):
        """
        Add a distributor to the part
        """
        # add distributor
        self.part.distributors.append(distributor)
        self.create_list.append(distributor)
        self._showDistributors()

    def RemoveDistributor(self, name):
        """
        Remove a distributor using its name
        """
        to_remove = []
        for distributor in self.part.distributors:
            if distributor.distributor and distributor.distributor.name==name:
                if distributor.id!=-1:
                    self.remove_list.append(distributor)
                    to_remove.append(distributor)
                    # remove it from update list if present
                    try:
                        # remove it if already exists
                        self.update_list.remove(distributor)
                    except:
                        pass
                else:
                    to_remove.append(distributor)
        
        # don't remove in previous loop to avoid missing elements
        for distributor in to_remove:
            self.part.distributors.remove(distributor)

        self._showDistributors()
        
    def _showDistributors(self):
        # apply new filter and reload
        self.distributors_model.Cleared()
        self.distributors_model = PartDistributorsDataModel(self.part)
        self.tree_distributors.AssociateModel(self.distributors_model)
    
    def ApplyChanges(self, part):
        for distributor in self.remove_list:
            distributor.part = part
            api.queries.PartDistributorsQuery().delete(distributor)
        self.remove_list = []

        # apply changes to current part
        for distributor in self.create_list:
            distributor.part = part
            api.queries.PartDistributorsQuery().create(distributor)
        self.create_list = []
        
        for distributor in self.update_list:
            distributor.part = part
            api.queries.PartDistributorsQuery().update(distributor)
        self.update_list = []
        
    def onButtonAddDistributorClick( self, event ):
        distributor = EditPartDistributorFrame(self).AddDistributor(self.part)
        if not distributor is None:
            self.part.distributors.append(distributor)
            self.create_list.append(distributor)
        self._showDistributors()
             
    def onButtonEditDistributorClick( self, event ):
        item = self.tree_distributors.GetSelection()
        if item is None:
            return 
        distributor = self.distributors_model.ItemToObject(item)
        if not distributor:
            return 
        if EditPartDistributorFrame(self).EditDistributor(self.part, distributor) and distributor.id!=-1:
            # set distributor to be updated
            try:
                # remove it from update list to avoid multiple update
                self.update_list.remove(distributor)
            except:
                pass
            self.update_list.append(distributor)
        self._showDistributors()
    
    def onButtonRemoveDistributorClick( self, event ):
        item = self.tree_distributors.GetSelection()
        if not item:
            return
        distributor = self.distributors_model.ItemToObject(item)
        self.part.distributors.remove(distributor)
        # set distributor to be removed
        if distributor.id!=-1:
            self.remove_list.append(distributor)
            try:
                # remove it from update list if present
                self.update_list.remove(distributor)
            except:
                pass

        self._showDistributors()
