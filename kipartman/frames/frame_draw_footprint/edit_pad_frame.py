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

            self.text_angle.Value = str(-self.pad.angle*180./math.pi)
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
                self.text_offset_x.Enable(False)
                self.text_offset_x.Value = '0'
                self.text_offset_y.Enable(False)
                self.text_offset_y.Value = '0'
            else:
                self.text_size_y.Enable(True)
                self.text_offset_x.Enable(True)
                self.text_offset_y.Enable(True)
            
            if self.pad.type=='np_thru_hole':
                self.text_pad_to_die.Enable(False)
            else:
                self.text_pad_to_die.Enable(True)

            if self.pad.type=='np_thru_hole':
                self.text_name.Enable(False)
                self.text_name.Value = ''
            else:
                self.text_name.Enable(True)
                

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
            
            self.text_pad_clearance.value = str(self.pad.clearance)
            self.text_solder_mask_clearance.Value = str(self.pad.solder_mask_margin)
            self.text_solder_paste_clearance.Value = str(self.pad.solder_paste_margin)
            self.text_solder_paste_ratio_clearance.Value = str(self.pad.solder_paste_margin_ratio)
            
            if self.pad.zone_connect is None:
                self.choice_pad_connection.SetSelection(1)
            elif self.pad.zone_connect==0:
                self.choice_pad_connection.SetSelection(0)
            elif self.pad.zone_connect==1:
                self.choice_pad_connection.SetSelection(3)
            elif self.pad.zone_connect==2:
                self.choice_pad_connection.SetSelection(2)

            self.text_thermal_relief_width.Value = str(self.pad.thermal_width)
            self.text_thermal_relief_gap.Value = str(self.pad.thermal_gap)
            
            if "*.Cu" in self.pad.layers:
                self.choice_copper_layer.SetSelection(0)
            elif "F.Cu" in self.pad.layers:
                self.choice_copper_layer.SetSelection(1)
            elif "B.Cu" in self.pad.layers:
                self.choice_copper_layer.SetSelection(2)
            else:
                self.choice_copper_layer.SetSelection(3)
            
            self.check_f_adhes.SetValue(False) 
            self.check_b_adhes.SetValue(False) 
            if "*.Adhes" in self.pad.layers or "F.Adhes" in self.pad.layers:
                self.check_f_adhes.SetValue(True) 
            if "*.Adhes" in self.pad.layers or "B.Adhes" in self.pad.layers:
                self.check_b_adhes.SetValue(True) 
               
            self.check_f_paste.SetValue(False) 
            self.check_b_paste.SetValue(False) 
            if "*.Paste" in self.pad.layers or "F.Paste" in self.pad.layers:
                self.check_f_paste.SetValue(True) 
            if "*.Paste" in self.pad.layers or "B.Paste" in self.pad.layers:
                self.check_b_paste.SetValue(True) 

            self.check_f_silk.SetValue(False) 
            self.check_b_silk.SetValue(False) 
            if "*.Silk" in self.pad.layers or "F.Silk" in self.pad.layers:
                self.check_f_silk.SetValue(True) 
            if "*.Silk" in self.pad.layers or "B.Silk" in self.pad.layers:
                self.check_b_silk.SetValue(True) 

            self.check_f_mask.SetValue(False) 
            self.check_b_mask.SetValue(False) 
            if "*.Mask" in self.pad.layers or "F.Mask" in self.pad.layers:
                self.check_f_mask.SetValue(True) 
            if "*.Mask" in self.pad.layers or "B.Mask" in self.pad.layers:
                self.check_b_mask.SetValue(True) 

            self.check_dwgs_user.SetValue(False) 
            if "Dwgs.User" in self.pad.layers:
                self.check_dwgs_user.SetValue(True) 

            self.check_eco1_u.SetValue(False) 
            if "Eco1.U" in self.pad.layers:
                self.check_eco1_u.SetValue(True) 

            self.check_eco2_u.SetValue(False) 
            if "Eco2.U" in self.pad.layers:
                self.check_eco2_u.SetValue(True) 
                
    def UpdatePad(self):
        self.pad.name = self.text_name.Value

        if self.radio_shape.GetSelection()==0:
            self.pad.SetShape('rect')
        elif self.radio_shape.GetSelection()==1:
            self.pad.SetShape('trapezoid')
        elif self.radio_shape.GetSelection()==2:
            self.pad.SetShape('oval')
        elif self.radio_shape.GetSelection()==3:
            self.pad.SetShape('circle')

        if self.radio_type.GetSelection()==0:
            self.pad.SetType('smd')
        elif self.radio_type.GetSelection()==1:
            self.pad.SetType('thru_hole')
        elif self.radio_type.GetSelection()==2:
            self.pad.SetType('connect')
        elif self.radio_type.GetSelection()==3:
            self.pad.SetType('np_thru_hole')

        try:
            self.pad.angle = -float(self.text_angle.Value)*math.pi/180.
        except Exception as e:
            print format(e)
            return

        try:
            self.pad.pos.x = float(self.text_position_x.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.pad.pos.y = float(self.text_position_y.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.pad.size.x = float(self.text_size_x.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.pad.size.y = float(self.text_size_y.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.pad.offset.x = float(self.text_offset_x.Value)
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
            self.pad.die_length = float(self.text_pad_to_die.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.pad.trapezoidal_delta = float(self.text_pad_trapezoidal_delta.Value)
        except Exception as e:
            print format(e)
            return

        if self.choice_trapezoidal_direction.GetSelection()==0:
            self.pad.trapezoidal_direction = 'vert'
        else:
            self.pad.trapezoidal_direction = 'horz'

        try:
            self.pad.drill.x = float(self.text_drill_size_x.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.pad.drill.y = float(self.text_drill_size_y.Value)
        except Exception as e:
            print format(e)
            return


        try:
            self.pad.clearance = float(self.text_pad_clearance.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.pad.solder_mask_margin = float(self.text_solder_mask_clearance.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.pad.solder_paste_margin = float(self.text_solder_paste_clearance.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.pad.solder_paste_margin_ratio = float(self.text_solder_paste_ratio_clearance.Value)
        except Exception as e:
            print format(e)
            return


        if self.choice_pad_connection.GetSelection()==0:
            self.pad.zone_connect = 0
        elif self.choice_pad_connection.GetSelection()==1:
            self.pad.zone_connect = None
        elif self.choice_pad_connection.GetSelection()==2:
            self.pad.zone_connect = 2
        elif self.choice_pad_connection.GetSelection()==3:
            self.pad.zone_connect = 1

        try:
            self.pad.thermal_width = float(self.text_thermal_relief_width.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.pad.thermal_gap = float(self.text_thermal_relief_gap.Value)
        except Exception as e:
            print format(e)
            return

        self.pad.layers = []
        if self.choice_copper_layer.GetSelection()==0:
            self.pad.layers.append("*.Cu")
        elif self.choice_copper_layer.GetSelection()==1:
            self.pad.layers.append("F.Cu")
        elif self.choice_copper_layer.GetSelection()==2:
            self.pad.layers.append("B.Cu")

        if self.check_f_adhes.GetValue() and self.check_b_adhes.GetValue():
            self.pad.layers.append("*.Adhes")
        elif self.check_f_adhes.GetValue():
            self.pad.layers.append("F.Adhes")
        elif self.check_b_adhes.GetValue():
            self.pad.layers.append("B.Adhes")
            
        if self.check_f_paste.GetValue() and self.check_b_paste.GetValue():
            self.pad.layers.append("*.Paste")
        elif self.check_f_paste.GetValue():
            self.pad.layers.append("F.Paste")
        elif self.check_b_paste.GetValue():
            self.pad.layers.append("B.Paste")

        if self.check_f_silk.GetValue() and self.check_b_silk.GetValue():
            self.pad.layers.append("*.Silk")
        elif self.check_f_silk.GetValue():
            self.pad.layers.append("F.Silk")
        elif self.check_b_silk.GetValue():
            self.pad.layers.append("B.Silk")

        if self.check_f_mask.GetValue() and self.check_b_mask.GetValue():
            self.pad.layers.append("*.Mask")
        elif self.check_f_mask.GetValue():
            self.pad.layers.append("F.Mask")
        elif self.check_b_mask.GetValue():
            self.pad.layers.append("B.Mask")

        if self.check_dwgs_user.GetValue():
            self.pad.layers.append("Dwgs.User")
            
        if self.check_eco1_u.GetValue():
            self.pad.layers.append("Eco1.U")

        if self.check_eco2_u.GetValue():
            self.pad.layers.append("Eco2.U")

        self.pad.Select()
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
    
    def onTextThermalReliefGapTextEnter( self, event ):
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
    

    

