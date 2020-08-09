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
## Class PanelStorages
###########################################################################

class PanelStorages ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		self.m_splitter2.SetMinimumPaneSize( 300 )

		self.panel_category = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.button_refresh_categories = wx.BitmapButton( self.panel_category, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.button_refresh_categories.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer4.Add( self.button_refresh_categories, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )

		self.tree_categories = wx.dataview.DataViewCtrl( self.panel_category, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer2.Add( self.tree_categories, 1, wx.ALL|wx.EXPAND, 5 )


		self.panel_category.SetSizer( bSizer2 )
		self.panel_category.Layout()
		bSizer2.Fit( self.panel_category )
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

		self.panel_category.Bind( wx.EVT_RIGHT_DOWN, self.panel_categoryOnContextMenu )

		self.m_panel3 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.storage_splitter = wx.SplitterWindow( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.storage_splitter.Bind( wx.EVT_IDLE, self.storage_splitterOnIdle )

		self.panel_storages = wx.Panel( self.storage_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.storage_parts_splitter = wx.SplitterWindow( self.panel_storages, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.storage_parts_splitter.Bind( wx.EVT_IDLE, self.storage_parts_splitterOnIdle )

		self.panel_storage_locations = wx.Panel( self.storage_parts_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer25 = wx.BoxSizer( wx.VERTICAL )

		self.filters_panel = wx.Panel( self.panel_storage_locations, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer161 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText15 = wx.StaticText( self.filters_panel, wx.ID_ANY, u"Filters: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		bSizer161.Add( self.m_staticText15, 0, wx.ALL, 5 )


		self.filters_panel.SetSizer( bSizer161 )
		self.filters_panel.Layout()
		bSizer161.Fit( self.filters_panel )
		bSizer25.Add( self.filters_panel, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		bSizer112 = wx.BoxSizer( wx.HORIZONTAL )

		self.toolbar_part = wx.ToolBar( self.panel_storage_locations, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.toggle_part_path = self.toolbar_part.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/tree_mode.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None )

		self.toolbar_part.Realize()

		bSizer112.Add( self.toolbar_part, 1, wx.EXPAND, 5 )

		bSizer611 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_parts = wx.SearchCtrl( self.panel_storage_locations, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_parts.ShowSearchButton( True )
		self.search_parts.ShowCancelButton( False )
		self.search_parts.SetMinSize( wx.Size( 200,-1 ) )

		bSizer611.Add( self.search_parts, 0, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_parts = wx.BitmapButton( self.panel_storage_locations, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_parts.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer611.Add( self.button_refresh_parts, 0, wx.ALL, 5 )


		bSizer112.Add( bSizer611, 0, 0, 5 )


		bSizer7.Add( bSizer112, 0, wx.EXPAND, 5 )

		self.tree_storages = wx.dataview.DataViewCtrl( self.panel_storage_locations, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer7.Add( self.tree_storages, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer25.Add( bSizer7, 1, wx.EXPAND, 5 )


		self.panel_storage_locations.SetSizer( bSizer25 )
		self.panel_storage_locations.Layout()
		bSizer25.Fit( self.panel_storage_locations )
		self.menu_storage = wx.Menu()
		self.menu_storage_add_storage = wx.MenuItem( self.menu_storage, wx.ID_ANY, u"Add new storage", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_storage_add_storage.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_storage.Append( self.menu_storage_add_storage )

		self.menu_storage_edit_storage = wx.MenuItem( self.menu_storage, wx.ID_ANY, u"Edit storage", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_storage_edit_storage.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_storage.Append( self.menu_storage_edit_storage )

		self.menu_storage_remove_storage = wx.MenuItem( self.menu_storage, wx.ID_ANY, u"Remove storage", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_storage_remove_storage.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_storage.Append( self.menu_storage_remove_storage )

		self.panel_storage_locations.Bind( wx.EVT_RIGHT_DOWN, self.panel_storage_locationsOnContextMenu )

		self.panel_storage_parts = wx.Panel( self.storage_parts_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer121 = wx.BoxSizer( wx.VERTICAL )

		self.tree_storage_parts = wx.dataview.DataViewCtrl( self.panel_storage_parts, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer121.Add( self.tree_storage_parts, 1, wx.ALL|wx.EXPAND, 5 )


		self.panel_storage_parts.SetSizer( bSizer121 )
		self.panel_storage_parts.Layout()
		bSizer121.Fit( self.panel_storage_parts )
		self.menu_part_storage = wx.Menu()
		self.menu_part_storage_add_part = wx.MenuItem( self.menu_part_storage, wx.ID_ANY, u"Add new category", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_storage_add_part.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part_storage.Append( self.menu_part_storage_add_part )

		self.menu_part_storage_remove_part = wx.MenuItem( self.menu_part_storage, wx.ID_ANY, u"Remove category", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_storage_remove_part.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part_storage.Append( self.menu_part_storage_remove_part )

		self.menu_part_storage.AppendSeparator()

		self.menu_part_storage_add_stock = wx.MenuItem( self.menu_part_storage, wx.ID_ANY, u"Add items to storage", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_storage_add_stock.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part_storage.Append( self.menu_part_storage_add_stock )

		self.menu_part_storage_remove_stock = wx.MenuItem( self.menu_part_storage, wx.ID_ANY, u"Remove items from storage", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_storage_remove_stock.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part_storage.Append( self.menu_part_storage_remove_stock )

		self.panel_storage_parts.Bind( wx.EVT_RIGHT_DOWN, self.panel_storage_partsOnContextMenu )

		self.storage_parts_splitter.SplitHorizontally( self.panel_storage_locations, self.panel_storage_parts, 455 )
		bSizer12.Add( self.storage_parts_splitter, 1, wx.EXPAND, 5 )


		self.panel_storages.SetSizer( bSizer12 )
		self.panel_storages.Layout()
		bSizer12.Fit( self.panel_storages )
		self.storage_splitter.Initialize( self.panel_storages )
		bSizer3.Add( self.storage_splitter, 1, wx.EXPAND, 5 )


		self.m_panel3.SetSizer( bSizer3 )
		self.m_panel3.Layout()
		bSizer3.Fit( self.m_panel3 )
		self.m_splitter2.SplitVertically( self.panel_category, self.m_panel3, 294 )
		bSizer1.Add( self.m_splitter2, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_refresh_categories.Bind( wx.EVT_BUTTON, self.onButtonRefreshCategoriesClick )
		self.Bind( wx.EVT_MENU, self.onMenuCategoryAddCategory, id = self.menu_category_add_category.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuCategoryEditCategory, id = self.menu_category_edit_category.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuCategoryRemoveCategory, id = self.menu_category_remove_category.GetId() )
		self.Bind( wx.EVT_TOOL, self.onToggleCategoryPathClicked, id = self.toggle_part_path.GetId() )
		self.search_parts.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchPartsButton )
		self.search_parts.Bind( wx.EVT_TEXT_ENTER, self.onSearchPartsTextEnter )
		self.button_refresh_parts.Bind( wx.EVT_BUTTON, self.onButtonRefreshPartsClick )
		self.Bind( wx.EVT_MENU, self.onMenuStorageAddStorage, id = self.menu_storage_add_storage.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuStorageEditStorage, id = self.menu_storage_edit_storage.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuStorageRemoveStorage, id = self.menu_storage_remove_storage.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartStorageAddPart, id = self.menu_part_storage_add_part.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartStorageRemovePart, id = self.menu_part_storage_remove_part.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartStorageAddStock, id = self.menu_part_storage_add_stock.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartStorageRemoveStock, id = self.menu_part_storage_remove_stock.GetId() )

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

	def onToggleCategoryPathClicked( self, event ):
		event.Skip()

	def onSearchPartsButton( self, event ):
		event.Skip()

	def onSearchPartsTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshPartsClick( self, event ):
		event.Skip()

	def onMenuStorageAddStorage( self, event ):
		event.Skip()

	def onMenuStorageEditStorage( self, event ):
		event.Skip()

	def onMenuStorageRemoveStorage( self, event ):
		event.Skip()

	def onMenuPartStorageAddPart( self, event ):
		event.Skip()

	def onMenuPartStorageRemovePart( self, event ):
		event.Skip()

	def onMenuPartStorageAddStock( self, event ):
		event.Skip()

	def onMenuPartStorageRemoveStock( self, event ):
		event.Skip()

	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 294 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )

	def panel_categoryOnContextMenu( self, event ):
		self.panel_category.PopupMenu( self.menu_category, event.GetPosition() )

	def storage_splitterOnIdle( self, event ):
		self.storage_splitter.SetSashPosition( 455 )
		self.storage_splitter.Unbind( wx.EVT_IDLE )

	def storage_parts_splitterOnIdle( self, event ):
		self.storage_parts_splitter.SetSashPosition( 455 )
		self.storage_parts_splitter.Unbind( wx.EVT_IDLE )

	def panel_storage_locationsOnContextMenu( self, event ):
		self.panel_storage_locations.PopupMenu( self.menu_storage, event.GetPosition() )

	def panel_storage_partsOnContextMenu( self, event ):
		self.panel_storage_parts.PopupMenu( self.menu_part_storage, event.GetPosition() )


