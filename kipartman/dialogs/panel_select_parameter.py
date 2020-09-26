# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep 24 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelSelectParameter
###########################################################################

class PanelSelectParameter ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 718,261 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_parameter = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_parameter.ShowSearchButton( True )
		self.search_parameter.ShowCancelButton( False )
		self.search_parameter.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_parameter, 1, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_parameters = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_parameters.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_parameters, 0, wx.ALL, 5 )


		bSizer4.Add( bSizer61, 0, wx.EXPAND, 5 )

		self.tree_parameters = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.tree_parameters, 1, wx.EXPAND|wx.ALL, 5 )


		bSizer2.Add( bSizer4, 1, wx.EXPAND|wx.BOTTOM, 5 )


		bSizer16.Add( bSizer2, 1, wx.EXPAND, 5 )

		button_select_parameter = wx.StdDialogButtonSizer()
		self.button_select_parameterOK = wx.Button( self, wx.ID_OK )
		button_select_parameter.AddButton( self.button_select_parameterOK )
		self.button_select_parameterCancel = wx.Button( self, wx.ID_CANCEL )
		button_select_parameter.AddButton( self.button_select_parameterCancel )
		button_select_parameter.Realize();

		bSizer16.Add( button_select_parameter, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )


		self.SetSizer( bSizer16 )
		self.Layout()

		# Connect Events
		self.search_parameter.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchSymbolCancel )
		self.search_parameter.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchSymbolButton )
		self.search_parameter.Bind( wx.EVT_TEXT_ENTER, self.onSearchSymbolTextEnter )
		self.button_refresh_parameters.Bind( wx.EVT_BUTTON, self.onButtonRefreshSymbolsClick )
		self.button_select_parameterCancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )
		self.button_select_parameterOK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onSearchSymbolCancel( self, event ):
		event.Skip()

	def onSearchSymbolButton( self, event ):
		event.Skip()

	def onSearchSymbolTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshSymbolsClick( self, event ):
		event.Skip()

	def onButtonCancelClick( self, event ):
		event.Skip()

	def onButtonOkClick( self, event ):
		event.Skip()


