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
            if self.pad.shape=='rect':
                self.radio_shape.SetSelection(0)
            elif self.pad.shape=='trapezoid':
                self.radio_shape.SetSelection(1)
            elif self.pad.shape=='oval':
                self.radio_shape.SetSelection(2)
            elif self.pad.shape=='circle':
                self.radio_shape.SetSelection(3)
            else:
                self.radio_shape.SetSelection(0)
                
            if self.pad.type=='smd':
                self.radio_type.SetSelection(0)
            elif self.pad.type=='thru_hole':
                self.radio_type.SetSelection(1)
            elif self.pad.type=='connect':
                self.radio_type.SetSelection(2)
            elif self.pad.type=='np_thru_hole':
                self.radio_type.SetSelection(3)
            else:
                self.radio_type.SetSelection(0)

            self.text_angle.Value = str(self.pad.angle*180./math.pi)
            self.text_name.Value = self.pad.name
            self.text_position_x.Value = str(self.pad.pos.x)
            self.text_position_y.Value = str(self.pad.pos.y)
            self.text_size_x.Value = str(self.pad.size.x)
            self.text_size_y.Value = str(self.pad.size.y)
            self.text_offset_x.Value = str(self.pad.offset.x)
            self.text_offset_y.Value = str(self.pad.offset.y)
            self.text_pad_to_die.Value = str(self.pad.die_length)
            self.text_pad_trapezoidal_delta.Value = str(self.pad.trapezoidal_delta)
            
            if self.pad.trapezoidal_direction=='vert':
                self.choice_trapezoidal_direction.SetSelection(0)
            else:
                self.choice_trapezoidal_direction.SetSelection(1)
                
        
            if self.pad.shape=='trapezoid':
                self.text_pad_trapezoidal_delta.Enable(True)
                self.choice_trapezoidal_direction.Enable(True)
            else:
                self.text_pad_trapezoidal_delta.Enable(False)
                self.choice_trapezoidal_direction.Enable(False)

            if self.pad.shape=='circle':
                self.text_size_y.Enable(False)
            else:
                self.text_size_y.Enable(True)
            
            if self.pad.type=='np_thru_hole':
                self.text_pad_to_die.Enable(False)
            else:
                self.text_pad_to_die.Enable(True)


            if self.pad.drill_type=='circle':
                self.choice_drill_shape.SetSelection(0)
            else:
                self.choice_drill_shape.SetSelection(1)
            
            self.text_drill_size_x.Value = str(self.pad.drill.x)
            self.text_drill_size_y.Value = str(self.pad.drill.y)

            if self.pad.type=='thru_hole' or self.pad.type=='np_thru_hole':
                self.choice_drill_shape.Enable(True)
                self.text_drill_size_x.Enable(True)
                self.text_drill_size_y.Enable(True)
                if self.pad.drill_type=='circle':
                    self.text_drill_size_y.Enable(False)
            else:
                self.choice_drill_shape.Enable(False)
                self.text_drill_size_x.Enable(False)
                self.text_drill_size_y.Enable(False)
                
    def UpdatePad(self):
        self.pad.name = self.text_name.Value

        try:
            angle = float(self.text_angle.Value)*math.pi/180.
            self.pad.angle = angle
        except Exception as e:
            print format(e)
            return

        try:
            posx = float(self.text_position_x.Value)
            self.pad.pos.x = posx
        except Exception as e:
            print format(e)
            return

        try:
            posy = float(self.text_position_y.Value)
            self.pad.pos.y = posy
        except Exception as e:
            print format(e)
            return

        try:
            sizex = float(self.text_size_x.Value)
            self.pad.size.x = sizex
        except Exception as e:
            print format(e)
            return

        try:
            sizey = float(self.text_size_y.Value)
            self.pad.size.y = sizey
        except Exception as e:
            print format(e)
            return

        try:
            offsetx = float(self.text_offset_x.Value)
            self.pad.offset.x = offsetx
        except Exception as e:
            print format(e)
            return

        try:
            offsety = float(self.text_offset_y.Value)
            self.pad.offset.y = offsety
        except Exception as e:
            print format(e)
            return

        try:
            die_length = float(self.text_pad_to_die.Value)
            self.pad.die_length = die_length
        except Exception as e:
            print format(e)
            return

        try:
            trapezoid_delta = float(self.text_pad_trapezoidal_delta.Value)
            self.pad.trapezoid_delta = trapezoid_delta
        except Exception as e:
            print format(e)
            return

        if self.radio_shape.GetSelection()==0:
            self.pad.shape = 'rect'
        elif self.radio_shape.GetSelection()==1:
            self.pad.shape = 'trapezoid'
        elif self.radio_shape.GetSelection()==2:
            self.pad.shape = 'oval'
        elif self.radio_shape.GetSelection()==3:
            self.pad.shape = 'circle'

        if self.radio_type.GetSelection()==0:
            self.pad.type = 'smd'
        elif self.radio_type.GetSelection()==1:
            self.pad.type = 'thru_hole'
        elif self.radio_type.GetSelection()==2:
            self.pad.type = 'connect'
        elif self.radio_type.GetSelection()==3:
            self.pad.type = 'np_thru_hole'

        try:
            drill_size_x = float(self.text_drill_size_x.Value)
            self.pad.drill.x = drill_size_x
        except Exception as e:
            print format(e)
            return

        try:
            drill_size_y = float(self.text_drill_size_y.Value)
            self.pad.drill.y = drill_size_y
        except Exception as e:
            print format(e)
            return

        self.pad.Update()
        self.ShowPad()
        self.render()

    def Update(self):
        self.ShowPad()
        
    def onRadioShapeRadioBox( self, event ):
        self.UpdatePad()
    
    def onRadioTypeRadioBox( self, event ):
        self.UpdatePad()
    
    def onPadTextEnter( self, event ):
        self.UpdatePad()
    
    def onAngleTextEnter( self, event ):
        self.UpdatePad()
            
    def onPositionXTextEnter( self, event ):
        self.UpdatePad()
    
    def onPositionYTextEnter( self, event ):
        self.UpdatePad()
    
    def onSizeXTextEnter( self, event ):
        self.UpdatePad()
    
    def onSizeYTextEnter( self, event ):
        self.UpdatePad()

    def onShapeRadioBox( self, event ):
        self.UpdatePad()
    
    def onTypeRadioBox( self, event ):
        self.UpdatePad()
        
    def onOffsetXTextEnter( self, event ):
        self.UpdatePad()
    
    def onOffsetYTextEnter( self, event ):
        self.UpdatePad()
    
    def onPadToDieTextEnter( self, event ):
        self.UpdatePad()
    
    def onTrapezoidalDeltaTextEnter( self, event ):
        self.UpdatePad()
    
    def onTrapezoidalDirectionChoice( self, event ):
        self.UpdatePad()
    
    def onDrillShapeChoice( self, event ):
        self.UpdatePad()
    
    def onDrillSizeXTextEnter( self, event ):
        self.UpdatePad()
    
    def onDrillSizeYTextEnter( self, event ):
        self.UpdatePad()
    
    def onPadClearanceTextEnter( self, event ):
        self.UpdatePad()
    
    def onSolderMaskClearanceTextEnter( self, event ):
        self.UpdatePad()
    
    def onTextSolderPasteClearanceTextEnter( self, event ):
        self.UpdatePad()
    
    def onSolderPasteRatioClearanceTextEnter( self, event ):
        self.UpdatePad()
    
    def onPadConnectionChoice( self, event ):
        self.UpdatePad()
    
    def onThermalReliefWidthTextEnter( self, event ):
        self.UpdatePad()
    
    def onTextThermalReliefHeightTextEnter( self, event ):
        self.UpdatePad()
    
    def onCopperLayerChoice( self, event ):
        self.UpdatePad()
    
    def onFAdhesCheckBox( self, event ):
        self.UpdatePad()
    
    def onBAdhesCheckBox( self, event ):
        self.UpdatePad()
    
    def onFPasteCheckBox( self, event ):
        self.UpdatePad()
    
    def onBPasteCheckBox( self, event ):
        self.UpdatePad()
    
    def onFSilkCheckBox( self, event ):
        self.UpdatePad()
    
    def onBSilkCheckBox( self, event ):
        self.UpdatePad()
    
    def onFMaskCheckBox( self, event ):
        self.UpdatePad()
    
    def onBMaskCheckBox( self, event ):
        self.UpdatePad()
    
    def onDwgsUserCheckBox( self, event ):
        self.UpdatePad()
    
    def onEco1UCheckBox( self, event ):
        self.UpdatePad()
    
    def onEco2UCheckBox( self, event ):
        self.UpdatePad()
    

    

