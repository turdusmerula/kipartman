from dialogs.draw_footprint.panel_edit_circle import PanelEditCircle

class EditCircleFrame(PanelEditCircle): 
    def __init__(self, parent, render, circle):
        super(EditCircleFrame, self).__init__(parent)
        self.render = render
        self.circle = circle
        self.ShowCircle()
        
    def SetCircle(self, circle):
        self.circle = circle
        self.ShowCircle()

    def ShowCircle(self):
        if self.circle:
            self.text_width.Value = str(self.circle.width)
    
    def Update(self):
        self.ShowCircle()
        
    def onWidthTextEnter( self, event ):
        self.circle.width = float(self.text_width.Value)
        self.circle.Update()
        self.render()
