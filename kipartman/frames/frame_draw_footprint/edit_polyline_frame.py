from dialogs.draw_footprint.panel_edit_polyline import PanelEditPolyline

class EditPolylineFrame(PanelEditPolyline): 
    def __init__(self, parent, render, polyline):
        super(EditPolylineFrame, self).__init__(parent)
        self.render = render
        self.polyline = polyline
        self.ShowPolyline()
        
    def SetPolyline(self, polyline):
        self.polyline = polyline
        self.ShowPolyline()

    def ShowPolyline(self):
        if self.polyline:
            self.text_width.Value = str(self.polyline.width)
    
    def Update(self):
        self.ShowPolyline()
        
    def onWidthTextEnter( self, event ):
        self.polyline.width = float(self.text_width.Value)
        self.polyline.Update()
        self.render()
