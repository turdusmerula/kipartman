# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep  1 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelSymbolLibraries
###########################################################################

class PanelSymbolLibraries ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.button_refresh_libraries = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_libraries.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer4.Add( self.button_refresh_libraries, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer4, 0, wx.ALIGN_RIGHT, 5 )

		self.tree_libraries = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer2.Add( self.tree_libraries, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()
		self.menu_libraries = wx.Menu()
		self.menu_libraries_add_folder = wx.MenuItem( self.menu_libraries, wx.ID_ANY, u"Add folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_libraries_add_folder.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_libraries.Append( self.menu_libraries_add_folder )

		self.menu_libraries_add_library = wx.MenuItem( self.menu_libraries, wx.ID_ANY, u"Add library", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_libraries_add_library.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_libraries.Append( self.menu_libraries_add_library )

		self.menu_libraries_rename = wx.MenuItem( self.menu_libraries, wx.ID_ANY, u"Rename", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_libraries_rename.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_libraries.Append( self.menu_libraries_rename )

		self.menu_libraries_remove = wx.MenuItem( self.menu_libraries, wx.ID_ANY, u"Remove", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_libraries_remove.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_libraries.Append( self.menu_libraries_remove )

		self.menu_libraries.AppendSeparator()

		self.menu_libraries_add_symbol = wx.MenuItem( self.menu_libraries, wx.ID_ANY, u"Add symbol", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_libraries_add_symbol.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_libraries.Append( self.menu_libraries_add_symbol )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelSymbolLibrariesOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_refresh_libraries.Bind( wx.EVT_BUTTON, self.onButtonRefreshLibrariesClick )
		self.Bind( wx.EVT_MENU, self.onMenuLibrariesAddFolder, id = self.menu_libraries_add_folder.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuLibrariesAddLibrary, id = self.menu_libraries_add_library.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuLibrariesRename, id = self.menu_libraries_rename.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuLibrariesRemove, id = self.menu_libraries_remove.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuLibrariesAddSymbol, id = self.menu_libraries_add_symbol.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onButtonRefreshLibrariesClick( self, event ):
		event.Skip()

	def onMenuLibrariesAddFolder( self, event ):
		event.Skip()

	def onMenuLibrariesAddLibrary( self, event ):
		event.Skip()

	def onMenuLibrariesRename( self, event ):
		event.Skip()

	def onMenuLibrariesRemove( self, event ):
		event.Skip()

	def onMenuLibrariesAddSymbol( self, event ):
		event.Skip()

	def PanelSymbolLibrariesOnContextMenu( self, event ):
		self.PopupMenu( self.menu_libraries, event.GetPosition() )


