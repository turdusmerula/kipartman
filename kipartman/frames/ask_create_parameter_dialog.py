from dialogs.dialog_ask_create_parameter import DialogAskCreateParameter
import wx
from frames.dropdown_dialog2 import DropdownDialog2
from frames.select_parameter_frame import SelectParameterFrame

class AskCreateParameterDialog(DialogAskCreateParameter):
    
    def __init__( self, parent, provider_parameter, *args, **kwargs ):
        super(AskCreateParameterDialog, self).__init__(parent, *args, **kwargs)
        self.provider_parameter = provider_parameter
        self.parameter = None
        self.static_message.Label = f"Parameter '{provider_parameter.name}' does not exists, create it?"
    
    def CreateParameter(self, provider_parameter):
        self.provider_parameter = provider_parameter
        if self.ShowModal()==wx.ID_OK:
            return self.parameter
        return None
    
    def onSelectParameterAliasClick( self, event ):
        frame = DropdownDialog2(self, SelectParameterFrame, self.provider_parameter.name)
        if frame.DropHere(self.onSelectParameterFrameOk)==wx.ID_OK:
            self.EndModal(wx.ID_OK)

    def onSelectParameterFrameOk(self, parameter):
        self.parameter = parameter

    def onCreateParameterClick( self, event ):
        event.Skip()

    def onCancelClick( self, event ):
        event.Skip()
    