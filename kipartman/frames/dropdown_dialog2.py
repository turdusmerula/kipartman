import wx

class DropdownDialog2(wx.Dialog):
    """
    Display a popup frame
    """
    
    def __init__( self, parent, frame, *args, **kwargs ):
        """
        Create a popup modal dialog window from frame
        :param parent: owner
        :param frame: type of frame to create
        :param initial: item to select by default
        Frame should contain a SetResult method allowing to set result and cancel callback 
        """
        super(DropdownDialog2, self).__init__(parent, style=wx.RESIZE_BORDER)
        self.panel = frame(self, *args, **kwargs)
        self.SetSize( self.panel.GetSize())
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add( self.panel, 1, wx.EXPAND, 5 )
        self.SetSizer(sizer)
        self.Layout()

    def DropDown(self):    
        pos = self.Parent.GetScreenPosition()
        pos.y = pos.y+self.Parent.GetSize().y
        
        screenSize = wx.Display(0).GetGeometry().GetSize()
        if pos.y+self.panel.GetSize().y>screenSize.y:
            pos.y = screenSize.y-self.panel.GetSize().y
        if pos.x+self.panel.GetSize().x>screenSize.x:
            pos.x = screenSize.x-self.panel.GetSize().x
        
        self.SetPosition(pos)

        return self.ShowModal()
    
    def DropHere(self, result_callback=None):
        pos = wx.GetMousePosition()

        screenSize = wx.Display(0).GetGeometry().GetSize()
        if pos.y+self.panel.GetSize().y>screenSize.y:
            pos.y = screenSize.y-self.panel.GetSize().y
        if pos.x+self.panel.GetSize().x>screenSize.x:
            pos.x = screenSize.x-self.panel.GetSize().x
        
        self.SetPosition(pos)

        return self.ShowModal()
