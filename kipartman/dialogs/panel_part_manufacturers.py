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
## Class PanelPartManufacturers
###########################################################################

class PanelPartManufacturers ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 496,385 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.tree_manufacturers = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_MULTIPLE )
		bSizer12.Add( self.tree_manufacturers, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_manufacturers = wx.Menu()
		self.menu_manufacturer_add_manufacturer = wx.MenuItem( self.menu_manufacturers, wx.ID_ANY, u"Add new manufacturer", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_manufacturer_add_manufacturer.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_manufacturers.Append( self.menu_manufacturer_add_manufacturer )

		self.menu_manufacturer_edit_manufacturer = wx.MenuItem( self.menu_manufacturers, wx.ID_ANY, u"Edit manufacturer", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_manufacturer_edit_manufacturer.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_manufacturers.Append( self.menu_manufacturer_edit_manufacturer )

		self.menu_manufacturer_remove_manufacturer = wx.MenuItem( self.menu_manufacturers, wx.ID_ANY, u"Remove manufacturer", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_manufacturer_remove_manufacturer.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_manufacturers.Append( self.menu_manufacturer_remove_manufacturer )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelPartManufacturersOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_MENU, self.onMenuManufacturerAddManufacturer, id = self.menu_manufacturer_add_manufacturer.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuManufacturerEditManufacturer, id = self.menu_manufacturer_edit_manufacturer.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuManufacturerRemoveManufacturer, id = self.menu_manufacturer_remove_manufacturer.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onMenuManufacturerAddManufacturer( self, event ):
		event.Skip()

	def onMenuManufacturerEditManufacturer( self, event ):
		event.Skip()

	def onMenuManufacturerRemoveManufacturer( self, event ):
		event.Skip()

	def PanelPartManufacturersOnContextMenu( self, event ):
		self.PopupMenu( self.menu_manufacturers, event.GetPosition() )


