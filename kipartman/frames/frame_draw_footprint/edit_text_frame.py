from dialogs.draw_footprint.panel_edit_text import PanelEditText
import math

class EditTextFrame(PanelEditText): 
    def __init__(self, parent, render, text):
        super(EditTextFrame, self).__init__(parent)
        self.render = render
        self.text = text
        self.ShowText()
                
    def SetText(self, text):
        self.text = text
        self.ShowText()

    def ShowText(self):
        if self.text:
            if self.text.font.style=='normal':
                self.radio_style.SetSelection(0)
            elif self.text.font.style=='italic':
                self.radio_style.SetSelection(1)
            
            if self.text.orientation=='horizontal':
                self.radio_orientation.SetSelection(0)
            elif self.text.orientation=='vertical':
                self.radio_orientation.SetSelection(1)

            if self.text.visible==True:
                self.radio_display.SetSelection(0)
            else:
                self.radio_display.SetSelection(1)

            self.text_text.Value = str(self.text.value)

            self.text_pos_x.Value = str(self.text.pos.x)
            self.text_pos_y.Value = str(self.text.pos.y)
            self.text_width.Value = str(self.text.font.size.x)
            self.text_height.Value = str(self.text.font.size.y)
            self.text_thickness.Value = str(self.text.font.thickness)
            
    def UpdateText(self):
        self.text.value = self.text_text.Value

        if self.radio_style.GetSelection()==0:
            self.text.font.style = 'normal'
        elif self.radio_style.GetSelection()==1:
            self.text.font.style = 'italic'
        
        if self.radio_orientation.GetSelection()==0:
            self.text.orientation = 'horizontal'
        elif self.radio_orientation.GetSelection()==1:
            self.text.orientation = 'vertical'

        if self.radio_display.GetSelection()==0:
            self.text.visible = True
        elif self.radio_display.GetSelection()==1:
            self.text.visible = False

        try:
            self.text.pos.x = float(self.text_pos_x.Value)
        except Exception as e:
            print format(e)
            return
    
        try:
            self.text.pos.y = float(self.text_pos_y.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.text.font.size.x = float(self.text_width.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.text.font.size.y = float(self.text_height.Value)
        except Exception as e:
            print format(e)
            return

        try:
            self.text.font.thickness = float(self.text_thickness.Value)
        except Exception as e:
            print format(e)
            return

        self.text.Update()
        self.ShowText()
        self.render()

    def Update(self):
        self.ShowText()

    def onStyleRadioBox( self, event ):
        self.UpdateText()
    
    def onOrientationRadioBox( self, event ):
        self.UpdateText()
    
    def onDisplayRadioBox( self, event ):
        self.UpdateText()
    
    def onTextTextEnter( self, event ):
        self.UpdateText()
    
    def onPosXTextEnter( self, event ):
        self.UpdateText()
    
    def onPosYTextEnter( self, event ):
        self.UpdateText()
    
    def onWidthTextEnter( self, event ):
        self.UpdateText()
    
    def onHeightTextEnter( self, event ):
        self.UpdateText()
    
    def onThicknessTextEnter( self, event ):
        self.UpdateText()
    

