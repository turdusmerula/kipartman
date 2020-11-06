from dialogs.panel_part_distributors import PanelPartDistributors
from frames.edit_part_offer_frame import EditPartOfferFrame
import helper.tree
from helper.log import log
import api.data.part_offer

class Distributor(helper.tree.TreeContainerItem):
    def __init__(self, distributor):
        super(Distributor, self).__init__()
        self.distributor = distributor

    def GetValue(self, col):
        if col==0:
            return self.distributor.name
        return ''

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

class PartOffer(helper.tree.TreeItem):
    def __init__(self, part_offer):
        super(PartOffer, self).__init__()
        self.part_offer = part_offer

    def item_price(self):
        return self.part_offer.unit_price*self.part_offer.quantity
    
    def GetValue(self, col):
        if col==1:
            return self.part_offer.packaging_unit
        elif col==2:
            return self.part_offer.packaging
        elif col==3:
            return self.part_offer.quantity
        elif col==4:
            return "{0:.3f}".format(self.item_price())
        elif col==5:
            return "{0:.3f}".format(self.part_offer.unit_price)
        elif col==6:
            return self.part_offer.currency
        elif col==7:
            return self.part_offer.sku
        return ''

    def GetAttr(self, col, attr):
        res = False
        if self.part_offer.id is None:
            attr.SetColour(helper.colors.GREEN_NEW_ITEM)
            res = True
        if self.part_offer.removed_pending():
            attr.SetStrikethrough(True)
            res = True
        return res

class TreeManagerPartDistributor(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerPartDistributor, self).__init__(tree_view, *args, **kwargs)

        self.part = None
        
        self.AddTextColumn("distributor")
        self.AddIntegerColumn("packaging unit")
        self.AddIntegerColumn("packaging")
        self.AddIntegerColumn("quantity")
        # TODO AddCurrencyColumn
        self.AddFloatColumn("price")
        self.AddFloatColumn("price per item")
        self.AddTextColumn("currency")
        self.AddTextColumn("SKU")
        # TODO
#         self.AddDateColumn("updated")

    def Load(self):
        
        self.SaveState()
        
        if self.part is not None:
            for part_offer in self.part.offers.all():
                distributorobj = self.FindDistributor(part_offer.distributor)
                if distributorobj is None:
                    distributorobj = Distributor(part_offer.distributor)
                    self.Append(None, distributorobj)
                else:
                    # all() extracts from database, fields are not updated to avoid discarding changes
                    self.Update(distributorobj)
                
                part_offerobj = self.FindPartOffer(part_offer)
                if part_offerobj is None:
                    part_offerobj = PartOffer(part_offer)
                    self.Append(distributorobj, part_offerobj)
                else:
                    # all() extracts from database, fields are not updated to avoid discarding changes
                    self.Update(part_offerobj)
                
            for part_offer in self.part.offers.pendings():
                distributorobj = self.FindDistributor(part_offer.distributor)
                if distributorobj is None:
                    distributorobj = Distributor(part_offer.distributor)
                    self.Append(None, distributorobj)
                else:
                    # all() extracts from database, fields are not updated to avoid discarding changes
                    self.Update(distributorobj)
                
                part_offerobj = self.FindPartOffer(part_offer)
                if part_offerobj is None:
                    part_offerobj = PartOffer(part_offer)
                    self.Append(distributorobj, part_offerobj)
                else:
                    # all() extracts from database, fields are not updated to avoid discarding changes
                    self.Update(part_offerobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Load()
        
    def FindDistributor(self, distributor):
        for data in self.data:
            if isinstance(data, Distributor) and ( (data.distributor.id is not None and data.distributor.id==distributor.id) or (data.distributor.id is None and data.distributor==distributor)):
                return data
        return None

    def FindPartOffer(self, part_offer):
        for data in self.data:
            if isinstance(data, PartOffer) and ( (data.part_offer.id is not None and data.part_offer.id==part_offer.id) or (data.part_offer.id is None and data.part_offer==part_offer) ):
                return data
        return None

class PartDistributorsFrame(PanelPartDistributors):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartDistributorsFrame, self).__init__(parent)

        # create distributors list
        self.tree_distributors_manager = TreeManagerPartDistributor(self.tree_distributors, context_menu=self.menu_distributors)
        self.tree_distributors_manager.OnItemBeforeContextMenu = self.onTreeDistributorsBeforeContextMenu

        self.tree_distributors_manager.Clear()
        self.SetPart(None)
        
        self._enable(False)
        
    def SetPart(self, part):
        self.part = part
        self.tree_distributors_manager.SetPart(part)
        self._enable(False)

    def EditPart(self, part):
        self.part = part
        self.tree_distributors_manager.SetPart(part)
        self._enable(True)

    def _enable(self, enabled=True):
        self.enabled = enabled

    def Save(self, part):
        pass

    def onTreeDistributorsBeforeContextMenu( self, event ):
        self.menu_distributor_add_distributor.Enable(True)
        self.menu_distributor_edit_distributor.Enable(True)
        self.menu_distributor_remove_distributor.Enable(True)
        if len(self.tree_distributors.GetSelections())==0:
            self.menu_distributor_edit_distributor.Enable(False)
            self.menu_distributor_remove_distributor.Enable(False)
        if len(self.tree_distributors.GetSelections())>1:
            self.menu_distributor_edit_distributor.Enable(False)
         
        if self.enabled==False:
            self.menu_distributor_add_distributor.Enable(False)
            self.menu_distributor_edit_distributor.Enable(False)
            self.menu_distributor_remove_distributor.Enable(False)

    def onMenuDistributorAddDistributor( self, event ):
        item = self.tree_distributors.GetSelection()
        distributor = None
        currency = None
        sku = None
        packaging = None
        if item.IsOk():
            obj = self.tree_distributors_manager.ItemToObject(item)
            if isinstance(obj, Distributor):
                distributor = obj.distributor
            elif isinstance(obj, PartOffer):
                distributor = obj.part_offer.distributor
                currency = obj.part_offer.currency
                sku = obj.part_offer.sku
                packaging = obj.part_offer.packaging
        EditPartOfferFrame(self).AddPartOffer(self.part, distributor, currency, sku, packaging)
        self.tree_distributors_manager.Load()

    def onMenuDistributorEditDistributor( self, event ):
        item = self.tree_distributors.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_distributors_manager.ItemToObject(item)
        if isinstance(obj, PartOffer)==False:
            return
        EditPartOfferFrame(self).EditPartOffer(self.part, obj.part_offer)
        self.tree_distributors_manager.Load()        
        event.Skip()

    def onMenuDistributorRemoveDistributor( self, event ):
        part_offers = []
        for item in self.tree_distributors.GetSelections():
            obj = self.tree_distributors_manager.ItemToObject(item)
            if isinstance(obj, PartOffer):
                part_offers.append(obj)
            if isinstance(obj, Distributor):
                for child in obj.childs:
                    part_offers.append(child)
        for part_offerobj in part_offers:
            self.part.offers.remove_pending(part_offerobj.part_offer)
        self.tree_distributors_manager.Load()
        event.Skip()

