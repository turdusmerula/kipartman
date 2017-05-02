from dialogs.panel_parts import PanelParts
from api.queries import PartCategoriesQuery

class PartsFrame(PanelParts): 
    def __init__(self, parent): 
        PanelParts.__init__(self, parent)

    def _loadCategories(self):
        request = PartCategoriesQuery()
        cats = request.get()
        for cat in cats:
            print cat
            
    def _loadParts(self):
        None

    # Virtual event handlers, overide them in your derived class
    def load(self): 
        self._loadCategories()
        self._loadParts()

