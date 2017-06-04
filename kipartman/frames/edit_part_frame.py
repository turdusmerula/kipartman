from dialogs.panel_edit_part import PanelEditPart
from frames.select_footprint_frame import SelectFootprintFrame
from frames.part_parameters_frame import PartParametersFrame
from frames.dropdown_frame import DropdownFrame
from frames.dropdown_dialog import DropdownDialog
from frames.select_octopart_frame import SelectOctopartFrame, EVT_SELECT_OCTOPART_OK_EVENT
import wx.lib.newevent
from api import models

EditPartApplyEvent, EVT_EDIT_PART_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditPartCancelEvent, EVT_EDIT_PART_CANCEL_EVENT = wx.lib.newevent.NewEvent()

class EditPartFrame(PanelEditPart): 
    def __init__(self, parent):
        super(EditPartFrame, self).__init__(parent)
        
        self.edit_part_parameters = PartParametersFrame(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_parameters, "Parameters")
        
        self.edit_part_distributors = wx.Panel(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_distributors, "Distributors")

        self.edit_part_manufacturers = wx.Panel(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_manufacturers, "Manufacturers")

        self.edit_part_attachements = wx.Panel(self.notebook_part)
        self.notebook_part.AddPage(self.edit_part_attachements, "Attachements")

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
        self.edit_part_parameters.SetPart(part)
    
    def ApplyChanges(self, part):
        self.edit_part_parameters.ApplyChanges(part)
#        self.edit_part_distributors.ApplyChanges(part)
#        self.edit_part_manufacturers.ApplyChanges(part)
#        self.edit_part_attachements.ApplyChanges(part)
        
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
        part = self.part
        if not part:
            part = models.Part()
        # set part content
        part.name = self.edit_part_name.Value
        part.description = self.edit_part_description.Value
        part.comment = self.edit_part_comment.Value
        part.footprint = self.button_part_footprint.Value
        # send result event
        event = EditPartApplyEvent(data=part)
        wx.PostEvent(self, event)
        
    def onButtonPartEditCancel( self, event ):
        event = EditPartCancelEvent()
        wx.PostEvent(self, event)


    def onButtonOctopartClick( self, event ):
        # create an octopart frame
        # dropdown frame
        dropdown = DropdownDialog(self.button_octopart, SelectOctopartFrame, self.edit_part_name.Value)
        dropdown.panel.Bind( EVT_SELECT_OCTOPART_OK_EVENT, self.onSelectOctopartFrameOk )
        dropdown.Dropdown()

    def onSelectOctopartFrameOk(self, part):
        if part:
            print part
