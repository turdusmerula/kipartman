# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jul 12 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelStorages
###########################################################################

class PanelStorages ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		self.m_splitter2.SetMinimumPaneSize( 300 )
		
		self.panel_category = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_category = wx.BitmapButton( self.panel_category, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_add_category, 0, wx.ALL, 5 )
		
		self.button_edit_category = wx.BitmapButton( self.panel_category, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_edit_category, 0, wx.ALL, 5 )
		
		self.button_remove_category = wx.BitmapButton( self.panel_category, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_remove_category, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_refresh_categories = wx.BitmapButton( self.panel_category, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer6.Add( self.button_refresh_categories, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer6, 0, 0, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		self.tree_categories = wx.dataview.DataViewCtrl( self.panel_category, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer2.Add( self.tree_categories, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_category.SetSizer( bSizer2 )
		self.panel_category.Layout()
		bSizer2.Fit( self.panel_category )
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
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_storage = wx.BitmapButton( self.panel_storage_locations, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_add_storage, 0, wx.ALL, 5 )
		
		self.button_edit_storage = wx.BitmapButton( self.panel_storage_locations, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_edit_storage, 0, wx.ALL, 5 )
		
		self.button_remove_storage = wx.BitmapButton( self.panel_storage_locations, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_remove_storage, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.search_storages = wx.SearchCtrl( self.panel_storage_locations, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_storages.ShowSearchButton( True )
		self.search_storages.ShowCancelButton( False )
		self.search_storages.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer61.Add( self.search_storages, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.button_refresh_storages = wx.BitmapButton( self.panel_storage_locations, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer61.Add( self.button_refresh_storages, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer61, 0, 0, 5 )
		
		
		bSizer7.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		self.tree_storages = wx.dataview.DataViewCtrl( self.panel_storage_locations, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer7.Add( self.tree_storages, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer25.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		self.panel_storage_locations.SetSizer( bSizer25 )
		self.panel_storage_locations.Layout()
		bSizer25.Fit( self.panel_storage_locations )
		self.panel_storage_parts = wx.Panel( self.storage_parts_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer121 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer71 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_storage_part = wx.BitmapButton( self.panel_storage_parts, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer101.Add( self.button_add_storage_part, 0, wx.ALL, 5 )
		
		self.button_remove_storage_part = wx.BitmapButton( self.panel_storage_parts, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer101.Add( self.button_remove_storage_part, 0, wx.ALL, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.panel_storage_parts, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer101.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.spin_num_parts = wx.SpinCtrl( self.panel_storage_parts, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 99999999, 0 )
		bSizer101.Add( self.spin_num_parts, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.button_add_storage_item = wx.BitmapButton( self.panel_storage_parts, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer101.Add( self.button_add_storage_item, 0, wx.ALL, 5 )
		
		self.button_remove_storage_item = wx.BitmapButton( self.panel_storage_parts, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer101.Add( self.button_remove_storage_item, 0, wx.ALL, 5 )
		
		
		bSizer111.Add( bSizer101, 1, wx.EXPAND, 5 )
		
		
		bSizer71.Add( bSizer111, 0, wx.EXPAND, 5 )
		
		self.tree_storage_parts = wx.dataview.DataViewCtrl( self.panel_storage_parts, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer71.Add( self.tree_storage_parts, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer121.Add( bSizer71, 1, wx.EXPAND, 5 )
		
		
		self.panel_storage_parts.SetSizer( bSizer121 )
		self.panel_storage_parts.Layout()
		bSizer121.Fit( self.panel_storage_parts )
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
		self.button_add_category.Bind( wx.EVT_BUTTON, self.onButtonAddCategoryClick )
		self.button_edit_category.Bind( wx.EVT_BUTTON, self.onButtonEditCategoryClick )
		self.button_remove_category.Bind( wx.EVT_BUTTON, self.onButtonRemoveCategoryClick )
		self.button_refresh_categories.Bind( wx.EVT_BUTTON, self.onButtonRefreshCategoriesClick )
		self.button_add_storage.Bind( wx.EVT_BUTTON, self.onButtonAddStorageClick )
		self.button_edit_storage.Bind( wx.EVT_BUTTON, self.onButtonEditStorageClick )
		self.button_remove_storage.Bind( wx.EVT_BUTTON, self.onButtonRemoveStorageClick )
		self.search_storages.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchStoragesButton )
		self.search_storages.Bind( wx.EVT_TEXT_ENTER, self.onSearchStoragesTextEnter )
		self.button_refresh_storages.Bind( wx.EVT_BUTTON, self.onButtonRefreshStoragesClick )
		self.button_add_storage_part.Bind( wx.EVT_BUTTON, self.onButtonAddStoragePartClick )
		self.button_remove_storage_part.Bind( wx.EVT_BUTTON, self.onButtonRemoveStoragePartClick )
		self.button_add_storage_item.Bind( wx.EVT_BUTTON, self.onButtonAddStorageItemClick )
		self.button_remove_storage_item.Bind( wx.EVT_BUTTON, self.onButtonRemoveStorageItemClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()
	
	def onButtonAddCategoryClick( self, event ):
		event.Skip()
	
	def onButtonEditCategoryClick( self, event ):
		event.Skip()
	
	def onButtonRemoveCategoryClick( self, event ):
		event.Skip()
	
	def onButtonRefreshCategoriesClick( self, event ):
		event.Skip()
	
	def onButtonAddStorageClick( self, event ):
		event.Skip()
	
	def onButtonEditStorageClick( self, event ):
		event.Skip()
	
	def onButtonRemoveStorageClick( self, event ):
		event.Skip()
	
	def onSearchStoragesButton( self, event ):
		event.Skip()
	
	def onSearchStoragesTextEnter( self, event ):
		event.Skip()
	
	def onButtonRefreshStoragesClick( self, event ):
		event.Skip()
	
	def onButtonAddStoragePartClick( self, event ):
		event.Skip()
	
	def onButtonRemoveStoragePartClick( self, event ):
		event.Skip()
	
	def onButtonAddStorageItemClick( self, event ):
		event.Skip()
	
	def onButtonRemoveStorageItemClick( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 294 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	
	def storage_splitterOnIdle( self, event ):
		self.storage_splitter.SetSashPosition( 455 )
		self.storage_splitter.Unbind( wx.EVT_IDLE )
	
	def storage_parts_splitterOnIdle( self, event ):
		self.storage_parts_splitter.SetSashPosition( 455 )
		self.storage_parts_splitter.Unbind( wx.EVT_IDLE )
	

