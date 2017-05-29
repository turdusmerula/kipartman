import wx

class DropdownFrame(wx.PopupTransientWindow):
    def __init__( self, parent, frame ):
        super(DropdownFrame, self).__init__(parent)
        self.panel = frame(self)
        
        self.SetSize(0, 0, self.panel.GetSize().x, self.panel.GetSize().y)
    
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add( self.panel, 1, wx.EXPAND, 5 )
        self.SetSizer(sizer)
        self.Layout()

    def Dropdown(self):
        pos = self.Parent.GetScreenPosition()
        pos.y = pos.y+self.Parent.GetSize().y

#         for display in range(wx.Display.GetCount()):
#             screen = wx.Display(display).GetGeometry()
#             p = self.Parent.GetScreenPosition()
#             if p.x>=screen.left and p.x<=screen.right:
#                 screenSize = display.GetGeometry().GetSize()
#         print type(screenSize)
#         if pos.y+self.GetSize().y>screenSize.y:
#             pos.y = screenSize.y-self.GetSize().y
        
        screenSize = wx.Display(0).GetGeometry().GetSize()
        if pos.y+self.panel.GetSize().y>screenSize.y:
            pos.y = screenSize.y-self.panel.GetSize().y
        if pos.x+self.panel.GetSize().x>screenSize.x:
            pos.x = screenSize.x-self.panel.GetSize().x

        self.SetPosition(pos)
        self.Popup()

