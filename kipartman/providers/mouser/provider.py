from providers.provider import Provider


class MouserProvider(Provider):
    name = "Mouser"
    
    has_search_part = False
    
    def __init__(self):
        super(MouserProvider, self).__init__()
        
    def CheckConnection(self):
        pass
    
    def SearchPart(self, text):
        return []