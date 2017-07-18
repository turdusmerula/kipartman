from dialogs.panel_part_distributors import PanelPartDistributors
from frames.edit_part_offer_frame import EditPartOfferFrame
import helper.tree
import rest

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

    def FindDistributor(self, name):
        for data in self.tree_distributors_manager.data:
            if isinstance(data, DataModelDistributor) and data.distributor.name==name:
                return data
        return None
        
    def AddPartDistributor(self, distributor):
        """
        Add a distributor to the part
        """
        distributorobj = self.FindDistributor(distributor.name)
        if distributorobj:
            return distributorobj
        # add part distributor
        part_distributor = rest.model.PartDistributor()
        part_distributor.name = distributor.name
        part_distributorobj = DataModelDistributor(part_distributor)

        if self.part.distributors is None:
            self.part.distributors = []
        self.part.distributors.append(part_distributor)
        self.tree_distributors_manager.AppendItem(None, part_distributorobj)
        return part_distributorobj

    def AddOffer(self, offer):
        """
        Add an offer from a distributor
        """
        # add distributor
        distributorobj = self.AddPartDistributor(offer.distributor)
        # add offer
        distributor = distributorobj.distributor
        if distributor.offers is None:
            distributor.offers = []
        offerobj = DataModelOffer(offer)
        distributor.offers.append(offer)
        self.tree_distributors_manager.AppendItem(distributorobj, offerobj)
        return offerobj
    
    def RemoveDistributor(self, name):
        """
        Remove a distributor using its name
        """
        if self.part.distributors is None:
            return 
        
        to_remove = []
        for distributor in self.part.distributors:
            if distributor.name==name:
                to_remove.append(distributor)
        
        # don't remove in previous loop to avoid missing elements
        for distributor in to_remove:
            self.part.distributors.remove(distributor)
            distributorobj = self.FindDistributor(distributor.name)
            self.tree_distributors_manager.DeleteItem(None, distributorobj)
            
    def showDistributors(self):
        self.tree_distributors_manager.ClearItems()

        if self.part and self.part.distributors:
            for distributor in self.part.distributors:
                distributorobj = DataModelDistributor(distributor)
                self.tree_distributors_manager.AppendItem(None, distributorobj)
                for offer in distributor.offers:
                    offerobj = DataModelOffer(offer)
                    self.tree_distributors_manager.AppendItem(distributorobj, offerobj)
                    
        
    def onButtonAddDistributorClick( self, event ):
        offer = EditPartOfferFrame(self).AddOffer(self.part)
        if offer:
            self.AddOffer(offer)

             
    def onButtonEditDistributorClick( self, event ):
        item = self.tree_distributors.GetSelection()
        if item is None:
            return 
        object = self.tree_distributors_manager.ItemToObject(item)
        if not object or isinstance(object, DataModelDistributor):
            return 

        offer = EditPartOfferFrame(self).EditOffer(self.part, object.offer)
        self.tree_distributors_manager.UpdateItem(object)
    
    def onButtonRemoveDistributorClick( self, event ):
        item = self.tree_distributors.GetSelection()
        if not item:
            return
        object = self.tree_distributors_manager.ItemToObject(item)
        if isinstance(object, DataModelDistributor):
            self.RemoveDistributor(object.distributor.name)
        if isinstance(object, DataModelOffer):
            distributorobj = self.FindDistributor(object.offer.distributor.name)
            distributorobj.distributor.offers.remove(object.offer)
            self.tree_distributors_manager.DeleteItem(object.parent, object)
            if len(distributorobj.childs)==0:
                self.tree_distributors_manager.DeleteItem(None, distributorobj)

