from dialogs.draw_footprint.panel_edit_angle import PanelEditAngle
import math

class EditAngleFrame(PanelEditAngle): 
    def __init__(self, parent, render, angle):
        super(EditAngleFrame, self).__init__(parent)
        self.render = render
        self.angle = angle
        self.ShowAngle()
                
    def SetAngle(self, angle):
        self.angle = angle
        self.ShowAngle()

    def ShowAngle(self):
        if self.angle:
            self.text_angle.Value = str(self.angle.Angle()*180./math.pi)
        
    def Update(self):
        self.ShowAngle()

    def onAngleTextEnter( self, event ):
        try:
            angle = float(self.text_angle.Value)*math.pi/180.
        except Exception as e:
            print format(e)
            return
        self.angle.SetAngle(angle)
        self.angle.Update()
        self.render()
        
        self.text_angle.Value = str(self.angle.Angle()*180./math.pi)                
