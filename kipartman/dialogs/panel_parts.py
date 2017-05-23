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
## Class PanelParts
###########################################################################

class PanelParts ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		
		self.m_panel2 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_category = wx.BitmapButton( self.m_panel2, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_add_category, 0, wx.ALL, 5 )
		
		self.button_edit_category = wx.BitmapButton( self.m_panel2, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_edit_category, 0, wx.ALL, 5 )
		
		self.button_remove_category = wx.BitmapButton( self.m_panel2, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_remove_category, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_refresh_categories = wx.BitmapButton( self.m_panel2, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer6.Add( self.button_refresh_categories, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer6, 0, 0, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		self.tree_categories = wx.TreeCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HIDE_ROOT|wx.TR_ROW_LINES )
		bSizer2.Add( self.tree_categories, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer2 )
		self.m_panel2.Layout()
		bSizer2.Fit( self.m_panel2 )
		self.m_panel3 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_checkBox1 = wx.CheckBox( self.m_panel3, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_checkBox1, 0, wx.ALL, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_part = wx.BitmapButton( self.m_panel3, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_add_part, 0, wx.ALL, 5 )
		
		self.button_edit_part = wx.BitmapButton( self.m_panel3, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_edit_part, 0, wx.ALL, 5 )
		
		self.button_remove_part = wx.BitmapButton( self.m_panel3, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_remove_part, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.search_parts = wx.SearchCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.search_parts.ShowSearchButton( True )
		self.search_parts.ShowCancelButton( False )
		self.search_parts.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer61.Add( self.search_parts, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.button_refresh_parts = wx.BitmapButton( self.m_panel3, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer61.Add( self.button_refresh_parts, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer61, 0, 0, 5 )
		
		
		bSizer7.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		self.tree_parts = wx.dataview.DataViewCtrl( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.tree_parts, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( bSizer3 )
		self.m_panel3.Layout()
		bSizer3.Fit( self.m_panel3 )
		self.m_splitter2.SplitVertically( self.m_panel2, self.m_panel3, 294 )
		bSizer1.Add( self.m_splitter2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_add_category.Bind( wx.EVT_BUTTON, self.onButtonAddCategoryClick )
		self.button_edit_category.Bind( wx.EVT_BUTTON, self.onButtonEditCategoryClick )
		self.button_remove_category.Bind( wx.EVT_BUTTON, self.onButtonRemoveCategoryClick )
		self.button_refresh_categories.Bind( wx.EVT_BUTTON, self.onButtonRefreshCategoriesClick )
		self.tree_categories.Bind( wx.EVT_CHAR, self.onTreeCategoriesOnChar )
		self.tree_categories.Bind( wx.EVT_TREE_BEGIN_DRAG, self.onTreeCategoriesBeginDrag )
		self.tree_categories.Bind( wx.EVT_TREE_END_DRAG, self.onTreeCategoriesEndDrag )
		self.tree_categories.Bind( wx.EVT_TREE_ITEM_COLLAPSED, self.onTreeCategoriesCollapsed )
		self.tree_categories.Bind( wx.EVT_TREE_ITEM_EXPANDED, self.onTreeCategoriesExpanded )
		self.tree_categories.Bind( wx.EVT_TREE_SEL_CHANGED, self.onTreeCategoriesSelChanged )
		self.tree_categories.Bind( wx.EVT_TREE_SEL_CHANGING, self.onTreeCategoriesSelChanging )
		self.button_add_part.Bind( wx.EVT_BUTTON, self.onButtonAddPartClick )
		self.button_edit_part.Bind( wx.EVT_BUTTON, self.onButtonEditPartClick )
		self.button_remove_part.Bind( wx.EVT_BUTTON, self.onButtonRemovePartClick )
		self.search_parts.Bind( wx.EVT_TEXT_ENTER, self.onSearchPartsTextEnter )
		self.button_refresh_parts.Bind( wx.EVT_BUTTON, self.onButtonRefreshPartsClick )
		self.tree_parts.Bind( wx.dataview.EVT_DATAVIEW_ITEM_BEGIN_DRAG, self.onTreePartsItemBeginDrag, id = wx.ID_ANY )
		self.tree_parts.Bind( wx.dataview.EVT_DATAVIEW_ITEM_DROP, self.onTreePartsItemDrop, id = wx.ID_ANY )
	
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
	
	def onTreeCategoriesOnChar( self, event ):
		event.Skip()
	
	def onTreeCategoriesBeginDrag( self, event ):
		event.Skip()
	
	def onTreeCategoriesEndDrag( self, event ):
		event.Skip()
	
	def onTreeCategoriesCollapsed( self, event ):
		event.Skip()
	
	def onTreeCategoriesExpanded( self, event ):
		event.Skip()
	
	def onTreeCategoriesSelChanged( self, event ):
		event.Skip()
	
	def onTreeCategoriesSelChanging( self, event ):
		event.Skip()
	
	def onButtonAddPartClick( self, event ):
		event.Skip()
	
	def onButtonEditPartClick( self, event ):
		event.Skip()
	
	def onButtonRemovePartClick( self, event ):
		event.Skip()
	
	def onSearchPartsTextEnter( self, event ):
		event.Skip()
	
	def onButtonRefreshPartsClick( self, event ):
		event.Skip()
	
	def onTreePartsItemBeginDrag( self, event ):
		event.Skip()
	
	def onTreePartsItemDrop( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 294 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	

