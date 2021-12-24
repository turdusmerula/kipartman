# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-34-g2d20e717)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui

###########################################################################
## Class DialogConfiguration
###########################################################################

class DialogConfiguration ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 542,612 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

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


		bSizer10.Add( sbSizer111, 0, wx.EXPAND|wx.ALL, 5 )

		self.m_staticline11 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )

		sbSizer11 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Parts" ), wx.HORIZONTAL )

		self.m_staticText11 = wx.StaticText( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Database", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		sbSizer11.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.dir_database_path = wx.DirPickerCtrl( sbSizer11.GetStaticBox(), wx.ID_ANY, u"/home/seb", u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		sbSizer11.Add( self.dir_database_path, 1, wx.ALL|wx.EXPAND, 5 )

		self.button_kicad_path_default1 = wx.Button( sbSizer11.GetStaticBox(), wx.ID_ANY, u"Default", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer11.Add( self.button_kicad_path_default1, 0, wx.ALL, 5 )


		bSizer10.Add( sbSizer11, 0, wx.EXPAND|wx.ALL, 5 )

		self.m_staticline5 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )

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


		bSizer10.Add( sbSizer21, 0, wx.EXPAND|wx.ALL, 5 )

		self.m_auinotebook1 = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE )
		self.m_panel1 = wx.Panel( self.m_auinotebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"User", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		fgSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_snapeda_user = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.edit_snapeda_user, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_snapeda_password = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		fgSizer2.Add( self.edit_snapeda_password, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( fgSizer2, 1, wx.EXPAND, 5 )

		self.button_test_snapeda = wx.Button( self.m_panel1, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_test_snapeda, 0, wx.ALL, 5 )


		self.m_panel1.SetSizer( bSizer2 )
		self.m_panel1.Layout()
		bSizer2.Fit( self.m_panel1 )
		self.m_auinotebook1.AddPage( self.m_panel1, u"SnapEDA", True, wx.NullBitmap )
		self.m_panel2 = wx.Panel( self.m_auinotebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.AddGrowableCol( 1 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"API Key", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		fgSizer3.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_octopart_apikey = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.edit_octopart_apikey, 1, wx.EXPAND|wx.ALL, 5 )


		bSizer6.Add( fgSizer3, 1, wx.EXPAND, 5 )

		self.button_test_octopart = wx.Button( self.m_panel2, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.button_test_octopart, 0, wx.ALL, 5 )


		self.m_panel2.SetSizer( bSizer6 )
		self.m_panel2.Layout()
		bSizer6.Fit( self.m_panel2 )
		self.m_auinotebook1.AddPage( self.m_panel2, u"Octopart", False, wx.NullBitmap )
		self.m_panel3 = wx.Panel( self.m_auinotebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

		fgSizer22 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer22.AddGrowableCol( 1 )
		fgSizer22.SetFlexibleDirection( wx.BOTH )
		fgSizer22.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText22 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"API Key", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )

		fgSizer22.Add( self.m_staticText22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_mouser_apikey = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer22.Add( self.edit_mouser_apikey, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer21.Add( fgSizer22, 1, wx.EXPAND, 5 )

		self.button_test_mouser = wx.Button( self.m_panel3, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.button_test_mouser, 0, wx.ALL, 5 )


		self.m_panel3.SetSizer( bSizer21 )
		self.m_panel3.Layout()
		bSizer21.Fit( self.m_panel3 )
		self.m_auinotebook1.AddPage( self.m_panel3, u"Mouser", False, wx.NullBitmap )

		bSizer10.Add( self.m_auinotebook1, 1, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();

		bSizer10.Add( m_sdbSizer1, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5 )


		self.SetSizer( bSizer10 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.button_kicad_path_default1.Bind( wx.EVT_BUTTON, self.onButtonKicadPathDefault )
		self.button_kicad_path_default.Bind( wx.EVT_BUTTON, self.onButtonKicadPathDefault )
		self.check_common_path.Bind( wx.EVT_CHECKBOX, self.onCheckCommonPath )
		self.button_test_snapeda.Bind( wx.EVT_BUTTON, self.onButtonTestSnapedaClick )
		self.button_test_octopart.Bind( wx.EVT_BUTTON, self.onButtonTestOctopartClick )
		self.button_test_mouser.Bind( wx.EVT_BUTTON, self.onButtonTestMouserClick )
		self.m_sdbSizer1Cancel.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.m_sdbSizer1OK.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def onButtonKicadPathDefault( self, event ):
		event.Skip()


	def onCheckCommonPath( self, event ):
		event.Skip()

	def onButtonTestSnapedaClick( self, event ):
		event.Skip()

	def onButtonTestOctopartClick( self, event ):
		event.Skip()

	def onButtonTestMouserClick( self, event ):
		event.Skip()

	def onCancelButtonClick( self, event ):
		event.Skip()

	def onOkButtonClick( self, event ):
		event.Skip()


