from dialogs.draw_footprint.panel_edit_pad import PanelEditPad
import wx
import math

class EditPadFrame(PanelEditPad): 
    def __init__(self, parent, render, pad):
        super(EditPadFrame, self).__init__(parent)
        self.render = render
        self.pad = pad
        self.ShowPad()
        
    def SetPad(self, pad):
        self.pad = pad
        self.ShowPad()

    def ShowPad(self):
        if self.pad:
            self.text_angle.Value = str(self.pad.angle*180./math.pi)
            self.text_name.Value = self.pad.name
            self.text_position_x.Value = str(self.pad.pos.x)
            self.text_position_y.Value = str(self.pad.pos.y)
            self.text_size_x.Value = str(self.pad.size.x)
            self.text_size_y.Value = str(self.pad.size.y)

    def Update(self):
        self.ShowPad()

    def onRadioShapeRadioBox( self, event ):
        event.Skip()
    
    def onRadioTypeRadioBox( self, event ):
        event.Skip()
    
    def onPadTextEnter( self, event ):
        self.pad.name = self.text_name.Value
        self.pad.Update()
        self.render()
    
    def onAngleTextEnter( self, event ):
        try:
            angle = float(self.text_angle.Value)*math.pi/180.
        except Exception as e:
            print format(e)
            return
        self.pad.angle = angle
        self.pad.Update()
        self.render()
            
    def onPositionXTextEnter( self, event ):
        try:
            posx = float(self.text_position_x.Value)
        except Exception as e:
            print format(e)
            return
        self.pad.pos.x = posx
        self.pad.Update()
        self.render()
    
    def onPositionYTextEnter( self, event ):
        try:
            posy = float(self.text_position_y.Value)
        except Exception as e:
            print format(e)
            return
        self.pad.pos.y = posy
        self.pad.Update()
        self.render()
    
    def onSizeXTextEnter( self, event ):
        try:
            sizex = float(self.text_size_x.Value)
        except Exception as e:
            print format(e)
            return
        self.pad.size.x = sizex
        self.pad.Update()
        self.render()
    
    def onSizeYTextEnter( self, event ):
        try:
            sizey = float(self.text_size_y.Value)
        except Exception as e:
            print format(e)
            return
        self.pad.size.y = sizey
        self.pad.Update()
        self.render()
    

