from dialogs.draw_footprint.panel_edit_pad import PanelEditPad
import wx

class EditPadFrame(PanelEditPad): 
    def __init__(self, parent, render, pad):
        super(EditPadFrame, self).__init__(parent)
        self.render = render
        self.pad = pad
        self.ShowPad(pad)
        
    def SetPad(self, pad):
        self.pad = pad
        self.ShowPad(pad)

    def ShowPad(self, symbol):
        if self.pad:
            pass
        
    def onRadioShapeRadioBox( self, event ):
        event.Skip()
    
    def onRadioTypeRadioBox( self, event ):
        event.Skip()

    def onPadText( self, event ):
        event.Skip()
    
    def onPositionXText( self, event ):
        event.Skip()
    
    def onPositionYText( self, event ):
        event.Skip()
    
    def onSizeXText( self, event ):
        event.Skip()
    
    def onSizeYText( self, event ):
        event.Skip()
    

