from dialogs.panel_buy import PanelBuy
from frames.order_options_dialog import OrderOptionsDialog
import wx.dataview
from bom_frame import pcb, bom
from currency.currency import Currency
from configuration import Configuration
import rest
import helper.tree
from twisted.cred.checkers import OnDiskUsernamePasswordDatabase

configuration = Configuration()
currency = Currency(configuration.base_currency)

board_number = 1
view_all = True
wish_parts = []

class DataModelBomPart(helper.tree.TreeItem):
    def __init__(self, bom_part):
        super(DataModelBomPart, self).__init__()
        self.bom_part = bom_part
        
    def is_equivalent(self, part):
        to_explore = []
        if self.bom_part.childs is None:
            return False
        for child in self.bom_part.childs:
            to_explore.append(child)
        while len(to_explore)>0:
            child = to_explore[0]
            if child.id==part.id:
                return True
            to_explore.remove(child)
            
            if child.childs:
                for c in child.childs:
                    to_explore.append(c)
    
        return False
    
    def provisioning(self):
        global wish_parts
        provisioning = 0
        for partobj in wish_parts:
            if partobj.part.id==self.bom_part.id or self.is_equivalent(partobj.part):
                provisioning = provisioning+partobj.buy_items(partobj.matching_offer())
        return provisioning
    
    def num_modules(self):
        num_modules = 0
        if bom.part_modules.has_key(self.bom_part.id):
            num_modules = len(bom.part_modules[self.bom_part.id])
        return num_modules
    
    def needed(self):
        return board_number*self.num_modules()
    
    def GetValue(self, col):
        vMap = { 
            0 : str(self.bom_part.id),
            1 : self.bom_part.name,
            2 : str(self.num_modules()),
            3 : str(self.needed()),
            4 : str(int(self.provisioning())),
            5 : self.bom_part.description,
            6 : self.bom_part.comment,
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        if col==4:
            if self.provisioning()<self.needed():
                attr.SetColour('red') # red
                attr.Bold = True
            else:
                attr.SetColour('green') # green
            return True
        return False

class DataModelEquivalentPart(helper.tree.TreeItem):
    def __init__(self, equivalent_part):
        super(DataModelEquivalentPart, self).__init__()
        self.equivalent_part = equivalent_part
        
    def GetValue(self, col):
        vMap = { 
            0 : str(self.equivalent_part.id),
            1 : self.equivalent_part.name,
            2 : self.equivalent_part.description,
            3 : self.equivalent_part.comment,
        }
        return vMap[col]

class DataModelEquivalentPartContainer(helper.tree.TreeContainerItem):
    def __init__(self, part):
        super(DataModelEquivalentPartContainer, self).__init__()
        self.part = part
    
    def GetValue(self, col):
        if col==0:
            return self.part.name
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==0:
            attr.Bold = True
            return True
        return False

class DataModelDistributorContainer(helper.tree.TreeContainerItem):
    def __init__(self, distributor):
        super(DataModelDistributorContainer, self).__init__()
        self.distributor = distributor
    
    def GetValue(self, col):
        if col==0:
            return self.distributor.name
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==0:
            attr.Bold = True
            return True
        return False
    
class DataModelOffer(helper.tree.TreeItem):
    def __init__(self, offer, bom_part):
        super(DataModelOffer, self).__init__()
        self.offer = offer
        self.bom_part = bom_part
    
    def item_price(self):
        return self.converted_unit_price()[0]*self.offer.quantity

    def converted_unit_price(self):
        res = [self.offer.unit_price, self.offer.currency]
        try:
            return [currency.convert(self.offer.unit_price, self.offer.currency, configuration.base_currency), configuration.base_currency]
        except:
            # error during conversion, no conversion
            return res
    
    def parts_num(self):
        global board_number
        num_modules = 0
        if bom.part_modules.has_key(self.bom_part.id):
            num_modules = len(bom.part_modules[self.bom_part.id])
        return num_modules*board_number
    
    def buy_packages(self):
        # number of packages to buy
        buy_packages = int(self.parts_num()/self.offer.packaging_unit)
        if divmod(self.parts_num(), self.offer.packaging_unit)[1]>0:
            buy_packages = buy_packages+1
        if buy_packages*self.offer.packaging_unit<self.offer.quantity:
            buy_packages = self.offer.quantity/self.offer.packaging_unit
        return buy_packages
    
    def buy_items(self):
        return self.buy_packages()*self.offer.packaging_unit
    
    def buy_price(self):
        # price to pay
        return self.buy_items()*self.converted_unit_price()[0]
    
    def GetValue(self, col):
        converted_unit_price = self.converted_unit_price()
        
        vMap = { 
            0 : str(int(self.buy_items())),
            1 : str(self.buy_price()),
            2 : str(int(self.offer.packaging_unit)),
            3 : str(int(self.offer.quantity)),
            4 : str(self.item_price()),
            5 : str(converted_unit_price[0]),
            6 : converted_unit_price[1],
            7 : self.offer.sku,
        }
        return vMap[col]

class DataModelWishPart(helper.tree.TreeItem):
    def __init__(self, part, distributor, sku, quantity):
        super(DataModelWishPart, self).__init__()
        # part is the real part likely to be bought
        self.part = part
        self.distributor = distributor
        self.quantity = quantity
        self.sku = sku
        
    def converted_unit_price(self, offer):
        res = [offer.unit_price, offer.currency]
        try:
            return [currency.convert(offer.unit_price, offer.currency, configuration.base_currency), configuration.base_currency]
        except:
            # error during conversion, no conversion
            return res

    def buy_packages(self, offer):
        # number of packages to buy
        quantity = self.quantity
        if quantity<offer.packaging_unit:
            quantity = offer.packaging_unit
        if quantity<offer.quantity:
            quantity = offer.quantity
        buy_packages = int(quantity/offer.packaging_unit)
        if divmod(quantity, offer.packaging_unit)[1]>0:
            buy_packages = buy_packages+1
        return buy_packages

    def buy_items(self, offer):
        return self.buy_packages(offer)*offer.packaging_unit

    def buy_price(self, offer):
        # price to pay
        return self.buy_items(offer)*self.converted_unit_price(offer)[0]

    def matching_offer(self):
        matching_offer = None
        for offer in self.distributor.offers:
            if offer.sku==self.sku:
                if matching_offer is None:
                    matching_offer = offer
                if self.buy_price(offer)<self.buy_price(matching_offer) and self.buy_items(offer)>=self.quantity:
                    matching_offer = offer
        return matching_offer

    def GetValue(self, col):
        matching_offer = self.matching_offer()
        print "++++", matching_offer, self.sku
        vMap = { 
            0 : self.part.name,
            1 : self.distributor.name,
            2 : self.sku,
            3 : str(matching_offer.packaging_unit),
            4 : str(int(self.buy_items(matching_offer))),
            5 : str(self.buy_price(matching_offer)),
            6 : str(self.converted_unit_price(matching_offer)[1]),
        }
        return vMap[col]


class TreeManagerDistributors(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerDistributors, self).__init__(tree_view)
    

class BuyFrame(PanelBuy): 
    def __init__(self, parent):
        super(BuyFrame, self).__init__(parent)

        # create module bom parts list
        self.tree_bom_parts_manager = helper.tree.TreeManager(self.tree_bom_parts)
        self.tree_bom_parts_manager.AddIntegerColumn("Id")
        self.tree_bom_parts_manager.AddTextColumn("Name")
        self.tree_bom_parts_manager.AddIntegerColumn("Modules")
        self.tree_bom_parts_manager.AddIntegerColumn("Needed")
        self.tree_bom_parts_manager.AddIntegerColumn("Provisioning")
        self.tree_bom_parts_manager.AddTextColumn("Description")
        self.tree_bom_parts_manager.AddTextColumn("Comment")

        # create equivalent parts list
        self.tree_equivalent_parts_manager = helper.tree.TreeManager(self.tree_part_equivalents)
        self.tree_equivalent_parts_manager.AddIntegerColumn("Id")
        self.tree_equivalent_parts_manager.AddTextColumn("Name")
        self.tree_equivalent_parts_manager.AddTextColumn("Description")
        self.tree_equivalent_parts_manager.AddTextColumn("Comment")

        # create octoparts list
        self.tree_distributors_manager = TreeManagerDistributors(self.tree_distributors)
        self.tree_distributors_manager.AddIntegerColumn("Amount To Buy")
        self.tree_distributors_manager.AddFloatColumn("Buy Price")
        self.tree_distributors_manager.AddIntegerColumn("Packaging Unit")
        self.tree_distributors_manager.AddIntegerColumn("Quantity")
        self.tree_distributors_manager.AddFloatColumn("Price")
        self.tree_distributors_manager.AddFloatColumn("Price per Item")
        self.tree_distributors_manager.AddTextColumn("Currency")
        self.tree_distributors_manager.AddTextColumn("SKU")

        # create wish parts list
        self.tree_wish_parts_manager = helper.tree.TreeManager(self.tree_wish_parts)
        self.tree_wish_parts_manager.AddTextColumn("Part")
        self.tree_wish_parts_manager.AddTextColumn("Distributor")
        self.tree_wish_parts_manager.AddTextColumn("SKU")
        self.tree_wish_parts_manager.AddIntegerColumn("Packaging Unit")
        self.tree_wish_parts_manager.AddFloatColumn("Amount")
        self.tree_wish_parts_manager.AddFloatColumn("Buy Price")
        self.tree_wish_parts_manager.AddTextColumn("Currency")

    def load(self):
        self.loadBomParts()
        self.loadPartEquivalents()
        self.loadDistributors()
    
    def refresh(self):
        self.refreshBomParts()
    
    def refreshBomParts(self):
        for data in self.tree_bom_parts_manager.data:
            self.tree_bom_parts_manager.UpdateItem(data)
        
    def loadBomParts(self):
        self.tree_bom_parts_manager.ClearItems()

        for bom_part in bom.Parts():
            full_part = rest.api.find_part(bom_part.id, with_childs=True)
            self.tree_bom_parts_manager.AppendItem(None, DataModelBomPart(full_part))

    def loadPartEquivalents(self):
        self.tree_equivalent_parts_manager.ClearItems()
        
        item = self.tree_bom_parts.GetSelection()
        part = None
        if item.IsOk()==False:
            return 
        
        part = self.tree_bom_parts_manager.ItemToObject(item).bom_part
        part = rest.api.find_part(part.id, with_childs=True)

        if part.childs is None:
            return
        # load parts
        to_add = []
        added = {}
        for child in part.childs:
            to_add.append(child)
        
        # recursive load subparts
        for child in to_add:
            if added.has_key(child.id)==False:
                self.tree_equivalent_parts_manager.AppendItem(None, DataModelEquivalentPart(child))
                added[child.id] = child
                
                if child.childs:
                    for c in child.childs:
                        to_add.append(c)

        self.tree_part_equivalents.SelectAll()
    
    def loadWhishParts(self):
        pass
    
    def loadTotalPrice(self):
        total = 0

        for data in self.tree_wish_parts_manager.data:
            total = total+data.buy_price(data.matching_offer())
        self.text_total_price.SetValue(str(total))
        self.static_total_price.SetLabel(configuration.base_currency)

    def loadDistributors(self):
        parts = []
        global view_all
    
        self.tree_distributors_manager.ClearItems()

        item = self.tree_bom_parts.GetSelection()
        if item.IsOk()==False:
            return 
        bom_part = self.tree_bom_parts_manager.ItemToObject(item).bom_part
        # load full part
        bom_part = rest.api.find_part(bom_part.id, with_distributors=True)
        parts.append(bom_part)
        
        for item in self.tree_part_equivalents.GetSelections():
            if item.IsOk():
                equivalent_part = self.tree_equivalent_parts_manager.ItemToObject(item).equivalent_part
                equivalent_part = rest.api.find_part(equivalent_part.id, with_distributors=True)
                parts.append(equivalent_part)
        
        self.tree_distributors_manager.ClearItems()

        # calculate pricing elements
        for part in parts:
            partobj = DataModelEquivalentPartContainer(part)
            self.tree_distributors_manager.AppendItem(None, partobj)
            
            for distributor in part.distributors:
                if distributor.allowed:
                    distributorobj = DataModelDistributorContainer(distributor)
                    self.tree_distributors_manager.AppendItem(partobj, distributorobj)
                    
                    if view_all:
                        self.loadAllOffers(bom_part, distributorobj)
                    else:
                        self.loadBestOffers(bom_part, distributorobj)
    
    def loadAllOffers(self, bom_part, distributorobj):
        for offer in distributorobj.distributor.offers:
            offerobj = DataModelOffer(offer, bom_part)
            self.tree_distributors_manager.AppendItem(distributorobj, offerobj)
    
    def loadBestOffers(self, bom_part, distributorobj):
        # Only keep best offer for each sku of each distributor
        # best offer by sku
        sku_best_offerobj = self.get_distributor_best_offers(bom_part, distributorobj)
        for sku in sku_best_offerobj:
            self.tree_distributors_manager.AppendItem(distributorobj, sku_best_offerobj[sku])
        
    def GetMenus(self):
        return [{'title': 'Prices', 'menu': self.menu_prices}]
    
    def onTreeBomPartsSelectionChanged( self, event ):
        self.loadPartEquivalents()
        self.loadDistributors()
    
    def onTreePartEquivalentsSelectionChanged( self, event ):
        self.loadDistributors()

    def onTreeDistributorsSelectionChanged( self, event ):
        self.spin_add_wish_parts.SetValue(0)
        item = self.tree_distributors.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_distributors_manager.ItemToObject(item)
        if isinstance(obj, DataModelOffer)==False:
            return

        self.spin_add_wish_parts.SetValue(obj.buy_items())
            
    def OnMenuItem( self, event ):
        # events are not distributed by the frame so we distribute them manually
        if event.GetId()==self.menu_item_prices_view_all.GetId():
            self.onMenuItemPricesViewAllSelection(event)
        elif event.GetId()==self.menu_item_prices_select_bestprice.GetId():
            self.onMenuItemPricesSelectBestpriceSelection(event)
        elif event.GetId()==self.menu_item_prices_automatic_order.GetId():
            self.onMenuItemPricesAutomaticOrderSelection(event)
    
    def onMenuItemPricesViewAllSelection( self, event ):
        global view_all
        view_all = self.menu_item_prices_view_all.IsChecked()
        self.loadDistributors()
    
    def onMenuItemPricesSelectBestpriceSelection( self, event ):
        best_offer = None
        for data in self.tree_distributors_manager.data:
            if isinstance(data, DataModelOffer):
                if best_offer is None:
                    best_offer = data
                if data.buy_price()<best_offer.buy_price():
                    best_offer = data
        
        self.tree_distributors_manager.Select(best_offer)
    
    def onMenuItemPricesAutomaticOrderSelection(self, event):
        options_dlg = OrderOptionsDialog(self)
        options_dlg.ShowModal()
        options = options_dlg.options
        if options is None:
            return
        
#         if options['clean']:
        self.tree_wish_parts_manager.ClearItems()

        if options['best_distributor']:
            self.add_wishes_best_distributor(options['allowed_distributors'])
        else:
            self.add_wishes_best_offers(options['allowed_distributors'])

#     class Offer(object):
#         def __init__(self, offerobj):
#             self.offerobj = offerobj
#     
#     class Distributor(object):
#         def __init__(self, distributorobj):
#             self.distributorobj = distributorobj

    def needed_bom_parts(self):
        parts = []
        for bom_part in self.tree_bom_parts_manager.data:
            if bom_part.provisioning()<bom_part.needed():
                parts.append(rest.api.find_part(bom_part.bom_part.id, with_distributors=True, with_offers=True, with_childs=True))
        return parts
    
    def get_distributor_best_offers(self, bom_part, distributorobj):
        # returns a list of best offer per part sku
        sku_best_offerobj = {}
        for offer in distributorobj.distributor.offers:
            offerobj = DataModelOffer(offer, bom_part)
            if sku_best_offerobj.has_key(offer.sku)==False:
                sku_best_offerobj[offer.sku] = offerobj
            elif offerobj.buy_price()<sku_best_offerobj[offer.sku].buy_price():
                best_offerobj = offerobj
        return sku_best_offerobj
    
    def get_distributor_best_offer(self, bom_part, distributorobj):
        sku_best_offerobj = self.get_distributor_best_offers(bom_part, distributorobj)
        best_offerobj = None
        for sku in sku_best_offerobj:
            if best_offerobj is None:
                best_offerobj = sku_best_offerobj[sku]
            if sku_best_offerobj[sku].item_price()<best_offerobj.item_price():
                best_offerobj = sku_best_offerobj[sku]
        return best_offerobj 

    def add_wishes_best_distributor(self, distributors):
        # compute distributor best prices
        
        # list of distributors
        distributor_parts = {}
        
        # parts to search best distributor
        bom_parts = self.needed_bom_parts()
        while len(bom_parts)>0:
        
            for distributor in distributors:
                if distributor.allowed:
                    # keep only allowed distributors
                    distributor_parts[distributor.name] = {'total_price': 0, 'parts': [], 'distributor': None}

            # search best offer for each distributor of each part
            for bom_part in bom_parts:
                if bom_part.distributors:
                    for distributor in bom_part.distributors:
                        if distributor_parts.has_key(distributor.name):
                            best_offerobj = self.get_distributor_best_offer(bom_part, DataModelDistributorContainer(distributor))
                            if best_offerobj is None:
                                raise "No best offer for distributor %s"%distributor.name
                            distributor_parts[distributor.name]['parts'].append(
                                {   
                                    'part': bom_part, 
                                    'offer': best_offerobj
                                }
                            )
                            distributor_parts[distributor.name]['total_price'] = distributor_parts[distributor.name]['total_price']+best_offerobj.buy_price()
                            distributor_parts[distributor.name]['distributor'] = distributor.name
                        
            for distributor_name in distributor_parts:
                distributor = distributor_parts[distributor_name]
                print "----", distributor_name
                print distributor['total_price'], len(distributor['parts'])
                for part in distributor_parts[distributor['distributor']]['parts']:
                    print part['part'].id, part['offer'].offer.sku
                
            # search best distributor
            best_distributor = None
            for distributor_name in distributor_parts:
                distributor = distributor_parts[distributor_name]
                if best_distributor is None:
                    best_distributor = distributor
                if distributor['total_price']<best_distributor['total_price'] and len(distributor['parts'])>=len(best_distributor['parts']):
                    best_distributor = distributor
            
            if best_distributor:
                # add wishes to list
                for part in best_distributor['parts']:
                    offer = part['offer']
                    # get distributor
                    distributor = None
                    for d in part['part'].distributors:
                        if d.name==best_distributor['distributor']:
                            distributor = d
                            
#                    print type(part['part']), type(best_distributor['distributor']), offer.offer.sku, offer.buy_items()
                    self.tree_wish_parts_manager.AppendItem(None, 
                        DataModelWishPart(part['part'], distributor, offer.offer.sku, offer.buy_items()))

            bom_parts = []
            #bom_parts = self.needed_bom_parts()
        self.refresh()
        self.loadTotalPrice()
        
    def add_wishes_best_offers(self):
        pass
    
    def onSpinBoardNumberCtrl( self, event ):
        global board_number
        board_number = self.spin_board_number.Value
        self.loadBomParts()
        self.loadDistributors()

    def onButtonAddWishPartsClick( self, event ):
        global wish_parts
        wish_parts = self.tree_wish_parts_manager.data
        
        item = self.tree_distributors.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_distributors_manager.ItemToObject(item)
        if isinstance(obj, DataModelOffer)==False:
            return
        part = obj.parent.parent.part
        distributor = obj.parent.distributor
        offer = obj.offer
        
        item = self.tree_bom_parts.GetSelection()
        if item.IsOk()==False:
            return        
        obj = self.tree_bom_parts_manager.ItemToObject(item)
        bom_part = obj.bom_part
        
        # search if part already added for this distributor
        wishobj = None
        for data in self.tree_wish_parts_manager.data:
            if data.part.name==part.name and data.sku==offer.sku:
                wishobj = data
        
        if wishobj:
            # append requested items to alredy existing wish
            wishobj.quantity = wishobj.quantity+self.spin_add_wish_parts.GetValue()
            self.tree_wish_parts_manager.UpdateItem(wishobj)
        else:
            wishobj = DataModelWishPart(part, distributor, offer.sku, self.spin_add_wish_parts.GetValue())
            self.tree_wish_parts_manager.AppendItem(None, wishobj)

        self.refresh()
        self.loadTotalPrice()
        

    def onButtonRefreshClick(self, event):
        self.load()

    def onButtonEditWishClick( self, event ):
        event.Skip()
    
    def onButtonDeleteWishClick( self, event ):
        item = self.tree_wish_parts.GetSelection()
        if item.IsOk()==False:
            return
        wishobj = self.tree_wish_parts_manager.ItemToObject(item)
        self.tree_wish_parts_manager.DeleteItem(None, wishobj)
        
        self.refresh()
        
