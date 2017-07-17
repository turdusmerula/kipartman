from dialogs.panel_part_distributors import PanelPartDistributors
from frames.edit_part_distributor_frame import EditPartDistributorFrame
import helper.tree

class DataModelDistributor(helper.tree.TreeContainerItem):
    def __init__(self, distributor):
        super(DataModelDistributor, self).__init__()
        self.distributor = distributor

    def GetValue(self, col):
        if col==0:
            return self.distributor.name
        return ''

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

class DataModelOffer(helper.tree.TreeItem):
    def __init__(self, offer):
        super(DataModelOffer, self).__init__()
        self.offer = offer

    def item_price(self):
        return self.offer.unit_price*self.offer.packaging_unit
    
    def GetValue(self, col):
        vMap = { 
            0 : '',
            1 : str(self.offer.packaging_unit),
            2 : str(self.offer.quantity),
            3 : str(self.item_price()),
            4 : str(self.offer.unit_price),
            5 : self.offer.currency,
            6 : self.offer.sku,
        }
        return vMap[col]

            
class PartDistributorsFrame(PanelPartDistributors):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartDistributorsFrame, self).__init__(parent)

        # create distributors list
        self.tree_distributors_manager = helper.tree.TreeManager(self.tree_distributors)
        self.tree_distributors_manager.AddTextColumn("Distributor")
        self.tree_distributors_manager.AddIntegerColumn("Packaging Unit")
        self.tree_distributors_manager.AddIntegerColumn("Quantity")
        self.tree_distributors_manager.AddFloatColumn("Price")
        self.tree_distributors_manager.AddFloatColumn("Price per Item")
        self.tree_distributors_manager.AddTextColumn("Currency")
        self.tree_distributors_manager.AddTextColumn("SKU")

        self.enable(False)
        
    def SetPart(self, part):
        self.part = part
        self.showDistributors()

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
        
    def showDistributors(self):
        self.tree_distributors_manager.ClearItems()

        if self.part and self.part.distributors:
            for distributor in self.part.distributors:
                distributorobj = DataModelDistributor(distributor)
                self.tree_distributors_manager.AppendItem(None, distributorobj)
                for offer in distributor.offers:
                    offerobj = DataModelOffer(offer)
                    self.tree_distributors_manager.AppendItem(distributorobj, offerobj)
                    
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