#     def AddPartDistributor(self, distributor):
#         """
#         Add a distributor to the part
#         """
#         distributorobj = self.FindDistributor(distributor.name)
#         if distributorobj:
#             return distributorobj
#         # add part distributor
#         part_distributor = rest.model.PartDistributor()
#         part_distributor.name = distributor.name
#         part_distributorobj = Distributor(part_distributor)
# 
#         if self.part.distributors is None:
#             self.part.distributors = []
#         self.part.distributors.append(part_distributor)
#         self.tree_distributors_manager.AppendItem(None, part_distributorobj)
#         return part_distributorobj
# 
#     def AddOffer(self, offer):
#         """
#         Add an offer from a distributor
#         """
#         # add distributor
#         distributorobj = self.AddPartDistributor(offer.distributor)
#         # add offer
#         distributor = distributorobj.distributor
#         if distributor.offers is None:
#             distributor.offers = []
#         offerobj = Offer(offer)
#         distributor.offers.append(offer)
#         self.tree_distributors_manager.AppendItem(distributorobj, offerobj)
#         return offerobj
#     
#     def RemoveDistributor(self, name):
#         """
#         Remove a distributor using its name
#         """
#         if self.part.distributors is None:
#             return 
#         
#         to_remove = []
#         for distributor in self.part.distributors:
#             if distributor.name==name:
#                 to_remove.append(distributor)
#         
#         # don't remove in previous loop to avoid missing elements
#         for distributor in to_remove:
#             self.part.distributors.remove(distributor)
#             distributorobj = self.FindDistributor(distributor.name)
#             self.tree_distributors_manager.DeleteItem(None, distributorobj)
#             
#     def showDistributors(self):
#         self.tree_distributors_manager.ClearItems()
# 
#         if self.part and self.part.distributors:
#             for distributor in self.part.distributors:
#                 distributorobj = Distributor(distributor)
#                 self.tree_distributors_manager.AppendItem(None, distributorobj)
#                 for offer in distributor.offers:
#                     offerobj = Offer(offer)
#                     self.tree_distributors_manager.AppendItem(distributorobj, offerobj)
#                     
#         
#     def onMenuDistributorAddDistributor( self, event ):
#         offer = EditPartOfferFrame(self).AddOffer(self.part)
#         if offer:
#             self.AddOffer(offer)
#              
#     def onMenuDistributorEditDistributor( self, event ):
#         item = self.tree_distributors.GetSelection()
#         if item is None:
#             return 
#         object = self.tree_distributors_manager.ItemToObject(item)
#         if not object or isinstance(object, Distributor):
#             return 
# 
#         offer = EditPartOfferFrame(self).EditOffer(self.part, object.offer)
#         self.tree_distributors_manager.UpdateItem(object)
#     
#     def onMenuDistributorRemoveDistributor( self, event ):
#         distributors = []
#         offers = []
#         for item in self.tree_distributors.GetSelections():
#             obj = self.tree_distributors_manager.ItemToObject(item)
#             if isinstance(obj, Distributor):
#                 distributors.append(obj)
#             if isinstance(obj, Offer):
#                 offers.append(obj)
# 
#         for offer in offers:
#             distributorobj = self.FindDistributor(offer.parent.distributor.name)
#             distributorobj.distributor.offers.remove(offer.offer)
#             self.tree_distributors_manager.DeleteItem(offer.parent, offer)
#             if len(distributorobj.childs)==0:
#                 self.tree_distributors_manager.DeleteItem(None, distributorobj)
#         
#         for distributor in distributors:
#             self.RemoveDistributor(distributor.distributor.name)

