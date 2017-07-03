from dialogs.panel_buy import PanelBuy
import wx.dataview
from bom_frame import pcb, bom
from api.queries import PartsQuery
from currency.currency import Currency
from configuration import Configuration

configuration = Configuration()
currency = Currency(configuration.base_currency)

class BomPartsModel(wx.dataview.PyDataViewModel):
    def __init__(self):
        super(BomPartsModel, self).__init__()
    
        self.parts = bom.Parts()
        
    def GetColumnCount(self):
        return 7

    def GetColumnType(self, col):
        mapper = { 
            0 : 'long',
            1 : 'string',
            2 : 'string',
            3 : 'string',
            4 : 'long',
            5 : 'long',
            6 : 'long'
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for part in self.parts:
                children.append(self.ObjectToItem(part))
            return len(self.parts)
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        num_modules = 0
        if bom.part_modules.has_key(obj.id):
            num_modules = len(bom.part_modules[obj.id])
        vMap = { 
            0 : str(obj.id),
            1 : obj.name,
            2 : obj.description,
            3 : obj.comment,
            4 : str(num_modules),
            5 : str(0),
            6 : str(0)
        }
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        return False


class BomEquivalentsModel(wx.dataview.PyDataViewModel):
    def __init__(self, part):
        super(BomEquivalentsModel, self).__init__()
        
        self.part = part
        self.parts = {}
        
        if part is None:
            return

        # load parts
        to_add = []
        for id in part.parts:
            to_add.append(id)
            
        # recursive load subparts
        for id in to_add:
            if self.parts.has_key(id)==False:
                subpart = PartsQuery().get(id)[0]
                self.parts[id] = subpart
                for subid in subpart.parts:
                    to_add.append(subid)
        
    def GetColumnCount(self):
        return 3

    def GetColumnType(self, col):
        mapper = { 
            0 : 'long',
            1 : 'string',
            2 : 'string',
            3 : 'string',
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for id in self.parts:
                children.append(self.ObjectToItem(self.parts[id]))
            return len(self.parts)
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        vMap = { 
            0 : str(obj.id),
            1 : obj.name,
            2 : obj.description,
            3 : obj.comment,
        }
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        return False


class PartDistributorsDataModel(wx.dataview.PyDataViewModel):
    def __init__(self, parts, num_modules, board_number, view_all):
        super(PartDistributorsDataModel, self).__init__()
        
        self.parts = parts
        self.data = []
        self.board_number = board_number
        self.view_all = view_all
        self.num_modules = num_modules

        # get requested parts number
        parts_num = self.board_number*self.num_modules
        
        # calculate pricing elements
        for part in parts:
            if view_all==False:
                distributors = self.BestPrice(part.distributors)
            else:
                distributors = part.distributors
                
            for distributor in distributors:
                distributor.part = part
                # convert currencies
                try:
                    distributor.unit_price = currency.convert(distributor.unit_price, distributor.currency, configuration.base_currency)
                    distributor.currency = configuration.base_currency
                except:
                    # no convertion in case of an error
                    pass

                # number of packages to buy
                distributor.buy_packages = int(parts_num/distributor.packaging_unit)
                if divmod(parts_num, distributor.packaging_unit)[1]>0:
                    distributor.buy_packages = distributor.buy_packages+1
                if distributor.buy_packages<distributor.quantity:
                    distributor.buy_packages = distributor.quantity/distributor.packaging_unit
                # price to pay
                distributor.buy_price = distributor.buy_packages*distributor.item_price()
                
                self.data.append(distributor)
    
    def MatchPrices(self, distributors):
        # find prices that matches requested part number, remove the rest
        res_distributors = []
        # TODO
        source_distributors = {}
        for distributor in distributors:
            if source_distributors.has_key(distributor.distributor.name)==False:
                source_distributors[distributor.distributor.name] = []
            source_distributors[distributor.distributor.name].append(distributor)

        return res_distributors
    
    def BestPrice(self, distributors):
        # find the best price for the part
        res_distributors = []
        
        # get requested parts number
        parts_num = self.board_number*self.num_modules
        
        source_distributors = {}
        for distributor in distributors:
            if source_distributors.has_key(distributor.distributor.name)==False:
                source_distributors[distributor.distributor.name] = []
            source_distributors[distributor.distributor.name].append(distributor)

        for distributor_name in source_distributors:
            prices = source_distributors[distributor_name]
            best_price = None
            for price in prices:
                # check if price is better than current best price
                # Note: sometimes buying a pack can be cheaper than buying items at unit price
                
                # compute number of packages to buy
                buy_packages = int(parts_num/price.packaging_unit)
                if divmod(parts_num, price.packaging_unit)[1]>0:
                    buy_packages = buy_packages+1
                if buy_packages<price.quantity:
                    buy_packages = price.quantity
                
                buy_price = buy_packages*price.item_price()

                if best_price is None:
                    best_price = [price, buy_price]
                
                if buy_price<best_price[1] and buy_packages>=price.quantity:
                    best_price = [price, buy_price]
            # add best found price for distributor
            res_distributors.append(best_price[0])

        return res_distributors
    
    def GetColumnCount(self):
        return 9

    def GetColumnType(self, col):
        mapper = { 
            0 : 'string',
            1 : 'string',
            2 : 'long',
            3 : 'double',
            4 : 'long',
            5 : 'long',
            6 : 'double',
            7 : 'double',
            8 : 'string',
            9 : 'string',
         }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for data in self.data:
                children.append(self.ObjectToItem(data))
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
            0 : obj.part.name,
            1 : distributor,
            2 : str(obj.buy_packages*obj.packaging_unit),
            3 : str(obj.buy_price),
            4 : str(obj.packaging_unit),
            5 : str(obj.quantity),
            6 : str(obj.item_price()),
            7 : str(obj.unit_price),
            8 : obj.currency,
            9 : obj.sku,
        }
            
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        return False


class WishPartsModel(wx.dataview.PyDataViewModel):
    def __init__(self, wish_parts):
        super(WishPartsModel, self).__init__()
        
        self.wish_parts = wish_parts
        
    def GetColumnCount(self):
        return 7

    def GetColumnType(self, col):
        mapper = { 
            0 : 'string',
            1 : 'string',
            2 : 'string',
            3 : 'long',
            4 : 'float',
            5 : 'float',
            6 : 'string',
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for wish in self.wish_parts:
                children.append(self.ObjectToItem(wish))
            return len(self.wish_parts)
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        
        quantity = obj[0]
        part = obj[1]
        price = obj[2]
        
        vMap = { 
            0 : part.name,
            1 : price.distributor.name,
            2 : price.sku,
            3 : str(price.packaging_unit),
            4 : str(quantity),
            5 : str(quantity*price.unit_price),
            6 : price.currency,
        }
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        return False

class BuyFrame(PanelBuy): 
    def __init__(self, parent):
        super(BuyFrame, self).__init__(parent)

        # create bom parts list
        self.bom_parts_model = BomPartsModel()
        self.tree_bom_parts.AssociateModel(self.bom_parts_model)
        # add default columns
        self.tree_bom_parts.AppendTextColumn("Id", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_parts.AppendTextColumn("Name", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_parts.AppendTextColumn("Description", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_parts.AppendTextColumn("Comment", 3, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_parts.AppendTextColumn("Modules", 4, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_parts.AppendTextColumn("Needed", 5, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_bom_parts.AppendTextColumn("Approvisioned", 6, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_bom_parts.Columns:
            c.Sortable = True

        # create bom parts list
        self.part_equivalents_model = BomEquivalentsModel(None)
        self.tree_part_equivalents.AssociateModel(self.part_equivalents_model)
        # add default columns
        self.tree_part_equivalents.AppendTextColumn("Id", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_part_equivalents.AppendTextColumn("Name", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_part_equivalents.AppendTextColumn("Description", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_part_equivalents.AppendTextColumn("Comment", 3, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_part_equivalents.Columns:
            c.Sortable = True

        # create octoparts list
        self.distributors_model = PartDistributorsDataModel([], 0, 0, False)
        self.tree_distributors.AssociateModel(self.distributors_model)
        # add default columns
        self.tree_distributors.AppendTextColumn("Part", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Distributor", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Amount To Buy", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Buy Price", 3, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Packaging Unit", 4, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Quantity", 5, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Price", 6, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Price per Item", 7, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("Currency", 8, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_distributors.AppendTextColumn("SKU", 9, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_distributors.Columns:
            c.Sortable = True

        # create wish parts list
        self.wish_parts = []
        self.wish_parts_model = WishPartsModel(self.wish_parts)
        self.tree_wish_parts.AssociateModel(self.wish_parts_model)
        # add default columns
        self.tree_wish_parts.AppendTextColumn("Part", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_wish_parts.AppendTextColumn("Distributor", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_wish_parts.AppendTextColumn("SKU", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_wish_parts.AppendTextColumn("Packaging Unit", 3, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_wish_parts.AppendTextColumn("Amount", 4, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_wish_parts.AppendTextColumn("Buy Price", 5, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_wish_parts.AppendTextColumn("Currency", 6, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_part_equivalents.Columns:
            c.Sortable = True

    def load(self):
        self.loadBomParts()
        self.loadPartEquivalents()
        self.loadDistributors()
        
    def loadBomParts(self):
        self.bom_parts_model.Cleared()
        self.bom_parts_model = BomPartsModel()
        self.tree_bom_parts.AssociateModel(self.bom_parts_model)

    def loadPartEquivalents(self):
        item = self.tree_bom_parts.GetSelection()
        part = None
        if item:
            part = self.bom_parts_model.ItemToObject(item)

        self.part_equivalents_model.Cleared()
        self.part_equivalents_model = BomEquivalentsModel(part)
        self.tree_part_equivalents.AssociateModel(self.part_equivalents_model)
        self.tree_part_equivalents.SelectAll()
    
    def loadWhishParts(self):
        self.wish_parts_model.Cleared()
        self.wish_parts_model = WishPartsModel(self.wish_parts)
        self.tree_wish_parts.AssociateModel(self.wish_parts_model)
    
    def loadTotalPrice(self):
        total = 0
        
        for wish in self.wish_parts:
            total = total+wish[2].buy_price
        self.text_total_price.SetValue(str(total))
        self.static_total_price.SetLabel(configuration.base_currency)
        
    def loadDistributors(self):
        parts = []
        
        item = self.tree_bom_parts.GetSelection()
        num_modules = 0
        if item:
            part = self.bom_parts_model.ItemToObject(item)
            num_modules = len(bom.part_modules[part.id])
            parts.append(part)
        
        try:
            for item in self.tree_part_equivalents.GetSelections():
                if item:
                    parts.append(self.part_equivalents_model.ItemToObject(item))
        except:
            pass
        
        self.distributors_model.Cleared()
        self.distributors_model = PartDistributorsDataModel(parts, num_modules, self.spin_board_number.GetValue(), self.menu_item_prices_view_all.IsChecked())
        self.tree_distributors.AssociateModel(self.distributors_model)
    
    def GetMenus(self):
        return [{'title': 'Prices', 'menu': self.menu_prices}]
    
    def OnTreeBomPartsSelectionChanged( self, event ):
        self.loadPartEquivalents()
        self.loadDistributors()
    
    def OnTreePartEquivalentsSelectionChanged( self, event ):
        self.loadDistributors()

    def OnTreeDistributorsSelectionChanged( self, event ):
        item = self.tree_distributors.GetSelection()
        distributor = None
        if item:
            distributor = self.distributors_model.ItemToObject(item)

        if distributor:
            self.spin_add_wish_parts.SetValue(distributor.buy_packages*distributor.packaging_unit)
        else:
            self.spin_add_wish_parts.SetValue(0)
            
    def OnMenuItem( self, event ):
        # events are not distributed by the frame so we distribute them manually
        if event.GetId()==self.menu_item_prices_view_all.GetId():
            self.OnMenuItemPricesViewAllSelection(event)
        elif event.GetId()==self.menu_item_prices_select_bestprice.GetId():
            self.OnMenuItemPricesSelectBestpriceSelection(event)
    
    def OnMenuItemPricesViewAllSelection( self, event ):
        self.loadDistributors()
    
    def OnMenuItemPricesSelectBestpriceSelection( self, event ):
        print "OnMenuItemPricesSelectBestpriceSelection"

    def OnSpinBoardNumberCtrl( self, event ):
        self.loadDistributors()

    def OnButtonAddWishPartsClick( self, event ):
        item = self.tree_distributors.GetSelection()
        distributor = None
        if item:
            distributor = self.distributors_model.ItemToObject(item)
        else:
            return
        
        # search if part already added for this distributor
        #TODO
        # calculate price for total items for the distributor
        #TODO
        self.wish_parts.append([self.spin_add_wish_parts.GetValue(), distributor.part, distributor])
        self.loadWhishParts()
        self.loadTotalPrice()
