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
## Class PanelEditUnit
###########################################################################

class PanelEditUnit ( wx.Panel ):

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

		self.edit_unit_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_unit_name, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Symbol", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.edit_unit_symbol = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_unit_symbol, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Prefixable", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		fgSizer1.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.check_unit_prefixable = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.check_unit_prefixable, 0, wx.ALL, 5 )


		bSizer1.Add( fgSizer1, 1, wx.EXPAND, 5 )

		button_unit_edit = wx.StdDialogButtonSizer()
		self.button_unit_editApply = wx.Button( self, wx.ID_APPLY )
		button_unit_edit.AddButton( self.button_unit_editApply )
		self.button_unit_editCancel = wx.Button( self, wx.ID_CANCEL )
		button_unit_edit.AddButton( self.button_unit_editCancel )
		button_unit_edit.Realize();

		bSizer1.Add( button_unit_edit, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10 )


		self.SetSizer( bSizer1 )
		self.Layout()

		# Connect Events
		self.edit_unit_name.Bind( wx.EVT_TEXT, self.onTextEditUnitName )
		self.edit_unit_symbol.Bind( wx.EVT_TEXT, self.onTextEditUnitSymbol )
		self.button_unit_editApply.Bind( wx.EVT_BUTTON, self.onButtonUnitEditApply )
		self.button_unit_editCancel.Bind( wx.EVT_BUTTON, self.onButtonUnitEditCancel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onTextEditUnitName( self, event ):
		event.Skip()

	def onTextEditUnitSymbol( self, event ):
		event.Skip()

	def onButtonUnitEditApply( self, event ):
		event.Skip()

	def onButtonUnitEditCancel( self, event ):
		event.Skip()


