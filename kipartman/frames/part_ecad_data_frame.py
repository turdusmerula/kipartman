from dialogs.panel_part_ecad_data import PanelPartEcadData
import helper.tree
import kicad.kicad_lib_file
import kicad.kicad_mod_file
from configuration import configuration
import os

class PartEcadDataFrame(PanelPartEcadData):
    def __init__(self, parent): 
        super(PartEcadDataFrame, self).__init__(parent)
        
        self.part = None
        
    def SetPart(self, part):
        self.part = part
        self.showData()

    def showData(self):
        self.showModel()
    
    def showModel(self):
        # download model
        if self.part and self.part.model:
            print "model", self.part.model
            url = os.path.join(configuration.kipartbase, 'file', self.part.model.storage_path)
            url = url.replace('\\','/') #Work around for running on Windows
            print "url", url