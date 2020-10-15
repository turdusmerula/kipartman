# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep 24 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PanelEditParameter
###########################################################################

class PanelEditParameter ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 412,417 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Parameter", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_parameter_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_parameter_name, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Alias", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		fgSizer1.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		combo_parameter_aliasChoices = []
		self.combo_parameter_alias = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, combo_parameter_aliasChoices, 0 )
		bSizer4.Add( self.combo_parameter_alias, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.button_parameter_alias_add = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.button_parameter_alias_add.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		bSizer4.Add( self.button_parameter_alias_add, 0, wx.TOP|wx.BOTTOM, 5 )

		self.button_parameter_alias_remove = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.button_parameter_alias_remove.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		bSizer4.Add( self.button_parameter_alias_remove, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )


		fgSizer1.Add( bSizer4, 1, wx.EXPAND, 5 )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_parameter_description = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_parameter_description, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		fgSizer1.Add( self.m_staticText10, 0, wx.ALL, 5 )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		fgSizer1.Add( self.m_staticText11, 0, wx.ALL, 5 )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Value Type", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.radio_choice_parameter_integer = wx.RadioButton( self, wx.ID_ANY, u"Integer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.radio_choice_parameter_integer.Enable( False )

		bSizer6.Add( self.radio_choice_parameter_integer, 0, wx.ALL, 5 )

		self.radio_choice_parameter_float = wx.RadioButton( self, wx.ID_ANY, u"Float", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.radio_choice_parameter_float.Enable( False )

		bSizer6.Add( self.radio_choice_parameter_float, 0, wx.ALL, 5 )

		self.radio_choice_parameter_text = wx.RadioButton( self, wx.ID_ANY, u"Text", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.radio_choice_parameter_text.Enable( False )

		bSizer6.Add( self.radio_choice_parameter_text, 0, wx.ALL, 5 )


		fgSizer1.Add( bSizer6, 1, wx.EXPAND, 5 )

		self.static_unit = wx.StaticText( self, wx.ID_ANY, u"Unit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.static_unit.Wrap( -1 )

		fgSizer1.Add( self.static_unit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.button_search_unit = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT )
		self.button_search_unit.Enable( False )

		bSizer3.Add( self.button_search_unit, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.button_remove_unit = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.button_remove_unit.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		bSizer3.Add( self.button_remove_unit, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )


		fgSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )


		bSizer1.Add( fgSizer1, 1, wx.EXPAND, 5 )

		button_parameter_edit = wx.StdDialogButtonSizer()
		self.button_parameter_editApply = wx.Button( self, wx.ID_APPLY )
		button_parameter_edit.AddButton( self.button_parameter_editApply )
		self.button_parameter_editCancel = wx.Button( self, wx.ID_CANCEL )
		button_parameter_edit.AddButton( self.button_parameter_editCancel )
		button_parameter_edit.Realize();

		bSizer1.Add( button_parameter_edit, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10 )


		self.SetSizer( bSizer1 )
		self.Layout()

		# Connect Events
		self.edit_parameter_name.Bind( wx.EVT_TEXT, self.onTextEditParameterName )
		self.combo_parameter_alias.Bind( wx.EVT_TEXT, self.onComboParameterAliasChange )
		self.button_parameter_alias_add.Bind( wx.EVT_BUTTON, self.onButtonParameterAliasAddClick )
		self.button_parameter_alias_remove.Bind( wx.EVT_BUTTON, self.onButtonParameterAliasRemoveClick )
		self.edit_parameter_description.Bind( wx.EVT_TEXT, self.onTextEditParameterDescription )
		self.button_search_unit.Bind( wx.EVT_BUTTON, self.onButtonSearchUnitClick )
		self.button_remove_unit.Bind( wx.EVT_BUTTON, self.onButtonRemoveUnitClick )
		self.button_parameter_editApply.Bind( wx.EVT_BUTTON, self.onButtonPartParameterEditApply )
		self.button_parameter_editCancel.Bind( wx.EVT_BUTTON, self.onButtonPartParameterEditCancel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onTextEditParameterName( self, event ):
		event.Skip()

	def onComboParameterAliasChange( self, event ):
		event.Skip()

	def onButtonParameterAliasAddClick( self, event ):
		event.Skip()

	def onButtonParameterAliasRemoveClick( self, event ):
		event.Skip()

	def onTextEditParameterDescription( self, event ):
		event.Skip()

	def onButtonSearchUnitClick( self, event ):
		event.Skip()

	def onButtonRemoveUnitClick( self, event ):
		event.Skip()

	def onButtonPartParameterEditApply( self, event ):
		event.Skip()

	def onButtonPartParameterEditCancel( self, event ):
		event.Skip()


