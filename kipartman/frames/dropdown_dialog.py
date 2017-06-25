import wx

class DropdownDialog(wx.Dialog):
    """
    Display a popup frame
    """
    
    def __init__( self, parent, frame, initial=None ):
        """
        Create a popup modal dialog window from frame
        :param parent: owner
        :param frame: type of frame to create
        :param initial: item to select by default
        Frame should contain a SetResult method allowing to set result and cancel callback 
        """

        super(DropdownDialog, self).__init__(parent, style=wx.RESIZE_BORDER)
        self.panel = frame(self, initial)
        
        self.SetSize(0, 0, self.panel.GetSize().x, self.panel.GetSize().y)
    
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add( self.panel, 1, wx.EXPAND, 5 )
        self.SetSizer(sizer)
        self.Layout()

    def Dropdown(self):
        pos = self.Parent.GetScreenPosition()
        pos.y = pos.y+self.Parent.GetSize().y
        
        screenSize = wx.Display(0).GetGeometry().GetSize()
        if pos.y+self.panel.GetSize().y>screenSize.y:
            pos.y = screenSize.y-self.panel.GetSize().y
        if pos.x+self.panel.GetSize().x>screenSize.x:
            pos.x = screenSize.x-self.panel.GetSize().x

        # callbacks from panel
        self.panel.SetResult(self.result, self.cancel)
        
        self.SetPosition(pos)
        self.ShowModal()
    
    def result(self, data):
        self.Destroy()

    def cancel(self):
        self.Destroy()