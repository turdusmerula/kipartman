# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 22 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DialogConfiguration
###########################################################################

class DialogConfiguration ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 484,589 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer111 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"User" ), wx.HORIZONTAL )
		
		self.m_staticText111 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Currency", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )
		sbSizer111.Add( self.m_staticText111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		choice_user_currencyChoices = []
		self.choice_user_currency = wx.Choice( sbSizer111.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_user_currencyChoices, 0 )
		self.choice_user_currency.SetSelection( 0 )
		sbSizer111.Add( self.choice_user_currency, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( sbSizer111, 0, wx.EXPAND, 5 )
		
		self.m_staticline11 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )
		
		sbSizer11 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Parts" ), wx.HORIZONTAL )
		
		self.m_staticText11 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Kipartbase", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		sbSizer11.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_kipartbase = wx.TextCtrl( sbSizer11.GetStaticBox(), wx.ID_ANY, u"http://localhost:8100", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer11.Add( self.edit_kipartbase, 1, wx.ALL, 5 )
		
		self.button_test_kipartbase = wx.Button( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Test", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer11.Add( self.button_test_kipartbase, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( sbSizer11, 0, wx.EXPAND, 5 )
		
		self.m_staticline5 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Octopart" ), wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"API Key", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		sbSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_octopart_apikey = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer1.Add( self.edit_octopart_apikey, 1, wx.ALL, 5 )
		
		self.button_test_octopart = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Test", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer1.Add( self.button_test_octopart, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( sbSizer1, 0, wx.EXPAND, 5 )
		
		self.m_staticline6 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"SnapEda" ), wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText2 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"User", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_snapeda_user = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.edit_snapeda_user, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText3 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_snapeda_password = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		fgSizer2.Add( self.edit_snapeda_password, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer2.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		self.button_test_snapeda = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Test", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_test_snapeda, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		sbSizer2.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		
		bSizer10.Add( sbSizer2, 0, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		sbSizer21 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Kicad integration" ), wx.VERTICAL )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer21 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer21.AddGrowableCol( 1 )
		fgSizer21.SetFlexibleDirection( wx.BOTH )
		fgSizer21.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText21 = wx.StaticText( sbSizer21.GetStaticBox(), wx.ID_ANY, u"Kicad path", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		fgSizer21.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.dir_kicad_path = wx.DirPickerCtrl( sbSizer21.GetStaticBox(), wx.ID_ANY, u"/home/seb", u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer4.Add( self.dir_kicad_path, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.button_kicad_path_default = wx.Button( sbSizer21.GetStaticBox(), wx.ID_ANY, u"Default", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.button_kicad_path_default, 0, wx.ALL, 5 )
		
		
		fgSizer21.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		self.m_staticText31 = wx.StaticText( sbSizer21.GetStaticBox(), wx.ID_ANY, u"Footprints path", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		fgSizer21.Add( self.m_staticText31, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.dir_footprints_path = wx.DirPickerCtrl( sbSizer21.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		fgSizer21.Add( self.dir_footprints_path, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText311 = wx.StaticText( sbSizer21.GetStaticBox(), wx.ID_ANY, u"Symbols path", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText311.Wrap( -1 )
		fgSizer21.Add( self.m_staticText311, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.dir_symbols_path = wx.DirPickerCtrl( sbSizer21.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		fgSizer21.Add( self.dir_symbols_path, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText312 = wx.StaticText( sbSizer21.GetStaticBox(), wx.ID_ANY, u"3D models path", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText312.Wrap( -1 )
		fgSizer21.Add( self.m_staticText312, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.dir_3d_models_path = wx.DirPickerCtrl( sbSizer21.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		fgSizer21.Add( self.dir_3d_models_path, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer3.Add( fgSizer21, 1, wx.EXPAND, 5 )
		
		self.check_common_path = wx.CheckBox( sbSizer21.GetStaticBox(), wx.ID_ANY, u"Use same folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.check_common_path.SetValue(True) 
		bSizer3.Add( self.check_common_path, 0, wx.ALL, 5 )
		
		
		sbSizer21.Add( bSizer3, 0, wx.EXPAND, 5 )
		
		
		bSizer10.Add( sbSizer21, 1, wx.EXPAND, 5 )
		
		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();
		
		bSizer10.Add( m_sdbSizer1, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer10 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.button_test_kipartbase.Bind( wx.EVT_BUTTON, self.onTestKipartbase )
		self.button_test_octopart.Bind( wx.EVT_BUTTON, self.onTestOctopart )
		self.button_test_snapeda.Bind( wx.EVT_BUTTON, self.onTestSnapeda )
		self.button_kicad_path_default.Bind( wx.EVT_BUTTON, self.onButtonKicadPathDefault )
		self.check_common_path.Bind( wx.EVT_CHECKBOX, self.onCheckCommonPath )
		self.m_sdbSizer1Cancel.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.m_sdbSizer1OK.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onTestKipartbase( self, event ):
		event.Skip()
	
	def onTestOctopart( self, event ):
		event.Skip()
	
	def onTestSnapeda( self, event ):
		event.Skip()
	
	def onButtonKicadPathDefault( self, event ):
		event.Skip()
	
	def onCheckCommonPath( self, event ):
		event.Skip()
	
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

