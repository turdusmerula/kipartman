from dialogs.dialog_main import DialogMain
from frames.parts_frame import PartsFrame
from frames.footprints_frame import FootprintsFrame
from frames.distributors_frame import DistributorsFrame
from frames.manufacturers_frame import ManufacturersFrame
from frames.bom_frame import BomFrame
from frames.configuration_frame import ConfigurationFrame

import wx

class MainFrame(DialogMain): 
    def __init__(self, parent): 
        DialogMain.__init__(self, parent)
        
        self.partsframe = BomFrame(self.notebook)
        self.notebook.AddPage(self.partsframe, "BOM", False)
        
        self.partsframe = PartsFrame(self.notebook)
        self.notebook.AddPage(self.partsframe, "Parts", False)
        
        self.partsframe = wx.Panel(self.notebook)
        self.notebook.AddPage(self.partsframe, "Models", False)

        self.footprintsframe = FootprintsFrame(self.notebook)
        self.notebook.AddPage(self.footprintsframe, "Footprints", False)

        self.distributorsframe = DistributorsFrame(self.notebook)
        self.notebook.AddPage(self.distributorsframe, "Distributors", False)

        self.partsframe = ManufacturersFrame(self.notebook)
        self.notebook.AddPage(self.partsframe, "Manufacturers", False)
        
        #TODO: projects
        #TODO: manufacturers

    def onMenuViewConfigurationSelection( self, event ):
        ConfigurationFrame(self).ShowModal()
