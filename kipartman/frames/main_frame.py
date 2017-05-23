from dialogs.dialog_main import DialogMain
from frames.parts_frame import PartsFrame


class MainFrame(DialogMain): 
    def __init__(self, parent): 
        DialogMain.__init__(self, parent)
        self.partsframe = PartsFrame(self.notebook)
        self.notebook.AddPage(self.partsframe, "parts", False)
        #TODO: footprints
        #TODO: projects
        #TODO: providers
        #TODO: manufacturers
        self.partsframe.load()