from dialogs.dialog_configuration import DialogConfiguration
from configuration import configuration
from currency.currency import Currency
import rest
import wx
import swagger_client

class ConfigurationFrame(DialogConfiguration): 
    def __init__(self, parent): 
        DialogConfiguration.__init__(self, parent)
        
        self.edit_kipartbase.Value = configuration.kipartbase
        self.edit_octopart_apikey.Value = configuration.octopart_api_key
        self.edit_snapeda_user.Value = configuration.snapeda_user
        self.edit_snapeda_password.Value = configuration.snapeda_password

        try:
            currencies = Currency(configuration.base_currency).load()
        except Exception as e:
            currencies = Currency('EUR').load()
            
        if currencies.has_key('error'):
            currencies = Currency('EUR').load()
            self.choice_user_currency.Append('EUR')
        else:
            self.choice_user_currency.Append(configuration.base_currency)
            
        for currency in currencies['rates']:
            self.choice_user_currency.Append(currency)
        self.choice_user_currency.SetSelection(0)

            
    def onCancelButtonClick( self, event ):
        self.EndModal(False)
    
    def onOkButtonClick( self, event ):
        configuration.kipartbase = self.edit_kipartbase.Value
        configuration.octopart_api_key = self.edit_octopart_apikey.Value
        configuration.snapeda_user = self.edit_snapeda_user.Value
        configuration.snapeda_password = self.edit_snapeda_password.Value
        
        configuration.base_currency = self.choice_user_currency.GetString(self.choice_user_currency.GetSelection())
        
        configuration.Save()
        
        # reload rest api
        rest.base_url = configuration.kipartbase
        rest.reload()
        
        self.EndModal(True)

    def onTestKipartbase( self, event ):
        try:
            base_url = self.edit_kipartbase.Value+'/api'
            client = swagger_client.ApiClient(base_url)
            api = swagger_client.DefaultApi(client)
            currencies = api.find_currencies()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        
    def onTestOctopart( self, event ):
        event.Skip()
    
    def onTestSnapeda( self, event ):
        event.Skip()
    
    def onButtonKicadPathDefault( self, event ):
        event.Skip()

    def onCheckCommonFolder( self, event ):
        event.Skip()
    
