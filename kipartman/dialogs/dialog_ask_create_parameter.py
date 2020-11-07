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
## Class DialogAskCreateParameter
###########################################################################

class DialogAskCreateParameter ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Unknown parameter", pos = wx.DefaultPosition, size = wx.Size( 556,206 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.static_message = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.static_message.Wrap( -1 )

		bSizer4.Add( self.static_message, 0, wx.ALL, 5 )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Select parameter alias", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		fgSizer2.Add( self.m_staticText1, 1, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.button_select_parameter_alias = wx.Button( self, wx.ID_ANY, u"->", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.button_select_parameter_alias, 0, wx.ALL, 5 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Create parameter", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		fgSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.button_create_parameter = wx.Button( self, wx.ID_ANY, u"->", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.button_create_parameter, 0, wx.ALL, 5 )


		bSizer4.Add( fgSizer2, 1, wx.EXPAND, 5 )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.button_cancel = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_cancel, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer2, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer4.Add( bSizer1, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer4 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.button_select_parameter_alias.Bind( wx.EVT_BUTTON, self.onSelectParameterAliasClick )
		self.button_create_parameter.Bind( wx.EVT_BUTTON, self.onCreateParameterClick )
		self.button_cancel.Bind( wx.EVT_BUTTON, self.onCancelClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onSelectParameterAliasClick( self, event ):
		event.Skip()

	def onCreateParameterClick( self, event ):
		event.Skip()

	def onCancelClick( self, event ):
		event.Skip()


