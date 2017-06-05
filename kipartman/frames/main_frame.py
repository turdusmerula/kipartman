from dialogs.dialog_main import DialogMain
from frames.parts_frame import PartsFrame
from frames.footprints_frame import FootprintsFrame
from frames.distributors_frame import DistributorsFrame


class MainFrame(DialogMain): 
    def __init__(self, parent): 
        DialogMain.__init__(self, parent)
        self.partsframe = PartsFrame(self.notebook)
        self.notebook.AddPage(self.partsframe, "Parts", False)
        
        self.footprintsframe = FootprintsFrame(self.notebook)
        self.notebook.AddPage(self.footprintsframe, "Footprints", False)

        self.distributorsframe = DistributorsFrame(self.notebook)
        self.notebook.AddPage(self.distributorsframe, "Distributors", False)
        
        #TODO: projects
        #TODO: manufacturers