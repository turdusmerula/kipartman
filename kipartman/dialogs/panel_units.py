# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Apr 29 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelUnits
###########################################################################

class PanelUnits ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 655,772 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel5 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		self.m_splitter2.SetMinimumPaneSize( 300 )
		
		self.panel_units = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_unit = wx.BitmapButton( self.panel_units, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_add_unit, 0, wx.ALL, 5 )
		
		self.button_edit_unit = wx.BitmapButton( self.panel_units, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_edit_unit, 0, wx.ALL, 5 )
		
		self.button_remove_unit = wx.BitmapButton( self.panel_units, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_remove_unit, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_refresh_units = wx.BitmapButton( self.panel_units, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer6.Add( self.button_refresh_units, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer6, 0, 0, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		self.tree_units = wx.dataview.DataViewCtrl( self.panel_units, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.tree_units, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_units.SetSizer( bSizer2 )
		self.panel_units.Layout()
		bSizer2.Fit( self.panel_units )
		self.panel_edit_unit = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_splitter2.SplitHorizontally( self.panel_units, self.panel_edit_unit, 447 )
		bSizer14.Add( self.m_splitter2, 1, wx.EXPAND, 5 )
		
		
		self.m_panel5.SetSizer( bSizer14 )
		self.m_panel5.Layout()
		bSizer14.Fit( self.m_panel5 )
		self.m_notebook1.AddPage( self.m_panel5, u"Units", True )
		self.m_panel51 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer141 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter21 = wx.SplitterWindow( self.m_panel51, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter21.Bind( wx.EVT_IDLE, self.m_splitter21OnIdle )
		self.m_splitter21.SetMinimumPaneSize( 300 )
		
		self.panel_unit_prefixes = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_unit_prefix = wx.BitmapButton( self.panel_unit_prefixes, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer51.Add( self.button_add_unit_prefix, 0, wx.ALL, 5 )
		
		self.button_edit_unit_prefix = wx.BitmapButton( self.panel_unit_prefixes, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer51.Add( self.button_edit_unit_prefix, 0, wx.ALL, 5 )
		
		self.button_remove_unit_prefix = wx.BitmapButton( self.panel_unit_prefixes, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer51.Add( self.button_remove_unit_prefix, 0, wx.ALL, 5 )
		
		
		bSizer41.Add( bSizer51, 1, wx.EXPAND, 5 )
		
		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_refresh_unit_prefixes = wx.BitmapButton( self.panel_unit_prefixes, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer61.Add( self.button_refresh_unit_prefixes, 0, wx.ALL, 5 )
		
		
		bSizer41.Add( bSizer61, 0, 0, 5 )
		
		
		bSizer21.Add( bSizer41, 0, wx.EXPAND, 5 )
		
		self.tree_unit_prefixes = wx.dataview.DataViewCtrl( self.panel_unit_prefixes, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.tree_unit_prefixes, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_unit_prefixes.SetSizer( bSizer21 )
		self.panel_unit_prefixes.Layout()
		bSizer21.Fit( self.panel_unit_prefixes )
		self.panel_edit_unit_prefix = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_splitter21.SplitHorizontally( self.panel_unit_prefixes, self.panel_edit_unit_prefix, 414 )
		bSizer141.Add( self.m_splitter21, 1, wx.EXPAND, 5 )
		
		
		self.m_panel51.SetSizer( bSizer141 )
		self.m_panel51.Layout()
		bSizer141.Fit( self.m_panel51 )
		self.m_notebook1.AddPage( self.m_panel51, u"Unit prefixes", False )
		
		bSizer1.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_add_unit.Bind( wx.EVT_BUTTON, self.onButtonAddCategoryClick )
		self.button_edit_unit.Bind( wx.EVT_BUTTON, self.onButtonEditCategoryClick )
		self.button_remove_unit.Bind( wx.EVT_BUTTON, self.onButtonRemoveCategoryClick )
		self.button_refresh_units.Bind( wx.EVT_BUTTON, self.onButtonRefreshCategoriesClick )
		self.tree_units.Bind( wx.dataview.EVT_DATAVIEW_ITEM_BEGIN_DRAG, self.onTreePartsItemBeginDrag, id = wx.ID_ANY )
		self.tree_units.Bind( wx.dataview.EVT_DATAVIEW_ITEM_COLLAPSED, self.onTreePartsItemCollapsed, id = wx.ID_ANY )
		self.tree_units.Bind( wx.dataview.EVT_DATAVIEW_ITEM_DROP, self.onTreePartsItemDrop, id = wx.ID_ANY )
		self.tree_units.Bind( wx.dataview.EVT_DATAVIEW_ITEM_EXPANDED, self.onTreePartsItemExpanded, id = wx.ID_ANY )
		self.tree_units.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreePartsSelectionChanged, id = wx.ID_ANY )
		self.button_add_unit_prefix.Bind( wx.EVT_BUTTON, self.onButtonAddCategoryClick )
		self.button_edit_unit_prefix.Bind( wx.EVT_BUTTON, self.onButtonEditCategoryClick )
		self.button_remove_unit_prefix.Bind( wx.EVT_BUTTON, self.onButtonRemoveCategoryClick )
		self.button_refresh_unit_prefixes.Bind( wx.EVT_BUTTON, self.onButtonRefreshCategoriesClick )
		self.tree_unit_prefixes.Bind( wx.dataview.EVT_DATAVIEW_ITEM_BEGIN_DRAG, self.onTreePartsItemBeginDrag, id = wx.ID_ANY )
		self.tree_unit_prefixes.Bind( wx.dataview.EVT_DATAVIEW_ITEM_COLLAPSED, self.onTreePartsItemCollapsed, id = wx.ID_ANY )
		self.tree_unit_prefixes.Bind( wx.dataview.EVT_DATAVIEW_ITEM_DROP, self.onTreePartsItemDrop, id = wx.ID_ANY )
		self.tree_unit_prefixes.Bind( wx.dataview.EVT_DATAVIEW_ITEM_EXPANDED, self.onTreePartsItemExpanded, id = wx.ID_ANY )
		self.tree_unit_prefixes.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreePartsSelectionChanged, id = wx.ID_ANY )
	
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
	
	def onTreePartsItemBeginDrag( self, event ):
		event.Skip()
	
	def onTreePartsItemCollapsed( self, event ):
		event.Skip()
	
	def onTreePartsItemDrop( self, event ):
		event.Skip()
	
	def onTreePartsItemExpanded( self, event ):
		event.Skip()
	
	def onTreePartsSelectionChanged( self, event ):
		event.Skip()
	
	
	
	
	
	
	
	
	
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 447 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	
	def m_splitter21OnIdle( self, event ):
		self.m_splitter21.SetSashPosition( 414 )
		self.m_splitter21.Unbind( wx.EVT_IDLE )
	

