from dialogs.draw_footprint.panel_edit_grid import PanelEditGrid
import wx

class EditGridFrame(PanelEditGrid): 
    def __init__(self, parent, render, grid):
        super(EditGridFrame, self).__init__(parent)
        self.render = render
        self.grid = grid
        self.ShowGrid(grid)
        
    def SetGrid(self, grid):
        self.grid = grid
        self.ShowGrid(grid)

    def ShowGrid(self, symbol):
        if self.grid:
            self.spin_x_count.Value = str(self.grid.count.x)
            self.spin_y_count.Value = str(self.grid.count.y)
            self.text_spacing_x.Value = str(self.grid.spacing.x)
            self.text_spacing_y.Value = str(self.grid.spacing.y)
    
    def onSpinXCountCtrl( self, event ):
        self.grid.count.x = int(self.spin_x_count.Value)
        self.grid.Update()
        self.render()
        
    def onSpinYCountCtrl( self, event ):
        self.grid.count.y = int(self.spin_y_count.Value)
        self.grid.Update()
        self.render()
    
    def onTextSpacingXText( self, event ):
        self.grid.spacing.x = float(self.text_spacing_x.Value)
        self.grid.Update()
        self.render()
    
    def onTextSpacingYText( self, event ):
        self.grid.spacing.y = float(self.text_spacing_y.Value)
        self.grid.Update()
        self.render()
