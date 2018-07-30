from dialogs.draw_footprint.panel_edit_dimension import PanelEditDimension
import math

class EditDimensionFrame(PanelEditDimension): 
    def __init__(self, parent, render, dimension):
        super(EditDimensionFrame, self).__init__(parent)
        self.render = render
        self.dimension = dimension
        self.ShowDimension(dimension)
        
    def SetDimension(self, dimension):
        self.dimension = dimension
        self.ShowDimension(dimension)

    def ShowDimension(self, symbol):
        if self.dimension:
            self.text_size.Value = str(self.dimension.Size())
        
    def onTextSizeText( self, event ):
        self.dimension.Value = str(math.fabs(float(self.text_size.Value)))
        self.dimension.SetSize(float(self.text_size.Value))
        self.dimension.Update()
        self.render()
