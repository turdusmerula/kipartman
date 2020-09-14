# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep  2 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PanelRenderSymbol
###########################################################################

class PanelRenderSymbol ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 284,229 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.bitmap_render_symbol = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.bitmap_render_symbol, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_kicad = wx.Menu()
		self.menu_rebuild_symbols = wx.MenuItem( self.menu_kicad, wx.ID_ANY, u"Rebuild symbols", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_kicad.Append( self.menu_rebuild_symbols )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelRenderSymbolOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.Bind( wx.EVT_MENU, self.onMenuKicadRebuildSymbolsSelection, id = self.menu_rebuild_symbols.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onMenuKicadRebuildSymbolsSelection( self, event ):
		event.Skip()

	def PanelRenderSymbolOnContextMenu( self, event ):
		self.PopupMenu( self.menu_kicad, event.GetPosition() )


