from dialogs.dialog_configuration import DialogConfiguration
from configuration import configuration
from currency.currency import Currency
import rest
import wx
import swagger_client
from octopart.queries import PartsQuery as OctpartPartsQuery
from snapeda.connection import SnapedaConnection, SnapedaConnectionException

class ConfigurationFrame(DialogConfiguration): 
    def __init__(self, parent): 
        DialogConfiguration.__init__(self, parent)
        
        self.edit_kipartbase.Value = configuration.kipartbase
        self.edit_octopart_apikey.Value = configuration.octopart_api_key
        self.edit_snapeda_user.Value = configuration.snapeda_user
        self.edit_snapeda_password.Value = configuration.snapeda_password
        
        if configuration.kicad_path=='':
            self.dir_kicad_path.SetPath(configuration.FindKicad())
        else:
            self.dir_kicad_path.SetPath(configuration.kicad_path)
        
        self.check_common_path.SetValue(configuration.kicad_library_common_path)
        self.dir_footprints_path.SetPath(configuration.kicad_footprints_path)
        if configuration.kicad_library_common_path:
            self.dir_symbols_path.SetPath(configuration.kicad_footprints_path)
            self.dir_3d_models_path.SetPath(configuration.kicad_footprints_path)
        else:
            self.dir_symbols_path.SetPath(configuration.kicad_symbols_path)
            self.dir_3d_models_path.SetPath(configuration.kicad_3d_models_path)
        self.onCheckCommonPath(None)
        
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
        
        configuration.kicad_path = self.dir_kicad_path.GetPath()
        configuration.kicad_footprints_path = self.dir_footprints_path.GetPath()
        if self.check_common_path.Value:
            configuration.kicad_symbols_path = self.dir_footprints_path.GetPath()
            configuration.kicad_3d_models_path = self.dir_footprints_path.GetPath()
        else:
            configuration.kicad_symbols_path = self.dir_symbols_path.GetPath()
            configuration.kicad_3d_models_path = self.dir_3d_models_path.GetPath()
        configuration.kicad_library_common_path = self.check_common_path.Value
        
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
        apikey = OctpartPartsQuery.apikey
        
        OctpartPartsQuery.apikey = self.edit_octopart_apikey.Value
        try:
            q = OctpartPartsQuery()
            q.get('atmega328p')
            self.data = q.results()
            print self.data
            wx.MessageBox( 'OCTOPART CONNECTION OK', 
                'OCTOPART CONNECTION OK', wx.OK )
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        OctpartPartsQuery.apikey = apikey
           
        
    def onTestSnapeda( self, event ):
        connection = SnapedaConnection()
        
        try:
            connection.connect(self.edit_snapeda_user.Value, self.edit_snapeda_password.Value)
            wx.MessageBox( 'SNAPEDA CONNECTION OK', 
                'SNAPEDA CONNECTION OK', wx.OK )
        except SnapedaConnectionException as e:
            wx.MessageBox(format(e.error), 'Error', wx.OK | wx.ICON_ERROR)
    
    def onButtonKicadPathDefault( self, event ):
        path = configuration.FindKicad()
        if path:
            self.dir_kicad_path.SetPath(path)
        else:
            wx.MessageBox("Kicad was not found in system path, check your kicad installation", 'Error', wx.OK | wx.ICON_ERROR)
            

    def onCheckCommonPath( self, event ):
        if self.check_common_path.Value:
            self.dir_3d_models_path.Enabled = False
            self.dir_symbols_path.Enabled = False
        else:
            self.dir_3d_models_path.Enabled = True
            self.dir_symbols_path.Enabled = True
            
    
