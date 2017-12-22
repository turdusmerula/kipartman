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
## Class PanelFootprintsProto
###########################################################################

class PanelFootprintsProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		self.m_splitter2.SetMinimumPaneSize( 300 )
		
		self.panel_category = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_refresh_categories = wx.BitmapButton( self.panel_category, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.button_refresh_categories, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.ALIGN_RIGHT, 5 )
		
		self.tree_libraries = wx.dataview.DataViewCtrl( self.panel_category, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer2.Add( self.tree_libraries, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_category.SetSizer( bSizer2 )
		self.panel_category.Layout()
		bSizer2.Fit( self.panel_category )
		self.m_panel3 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.footprint_splitter = wx.SplitterWindow( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.footprint_splitter.Bind( wx.EVT_IDLE, self.footprint_splitterOnIdle )
		
		self.panel_footprints = wx.Panel( self.footprint_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.filters_panel = wx.Panel( self.panel_footprints, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer161 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15 = wx.StaticText( self.filters_panel, wx.ID_ANY, u"Filters: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		bSizer161.Add( self.m_staticText15, 0, wx.ALL, 5 )
		
		
		self.filters_panel.SetSizer( bSizer161 )
		self.filters_panel.Layout()
		bSizer161.Fit( self.filters_panel )
		bSizer12.Add( self.filters_panel, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.toolbar_footprint = wx.ToolBar( self.panel_footprints, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.button_add_footprint = self.toolbar_footprint.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.button_edit_footprint = self.toolbar_footprint.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.button_remove_footprint = self.toolbar_footprint.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toolbar_footprint.AddSeparator()
		
		self.toggle_footprint_path = self.toolbar_footprint.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/tree_mode.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toolbar_footprint.AddSeparator()
		
		self.button_update_footprint = self.toolbar_footprint.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/update.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.button_commit_footprint = self.toolbar_footprint.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/commit.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toggle_show_showboth_changes = self.toolbar_footprint.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_both.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toggle_show_conflict_changes = self.toolbar_footprint.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_conf.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toggle_show_incoming_changes = self.toolbar_footprint.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_in.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toggle_show_outgoing_changes = self.toolbar_footprint.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_out.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toolbar_footprint.Realize() 
		
		bSizer10.Add( self.toolbar_footprint, 1, wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.search_footprints = wx.SearchCtrl( self.panel_footprints, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_footprints.ShowSearchButton( True )
		self.search_footprints.ShowCancelButton( False )
		self.search_footprints.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer61.Add( self.search_footprints, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.button_refresh_footprints = wx.BitmapButton( self.panel_footprints, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer61.Add( self.button_refresh_footprints, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer61, 0, 0, 5 )
		
		
		bSizer7.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		self.tree_footprints = wx.dataview.DataViewCtrl( self.panel_footprints, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer7.Add( self.tree_footprints, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer12.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		self.panel_footprints.SetSizer( bSizer12 )
		self.panel_footprints.Layout()
		bSizer12.Fit( self.panel_footprints )
		self.footprint_splitter.Initialize( self.panel_footprints )
		bSizer3.Add( self.footprint_splitter, 1, wx.EXPAND, 5 )
		
		
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
		self.search_footprints.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchFootprintsButton )
		self.search_footprints.Bind( wx.EVT_TEXT_ENTER, self.onSearchFootprintsTextEnter )
		self.button_refresh_footprints.Bind( wx.EVT_BUTTON, self.onButtonRefreshFootprintsClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()
	
	def onButtonRefreshCategoriesClick( self, event ):
		event.Skip()
	
	def onSearchFootprintsButton( self, event ):
		event.Skip()
	
	def onSearchFootprintsTextEnter( self, event ):
		event.Skip()
	
	def onButtonRefreshFootprintsClick( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 294 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	
	def footprint_splitterOnIdle( self, event ):
		self.footprint_splitter.SetSashPosition( 455 )
		self.footprint_splitter.Unbind( wx.EVT_IDLE )
	

