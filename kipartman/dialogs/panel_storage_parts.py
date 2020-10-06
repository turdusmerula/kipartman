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
## Class PanelStorageParts
###########################################################################

class PanelStorageParts ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1064,241 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer121 = wx.BoxSizer( wx.VERTICAL )

		self.tree_storage_parts = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer121.Add( self.tree_storage_parts, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer121 )
		self.Layout()
		self.menu_part_storage = wx.Menu()
		self.menu_part_storage_add_stock = wx.MenuItem( self.menu_part_storage, wx.ID_ANY, u"Add items to stock", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_storage_add_stock.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part_storage.Append( self.menu_part_storage_add_stock )

		self.menu_part_storage_remove_stock = wx.MenuItem( self.menu_part_storage, wx.ID_ANY, u"Remove items from stock", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_storage_remove_stock.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part_storage.Append( self.menu_part_storage_remove_stock )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelStoragePartsOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.Bind( wx.EVT_MENU, self.onMenuPartStorageAddStock, id = self.menu_part_storage_add_stock.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartStorageRemoveStock, id = self.menu_part_storage_remove_stock.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onMenuPartStorageAddStock( self, event ):
		event.Skip()

	def onMenuPartStorageRemoveStock( self, event ):
		event.Skip()

	def PanelStoragePartsOnContextMenu( self, event ):
		self.PopupMenu( self.menu_part_storage, event.GetPosition() )


