from dialogs.draw_footprint.panel_edit_dimension import PanelEditDimension
import math
from helper.exception import print_stack
from helper.log import log

class EditDimensionFrame(PanelEditDimension): 
    def __init__(self, parent, render, dimension):
        super(EditDimensionFrame, self).__init__(parent)
        self.render = render
        self.dimension = dimension
        self.ShowDimension()
        
    def SetDimension(self, dimension):
        self.dimension = dimension
        self.ShowDimension(dimension)

    def ShowDimension(self):
        if self.dimension:
            self.text_size.Value = str(self.dimension.Size())
        
    def Update(self):
        self.ShowDimension()

    def onSizeTextEnter( self, event ):
        try:
            size = math.fabs(float(self.text_size.Value))
        except Exception as e:
            print_stack()
            log.error(format(e))
            return

        self.dimension.Value = str(size)
        self.dimension.SetSize(size)
        self.dimension.Update()
        self.render()
