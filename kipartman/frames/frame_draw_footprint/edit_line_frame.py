from dialogs.draw_footprint.panel_edit_line import PanelEditLine
import wx

class EditLineFrame(PanelEditLine): 
    def __init__(self, parent, render, line):
        super(EditLineFrame, self).__init__(parent)
        self.render = render
        self.line = line
        self.ShowLine(line)
        
    def SetLine(self, line):
        self.line = line
        self.ShowGrid(line)

    def ShowLine(self, symbol):
        if self.line:
            self.text_angle.Value = str(self.line.angle)
    
    def Update(self):
        self.ShowLine(self.line)
        
    def onAngleText( self, event ):
        self.line.angle = float(self.text_angle.Value)
        self.line.Update()
        self.render()
