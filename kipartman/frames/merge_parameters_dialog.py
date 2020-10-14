from dialogs.dialog_merge_parameters import DialogMergeParameters
import wx.dataview
import wx.lib.newevent
import helper.tree
from helper.exception import print_stack
from frames.wait_dialog import WaitDialog

SelectParameterOkEvent, EVT_SELECT_PARAMETER_OK_EVENT = wx.lib.newevent.NewEvent()
    
class MergeParametersDialog(DialogMergeParameters):
    def __init__(self, parent, parameters): 
        super(MergeParametersDialog, self).__init__(parent)

        self.parameters = parameters
        
        for parameter in parameters:
            self.combo_merge_into.Append(parameter.name)
        
        self.button_apply.Enabled = False
        
    def onComboMergeIntoChoice( self, event ):
        if self.combo_merge_into.Selection>=0:
            self.button_apply.Enabled = True
        event.Skip()

    def onButtonCancelClick( self, event ):
#         self.Close()
        event.Skip()

    def onButtonOkClick( self, event ):
        name = self.combo_merge_into.Items[self.combo_merge_into.Selection]
        for parameter in self.parameters:
            if name==parameter.name:
                # trigger result event
                event = SelectParameterOkEvent(data=parameter)
                wx.PostEvent(self, event)
                return
            
        event.Skip()
        
