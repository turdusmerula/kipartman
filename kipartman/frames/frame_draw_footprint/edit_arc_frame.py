from dialogs.draw_footprint.panel_edit_arc import PanelEditArc

class EditArcFrame(PanelEditArc): 
    def __init__(self, parent, render, arc):
        super(EditArcFrame, self).__init__(parent)
        self.render = render
        self.arc = arc
        self.ShowArc()
        
    def SetArc(self, arc):
        self.arc = arc
        self.ShowArc()

    def ShowArc(self):
        if self.arc:
            self.text_width.Value = str(self.arc.width)
    
    def Update(self):
        self.ShowArc()
        
    def onWidthTextEnter( self, event ):
        self.arc.width = float(self.text_width.Value)
        self.arc.Update()
        self.render()
