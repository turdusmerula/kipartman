from dialogs.dialog_main import DialogMain
from frames.buy_frame import BuyFrame
from frames.parts_frame import PartsFrame
from frames.symbols_frame import SymbolsFrame
from frames.footprints_frame import FootprintsFrame
from frames.distributors_frame import DistributorsFrame
from frames.manufacturers_frame import ManufacturersFrame
from frames.bom_frame import BomFrame
from frames.configuration_frame import ConfigurationFrame
from frames.storages_frame import StoragesFrame

import wx

class MainFrame(DialogMain): 
    def __init__(self, parent): 
        DialogMain.__init__(self, parent)
        
        self.menus = self.menu_bar.GetMenus()

        self.pages = []
        self.partsframe = PartsFrame(self.notebook)
        self.symbolsframe = SymbolsFrame(self.notebook)
        self.footprintsframe = FootprintsFrame(self.notebook)
        self.distributorsframe = DistributorsFrame(self.notebook)
        self.manufacturersframe = ManufacturersFrame(self.notebook)
        self.storageframe = StoragesFrame(self.notebook)
        self.buyframe = BuyFrame(self.notebook)
        self.bomframe = BomFrame(self.notebook)
 
        self.pages.append(self.partsframe)
        self.notebook.AddPage(self.partsframe, "Parts", False)
        self.pages.append(self.symbolsframe)
        self.notebook.AddPage(self.symbolsframe, "Symbols", False)
        self.pages.append(self.footprintsframe)
        self.notebook.AddPage(self.footprintsframe, "Footprints", False)
        self.pages.append(self.distributorsframe)
        self.notebook.AddPage(self.distributorsframe, "Distributors", False)
        self.pages.append(self.manufacturersframe)
        self.notebook.AddPage(self.manufacturersframe, "Manufacturers", False)
        self.pages.append(self.storageframe)
        self.notebook.AddPage(self.storageframe, "Storage locations", False)
        self.pages.append(self.bomframe)
        self.notebook.AddPage(self.bomframe, "BOM", False)
        self.pages.append(self.buyframe)
        self.notebook.AddPage(self.buyframe, "Buy", False)

    def onMenuViewConfigurationSelection( self, event ):
        ConfigurationFrame(self).ShowModal()

    def onNotebookPageChanged( self, event ):
        if self.menus is None:
            return
        if self.menu_bar is None:
            return
        
        self.menu_bar.SetMenus(self.menus)

        try:
            page = self.pages[self.notebook.GetSelection()]
            self.page_menus = page.GetMenus()
            
            for menu in self.page_menus:
                self.menu_bar.Insert(len(self.menu_bar.GetMenus())-1, menu['menu'], menu['title'])
                for menu_item in menu['menu'].GetMenuItems():
                    self.Bind( wx.EVT_MENU, self.OnMenuItem, id = menu_item.GetId() )
        except:
            pass
    
    def OnMenuItem( self, event ):
        self.pages[self.notebook.GetSelection()].OnMenuItem(event)
