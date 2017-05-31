from dialogs.panel_edit_part import PanelEditPart
from frames.select_footprint_frame import SelectFootprintFrame
from frames.dropdown_frame import DropdownFrame
from frames.dropdown_dialog import DropdownDialog
from frames.select_octopart_frame import SelectOctopartFrame
import wx.lib.newevent

EditPartApplyEvent, EVT_EDIT_PART_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditPartCancelEvent, EVT_EDIT_PART_CANCEL_EVENT = wx.lib.newevent.NewEvent()

class EditPartFrame(PanelEditPart): 
    def __init__(self, parent, part):
        super(PanelEditPart, self).__init__(parent)

    def SetPart(self, part):
        self.part = part
        if part:
            self.edit_part_name.Value = part.name
            self.edit_part_description.Value = part.description
            self.edit_part_comment.Value = part.comment
            if part.footprint:
                self.button_part_footprint.Label = part.footprint.name
            else:
                self.button_part_footprint.Label = "<none>"
            self.button_part_footprint.Value = part.footprint
        else:
            self.edit_part_name.Value = ''
            self.edit_part_description.Value = ''
            self.edit_part_comment.Value = ''
            self.button_part_footprint.Label = "<none>"

    def onButtonPartFootprintClick( self, event ):
        footprint = self.button_part_footprint.Value
        frame = DropdownFrame(self.button_part_footprint, SelectFootprintFrame, footprint)
        frame.Dropdown(self.onSetFootprintCallback)
    
    def onSetFootprintCallback(self, footprint):
        if footprint:
            self.button_part_footprint.Label = footprint.name
        else:
            self.button_part_footprint.Label = "<none>"
        self.button_part_footprint.Value = footprint
        
    def onButtonPartEditApply( self, event ):
        event = EditPartApplyEvent(data=self.part)
        wx.PostEvent(self, event)
        
    def onButtonPartEditCancel( self, event ):
        event = EditPartCancelEvent()
        wx.PostEvent(self, event)

    def onButtonOctopartClick( self, event ):
        search = self.edit_part_name.Value
        frame = DropdownDialog(self.button_part_footprint, SelectOctopartFrame, search)
        frame.Dropdown(self.onSetOctopartCallback)

    def onSetOctopartCallback(self, part):
        if part:
            print part
