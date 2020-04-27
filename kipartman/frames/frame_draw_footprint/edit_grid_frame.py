from dialogs.draw_footprint.panel_edit_grid import PanelEditGrid
import wx
import math
from helper.exception import print_stack
from helper.log import log

class EditGridFrame(PanelEditGrid): 
    def __init__(self, parent, render, grid):
        super(EditGridFrame, self).__init__(parent)
        self.render = render
        self.grid = grid
        self.ShowGrid()
        
    def SetGrid(self, grid):
        self.grid = grid
        self.ShowGrid()

    def ShowGrid(self):
        if self.grid:
            self.spin_x_count.Value = str(self.grid.count.x)
            self.spin_y_count.Value = str(self.grid.count.y)
            self.text_spacing_x.Value = str(self.grid.spacing.x)
            self.text_spacing_y.Value = str(self.grid.spacing.y)
    
    def Update(self):
        self.ShowGrid()

    def onSpinXCountCtrl( self, event ):
        self.grid.count.x = int(self.spin_x_count.Value)
        self.grid.Update()
        self.render()
    
    def onSpinYCountCtrl( self, event ):
        self.grid.count.y = int(self.spin_y_count.Value)
        self.grid.Update()
        self.render()

    def onSpinXCountTextEnter( self, event ):
        self.grid.count.x = int(self.spin_x_count.Value)
        self.grid.Update()
        self.render()
    
    def onSpinYCountTextEnter( self, event ):
        self.grid.count.y = int(self.spin_y_count.Value)
        self.grid.Update()
        self.render()
    
    def onAngleTextEnter( self, event ):
        try:
            angle = float(self.text_angle.Value)*math.pi/180.
        except Exception as e:
            print_stack()
            log.error(format(e))
            return
        self.grid.angle = angle
        self.grid.Update()
        self.render()
    
    def onSpacingXTextEnter( self, event ):
        self.grid.spacing.x = float(self.text_spacing_x.Value)
        self.grid.Update()
        self.render()
    
    def onSpacingYTextEnter( self, event ):
        self.grid.spacing.y = float(self.text_spacing_y.Value)
        self.grid.Update()
        self.render()
