import wx

class DropdownMenu(object):
    """
    Display a popup menu from parent position
    """
    
    def __init__( self, parent, menu, *args, **kwargs ):
        """
        Create a popup menu
        :param parent: owner
        :param menu: menu to popup
        """
        super(DropdownMenu, self).__init__()
        self.parent = parent
        self.menu = menu

    def Dropdown(self):    
        pos = self.parent.GetPosition()
#         pos.y = pos.y+self.parent.GetSize().y
        
#         screenSize = wx.Display(0).GetGeometry().GetSize()
#         if pos.y+self.parent.GetSize().y>screenSize.y:
#             pos.y = screenSize.y-self.parent.GetSize().y
#         if pos.x+self.parent.GetSize().x>screenSize.x:
#             pos.x = screenSize.x-self.parent.GetSize().x

        return self.parent.GetPopupMenuSelectionFromUser(self.menu)
