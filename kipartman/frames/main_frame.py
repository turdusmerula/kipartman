from dialogs.dialog_main import DialogMain
from frames.buy_frame import BuyFrame
from frames.parts_frame import PartsFrame
from frames.symbols_frame import SymbolsFrame
from frames.footprints_frame import FootprintsFrame
from frames.distributors_frame import DistributorsFrame
from frames.manufacturers_frame import ManufacturersFrame
from frames.configuration_frame import ConfigurationFrame
from frames.storages_frame import StoragesFrame
from frames.project_frame import ProjectFrame
from helper.exception import print_stack
import os
import wx

class MainFrame(DialogMain): 
    def __init__(self, parent): 
        DialogMain.__init__(self, parent)
        
        self.cwd = os.getcwd()
        
        self.menus = self.menu_bar.GetMenus()

        self.pages = []
        self.partsframe = PartsFrame(self.notebook)
        self.symbolsframe = SymbolsFrame(self.notebook)
        self.footprintsframe = FootprintsFrame(self.notebook)
        self.distributorsframe = DistributorsFrame(self.notebook)
        self.manufacturersframe = ManufacturersFrame(self.notebook)
        self.storageframe = StoragesFrame(self.notebook)
 
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
            print_stack()
            pass

    def onMenuFileProjetSelection( self, event ):
        dlg = wx.FileDialog(
            self, message="Choose a kicad project file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard="Kicad project (*.pro)|*.pro",
                style=wx.FD_OPEN |
                wx.FD_FILE_MUST_EXIST |
                wx.FD_PREVIEW
        )
        dlg.SetFilterIndex(0)

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            os.chdir(self.cwd)
            project_frame = ProjectFrame(self, dlg.GetPath())
            project_frame.Show(True)

    def onMenuBuyPartsSelection( self, event ):
        os.chdir(self.cwd)
        buy_frame = BuyFrame(self)
        buy_frame.Show(True)

    def OnMenuItem( self, event ):
        self.pages[self.notebook.GetSelection()].OnMenuItem(event)

