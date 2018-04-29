# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 22 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelParts
###########################################################################

class PanelParts ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1361,758 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		self.m_splitter2.SetMinimumPaneSize( 100 )
		
		self.m_panel6 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer161 = wx.BoxSizer( wx.VERTICAL )
		
		self.kicadlink_splitter = wx.SplitterWindow( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.kicadlink_splitter.SetMinimumPaneSize( 100 )
		
		self.panel_category = wx.Panel( self.kicadlink_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_refresh_categories = wx.BitmapButton( self.panel_category, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
		bSizer4.Add( self.button_refresh_categories, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.ALIGN_RIGHT, 5 )
		
		self.tree_categories = wx.dataview.DataViewCtrl( self.panel_category, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
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
		
		self.kicadlink_splitter.Initialize( self.panel_category )
		bSizer161.Add( self.kicadlink_splitter, 1, wx.EXPAND, 5 )
		
		
		bSizer15.Add( bSizer161, 1, wx.EXPAND, 5 )
		
		
		self.m_panel6.SetSizer( bSizer15 )
		self.m_panel6.Layout()
		bSizer15.Fit( self.m_panel6 )
		self.m_panel3 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.part_splitter = wx.SplitterWindow( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.part_splitter.SetMinimumPaneSize( 300 )
		
		self.panel_parts = wx.Panel( self.part_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		filters_sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.filters_panel = wx.Panel( self.panel_parts, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15 = wx.StaticText( self.filters_panel, wx.ID_ANY, u"Filters: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		bSizer16.Add( self.m_staticText15, 0, wx.ALL, 5 )
		
		
		self.filters_panel.SetSizer( bSizer16 )
		self.filters_panel.Layout()
		bSizer16.Fit( self.filters_panel )
		filters_sizer.Add( self.filters_panel, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer12.Add( filters_sizer, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.toolbar_part = wx.ToolBar( self.panel_parts, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.toggle_part_path = self.toolbar_part.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/tree_mode.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toolbar_part.Realize() 
		
		bSizer11.Add( self.toolbar_part, 1, wx.EXPAND, 5 )
		
		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.search_parts = wx.SearchCtrl( self.panel_parts, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_parts.ShowSearchButton( True )
		self.search_parts.ShowCancelButton( False )
		self.search_parts.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer61.Add( self.search_parts, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.button_refresh_parts = wx.BitmapButton( self.panel_parts, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
		bSizer61.Add( self.button_refresh_parts, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer61, 0, 0, 5 )
		
		
		bSizer12.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		self.tree_parts = wx.dataview.DataViewCtrl( self.panel_parts, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.tree_parts, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_parts.SetSizer( bSizer12 )
		self.panel_parts.Layout()
		bSizer12.Fit( self.panel_parts )
		self.menu_parameters = wx.Menu()
		self.menu_parameters_add = wx.MenuItem( self.menu_parameters, wx.ID_ANY, u"Add", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parameters.Append( self.menu_parameters_add )
		
		self.menu_parameters_remove = wx.MenuItem( self.menu_parameters, wx.ID_ANY, u"Remove", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parameters.Append( self.menu_parameters_remove )
		
		self.panel_parts.Bind( wx.EVT_RIGHT_DOWN, self.panel_partsOnContextMenu ) 
		
		self.part_splitter.Initialize( self.panel_parts )
		bSizer7.Add( self.part_splitter, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( bSizer3 )
		self.m_panel3.Layout()
		bSizer3.Fit( self.m_panel3 )
		self.menu_part = wx.Menu()
		self.menu_part_add_part = wx.MenuItem( self.menu_part, wx.ID_ANY, u"Add new part", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_add_part.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part.Append( self.menu_part_add_part )
		
		self.menu_part_edit_part = wx.MenuItem( self.menu_part, wx.ID_ANY, u"Edit part", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_edit_part.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part.Append( self.menu_part_edit_part )
		
		self.menu_part_remove_part = wx.MenuItem( self.menu_part, wx.ID_ANY, u"Remove part", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_remove_part.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part.Append( self.menu_part_remove_part )
		
		self.m_panel3.Bind( wx.EVT_RIGHT_DOWN, self.m_panel3OnContextMenu ) 
		
		self.m_splitter2.SplitVertically( self.m_panel6, self.m_panel3, 308 )
		bSizer1.Add( self.m_splitter2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_parts = wx.Menu()
		self.menu_parts_refresh_octopart = wx.MenuItem( self.menu_parts, wx.ID_ANY, u"Refresh octopart parts", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parts.Append( self.menu_parts_refresh_octopart )
		
		self.menu_parts.AppendSeparator()
		
		self.menu_parts_import_parts = wx.MenuItem( self.menu_parts, wx.ID_ANY, u"Import parts", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parts.Append( self.menu_parts_import_parts )
		
		self.menu_parts_export_parts = wx.MenuItem( self.menu_parts, wx.ID_ANY, u"Export parts", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parts.Append( self.menu_parts_export_parts )
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelPartsOnContextMenu ) 
		
		
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
		self.Bind( wx.EVT_MENU, self.onMenuParametersAddSelection, id = self.menu_parameters_add.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuParametersRemoveSelection, id = self.menu_parameters_remove.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartAddPart, id = self.menu_part_add_part.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartEditPart, id = self.menu_part_edit_part.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartRemovePart, id = self.menu_part_remove_part.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemPartsRefreshOctopart, id = self.menu_parts_refresh_octopart.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemPartsImportParts, id = self.menu_parts_import_parts.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemPartsExportParts, id = self.menu_parts_export_parts.GetId() )
	
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
	
	def onMenuParametersAddSelection( self, event ):
		event.Skip()
	
	def onMenuParametersRemoveSelection( self, event ):
		event.Skip()
	
	def onMenuPartAddPart( self, event ):
		event.Skip()
	
	def onMenuPartEditPart( self, event ):
		event.Skip()
	
	def onMenuPartRemovePart( self, event ):
		event.Skip()
	
	def onMenuItemPartsRefreshOctopart( self, event ):
		event.Skip()
	
	def onMenuItemPartsImportParts( self, event ):
		event.Skip()
	
	def onMenuItemPartsExportParts( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 308 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	
	def panel_categoryOnContextMenu( self, event ):
		self.panel_category.PopupMenu( self.menu_category, event.GetPosition() )
		
	def panel_partsOnContextMenu( self, event ):
		self.panel_parts.PopupMenu( self.menu_parameters, event.GetPosition() )
		
	def m_panel3OnContextMenu( self, event ):
		self.m_panel3.PopupMenu( self.menu_part, event.GetPosition() )
		
	def PanelPartsOnContextMenu( self, event ):
		self.PopupMenu( self.menu_parts, event.GetPosition() )
		

