# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Dec 18 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelPartStorages
###########################################################################

class PanelPartStorages ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 496,385 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.tree_storages = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.tree_storages, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_storage = wx.Menu()
		self.menu_storage_add_storage = wx.MenuItem( self.menu_storage, wx.ID_ANY, u"Add new storage location", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_storage_add_storage.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_storage.Append( self.menu_storage_add_storage )

		self.menu_storage_edit_storage = wx.MenuItem( self.menu_storage, wx.ID_ANY, u"Edit storage location", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_storage_edit_storage.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_storage.Append( self.menu_storage_edit_storage )

		self.menu_storage_remove_storage = wx.MenuItem( self.menu_storage, wx.ID_ANY, u"Remove storage location", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_storage_remove_storage.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_storage.Append( self.menu_storage_remove_storage )

		self.menu_storage.AppendSeparator()

		self.menu_storage_add_stock = wx.MenuItem( self.menu_storage, wx.ID_ANY, u"Add items to storage", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_storage_add_stock.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_storage.Append( self.menu_storage_add_stock )

		self.menu_storage_remove_stock = wx.MenuItem( self.menu_storage, wx.ID_ANY, u"Remove items from storage", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_storage_remove_stock.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_storage.Append( self.menu_storage_remove_stock )



		# Connect Events
		self.Bind( wx.EVT_MENU, self.onMenuStorageAddStorage, id = self.menu_storage_add_storage.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuStorageEditStorage, id = self.menu_storage_edit_storage.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuStorageRemoveStorage, id = self.menu_storage_remove_storage.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuStorageAddStock, id = self.menu_storage_add_stock.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuStorageRemoveStock, id = self.menu_storage_remove_stock.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onMenuStorageAddStorage( self, event ):
		event.Skip()

	def onMenuStorageEditStorage( self, event ):
		event.Skip()

	def onMenuStorageRemoveStorage( self, event ):
		event.Skip()

	def onMenuStorageAddStock( self, event ):
		event.Skip()

	def onMenuStorageRemoveStock( self, event ):
		event.Skip()


