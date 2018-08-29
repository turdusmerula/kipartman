from dialogs.draw_footprint.panel_edit_footprint import PanelEditFootprint

class EditFootprintFrame(PanelEditFootprint): 
    def __init__(self, parent, render, footprint):
        super(EditFootprintFrame, self).__init__(parent)
        self.render = render
        self.footprint = footprint
        self.ShowFootprint()
        
    def SetFootprint(self, footprint):
        self.footprint = footprint
        self.ShowFootprint()

    def ShowFootprint(self):
        if self.footprint:
            self.text_name.Value = self.footprint.footprint_name
            self.text_timestamp.Value = self.footprint.footprint_timestamp
            self.text_descr.Value = self.footprint.footprint_descr
            self.text_tags.Value = ""
            for tag in self.footprint.footprint_tags:
                if self.text_tags.Value!='':
                    self.text_tags.Value = self.text_tags.Value+' '
                self.text_tags.Value = self.text_tags.Value+tag
            
    def Update(self):
        self.footprint.SetFootprintName(self.text_name.Value)
        self.footprint.SetFootprintTimestamp(self.text_timestamp.Value)
        self.footprint.SetFootprintDescr(self.text_descr.Value)

        tags = []
        for tag in self.text_tags.Value.split(' '):
            tags.append(tag)
        self.footprint.SetFootprintTags(tags)

        self.render()
        self.ShowFootprint()
        
    def onNameTextEnter( self, event ):
        self.Update()
        
    def onTimestampTextEnter( self, event ):
        self.Update()
    
    def onDescrTextEnter( self, event ):
        self.Update()

    def onTagsTextEnter( self, event ):
        self.Update()
