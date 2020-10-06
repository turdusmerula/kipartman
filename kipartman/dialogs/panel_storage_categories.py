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
## Class PanelStorageCategories
###########################################################################

class PanelStorageCategories ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.button_refresh_categories = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.BORDER_NONE )

		self.button_refresh_categories.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer4.Add( self.button_refresh_categories, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )

		self.tree_categories = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer2.Add( self.tree_categories, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_category = wx.Menu()
		self.menu_category_add_category = wx.MenuItem( self.menu_category, wx.ID_ANY, u"Add new category", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_category_add_category.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_category.Append( self.menu_category_add_category )

		self.menu_category_edit_category = wx.MenuItem( self.menu_category, wx.ID_ANY, u"Edit category", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_category_edit_category.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_category.Append( self.menu_category_edit_category )

		self.menu_category_remove_category = wx.MenuItem( self.menu_category, wx.ID_ANY, u"Remove category", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_category_remove_category.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_category.Append( self.menu_category_remove_category )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelStorageCategoriesOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_refresh_categories.Bind( wx.EVT_BUTTON, self.onButtonRefreshCategoriesClick )
		self.Bind( wx.EVT_MENU, self.onMenuCategoryAddCategory, id = self.menu_category_add_category.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuCategoryEditCategory, id = self.menu_category_edit_category.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuCategoryRemoveCategory, id = self.menu_category_remove_category.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onButtonRefreshCategoriesClick( self, event ):
		event.Skip()

	def onMenuCategoryAddCategory( self, event ):
		event.Skip()

	def onMenuCategoryEditCategory( self, event ):
		event.Skip()

	def onMenuCategoryRemoveCategory( self, event ):
		event.Skip()

	def PanelStorageCategoriesOnContextMenu( self, event ):
		self.PopupMenu( self.menu_category, event.GetPosition() )


