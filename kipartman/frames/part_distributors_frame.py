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

class Offer(helper.tree.TreeItem):
    def __init__(self, offer):
        super(Offer, self).__init__()
        self.offer = offer

    def item_price(self):
        return self.offer.unit_price*self.offer.quantity
    
    def GetValue(self, col):
        if col==1:
            return self.offer.packaging_unit
        elif col==2:
            return self.offer.packaging
        elif col==3:
            return self.offer.quantity
        elif col==4:
            return "{0:.3f}".format(self.item_price())
        elif col==5:
            return "{0:.3f}".format(self.offer.unit_price)
        elif col==6:
            return self.offer.currency
        elif col==7:
            return self.offer.sku
        return ''

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
            for offer in self.part.offers.all():
                distributorobj = self.FindDistributor(offer.distributor)
                if distributorobj is None:
                    distributorobj = Distributor(offer.distributor)
                    self.Append(None, distributorobj)
                else:
                    distributorobj.distributor = offer.distributor
                    self.Update(distributorobj)
                
                offerobj = self.FindOffer(offer)
                if offerobj is None:
                    offerobj = Offer(offer)
                    self.Append(distributorobj, offerobj)
                else:
                    offerobj.offer = offer
                    self.Update(offerobj)
                
#             # add not yet persisted data
#             for parameter in self.part.parameters.pendings():
#                 parameterobj = self.FindParameter(parameter)
#                 if parameterobj is None:
#                     parameterobj = PartParameter(parameter.part, parameter)
#                     self.Append(None, parameterobj)
#                 else:
#                     parameterobj.part = self.part
#                     parameterobj.part_parameter = parameter
#                     self.Update(parameterobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Load()
        
    def FindDistributor(self, distributor):
        for data in self.data:
            if isinstance(data, Distributor) and data.distributor.id==distributor.id:
                return data
        return None

    def FindOffer(self, offer):
        for data in self.data:
            if isinstance(data, Offer) and data.offer.id==offer.id:
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

