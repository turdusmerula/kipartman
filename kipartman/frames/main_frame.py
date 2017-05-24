from dialogs.dialog_main import DialogMain
from frames.parts_frame import PartsFrame
from frames.footprints_frame import FootprintsFrame


class MainFrame(DialogMain): 
    def __init__(self, parent): 
        DialogMain.__init__(self, parent)
        self.partsframe = PartsFrame(self.notebook)
        self.notebook.AddPage(self.partsframe, "parts", False)
        
        self.footprintsframe = FootprintsFrame(self.notebook)
        self.notebook.AddPage(self.footprintsframe, "footprints", False)
        #TODO: projects
        #TODO: providers
        #TODO: manufacturers
        self.partsframe.load()