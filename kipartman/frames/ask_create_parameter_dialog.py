from dialogs.dialog_ask_create_parameter import DialogAskCreateParameter
import wx
from frames.dropdown_dialog import DropdownDialog
from frames.dropdown_dialog2 import DropdownDialog2
from frames.select_parameter_frame import SelectParameterFrame
from frames.edit_parameter_frame import EditParameterFrame, EVT_EDIT_PARAMETER_APPLY_EVENT
import api.data.parameter

class AskCreateParameterDialog(DialogAskCreateParameter):
    
    def __init__( self, parent, provider_parameter, *args, **kwargs ):
        super(AskCreateParameterDialog, self).__init__(parent, *args, **kwargs)
        self.provider_parameter = provider_parameter
        self.parameter = None
        self.static_message.Label = f"Parameter '{provider_parameter.name}' with value '{provider_parameter.value}' does not exists, create it?"
    
    def CreateParameter(self, provider_parameter):
        self.provider_parameter = provider_parameter
        if self.ShowModal()==wx.ID_OK:
            return self.parameter
        return None
    
    def onSelectParameterAliasClick( self, event ):
        frame = DropdownDialog(self, SelectParameterFrame, self.provider_parameter.name)
        if frame.DropHere(self.onSelectParameterFrameOk)==wx.ID_OK:
            self.EndModal(wx.ID_OK)

    def onSelectParameterFrameOk(self, parameter):
        self.parameter = parameter

    def onCreateParameterClick( self, event ):
        self.frame = DropdownDialog2(self, EditParameterFrame)
        self.frame.panel.Bind( EVT_EDIT_PARAMETER_APPLY_EVENT, self.onEditParameterApply )
        self.frame.panel.AddParameter(name=self.provider_parameter.name)
        
        if self.frame.DropHere(self.onSelectParameterFrameOk)==wx.ID_OK:
            self.EndModal(wx.ID_OK)

    def onEditParameterApply(self, event):
        self.parameter = event.data
        self.frame.EndModal(wx.ID_OK)

    def onCancelClick( self, event ):
        self.EndModal(wx.ID_CANCEL)
        event.Skip()
