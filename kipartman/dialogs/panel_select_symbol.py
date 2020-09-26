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
## Class PanelSelectSymbol
###########################################################################

class PanelSelectSymbol ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 744,328 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_symbol = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_symbol.ShowSearchButton( True )
		self.search_symbol.ShowCancelButton( False )
		self.search_symbol.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_symbol, 1, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_symbols = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_symbols.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_symbols, 0, wx.ALL, 5 )


		bSizer4.Add( bSizer61, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )

		self.tree_symbols = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.tree_symbols, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )

		self.panel_image_symbol = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer41 = wx.BoxSizer( wx.VERTICAL )

		self.image_symbol = wx.StaticBitmap( self.panel_image_symbol, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer41.Add( self.image_symbol, 1, wx.ALL|wx.EXPAND, 5 )


		self.panel_image_symbol.SetSizer( bSizer41 )
		self.panel_image_symbol.Layout()
		bSizer41.Fit( self.panel_image_symbol )
		bSizer2.Add( self.panel_image_symbol, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer16.Add( bSizer2, 1, wx.EXPAND, 5 )

		button_symbol_edit = wx.StdDialogButtonSizer()
		self.button_symbol_editOK = wx.Button( self, wx.ID_OK )
		button_symbol_edit.AddButton( self.button_symbol_editOK )
		self.button_symbol_editCancel = wx.Button( self, wx.ID_CANCEL )
		button_symbol_edit.AddButton( self.button_symbol_editCancel )
		button_symbol_edit.Realize();

		bSizer16.Add( button_symbol_edit, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )


		self.SetSizer( bSizer16 )
		self.Layout()

		# Connect Events
		self.search_symbol.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchSymbolCancel )
		self.search_symbol.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchSymbolButton )
		self.search_symbol.Bind( wx.EVT_TEXT_ENTER, self.onSearchSymbolTextEnter )
		self.button_refresh_symbols.Bind( wx.EVT_BUTTON, self.onButtonRefreshSymbolsClick )
		self.button_symbol_editCancel.Bind( wx.EVT_BUTTON, self.onButtonCancelClick )
		self.button_symbol_editOK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )

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


