from dialogs.panel_test import PanelTest
import wx

class TestFrame(PanelTest): 
    def __init__(self, parent): 
        super(TestFrame, self).__init__(parent)
        
    def activate(self):
        pass

    def set_panel(self, panel):
        self.sizer_test.Add( panel, 0, wx.ALL|wx.EXPAND, 5 )
        self.SetSizer( self.sizer_test )
        self.Layout()
