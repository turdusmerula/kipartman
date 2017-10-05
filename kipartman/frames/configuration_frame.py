from dialogs.dialog_configuration import DialogConfiguration
from configuration import configuration

class ConfigurationFrame(DialogConfiguration): 
    def __init__(self, parent): 
        DialogConfiguration.__init__(self, parent)
        
        self.edit_kipartbase.Value = configuration.kipartbase
        self.edit_octopart_apikey.Value = configuration.octopart_api_key
        self.edit_snapeda_user.Value = configuration.snapeda_user
        self.edit_snapeda_password.Value = configuration.snapeda_password

    def onCancelButtonClick( self, event ):
        self.EndModal(False)
    
    def onOkButtonClick( self, event ):
        configuration.kipartbase = self.edit_kipartbase.Value
        configuration.octopart_api_key = self.edit_octopart_apikey.Value
        configuration.snapeda_user = self.edit_snapeda_user.Value
        configuration.snapeda_password = self.edit_snapeda_password.Value
        configuration.Save()
        self.EndModal(True)
