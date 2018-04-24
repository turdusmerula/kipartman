from dialogs.panel_select_symbol import PanelSelectSymbol
import helper.tree
import rest
import wx

class DataModelCategoryPath(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(DataModelCategoryPath, self).__init__()
        self.category = category
    
    def GetValue(self, col):
        if self.category:
            path = self.category.path
        else:
            path = "/"
        if col==0   :
            return path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
            return True
        return False
    
class DataModelSymbol(helper.tree.TreeItem):
    def __init__(self, symbol):
        super(DataModelSymbol, self).__init__()
        self.symbol = symbol
            
    def GetValue(self, col):
        vMap = { 
            0 : self.symbol.name,
            1 : self.symbol.description,
        }
        return vMap[col]


class TreeManagerSymbols(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerSymbols, self).__init__(tree_view)

    def FindSymbol(self, symbol_id):
        for data in self.data:
            if isinstance(data, DataModelSymbol) and data.symbol.id==symbol_id:
                return data
        return None


class SelectSymbolFrame(PanelSelectSymbol):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectSymbolFrame, self).__init__(parent)
        
        # create symbols list
        self.tree_symbols_manager = TreeManagerSymbols(self.tree_symbols)
        self.tree_symbols_manager.AddTextColumn("Name")
        self.tree_symbols_manager.AddTextColumn("Description")
        
        self.search_filter = None
        self.search_symbol.Value = ''
        self.load()
        
        if initial:
            self.tree_symbols.Select(self.tree_symbols_manager.ObjectToItem(self.tree_symbols_manager.FindSymbol(initial.id)))
        
        # set result functions
        self.cancel = None
        self.result = None

    def load(self):
        try:
            #self.loadSymbols()
            pass
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def loadSymbols(self):
        # clear all
        self.tree_symbols_manager.ClearItems()
        
        # load parts
        if self.search_filter:
            symbols = rest.api.find_symbols(search=self.search_filter)
        else:
            symbols = rest.api.find_symbols()
            
        # load categories
        categories = {}
        for symbol in symbols:
            if symbol.category:
                category_name = symbol.category.path
            else:
                category_name = "/"

            if categories.has_key(category_name)==False:
                categories[category_name] = DataModelCategoryPath(symbol.category)
                self.tree_symbols_manager.AppendItem(None, categories[category_name])
            self.tree_symbols_manager.AppendItem(categories[category_name], DataModelSymbol(symbol))
        
        for category in categories:
            self.tree_symbols_manager.Expand(categories[category])

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
    # Virtual event handlers, overide them in your derived class
    def onTreeModelsSelectionChanged( self, event ):
        event.Skip()
    
    def onButtonCancelClick( self, event ):
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        symbol = self.tree_symbols_manager.ItemToObject(self.tree_symbols.GetSelection())
        if isinstance(symbol, DataModelSymbol) and self.result:
            self.result(symbol.symbol)

    def onSearchSymbolCancel( self, event ):
        self.search_filter = None
        self.load()
    
    def onSearchSymbolButton( self, event ):
        self.search_filter = self.search_symbol.Value
        self.load()
    
    def onSearchSymbolEnter( self, event ):
        self.search_filter = self.search_symbol.Value
        self.load()
