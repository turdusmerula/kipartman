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
		
		self.tree_categories = wx.TreeCtrl( self.panel_category, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HIDE_ROOT|wx.TR_ROW_LINES )
		bSizer2.Add( self.tree_categories, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_category.SetSizer( bSizer2 )
		self.panel_category.Layout()
		bSizer2.Fit( self.panel_category )
		self.m_panel3 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter21 = wx.SplitterWindow( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter21.Bind( wx.EVT_IDLE, self.m_splitter21OnIdle )
		self.m_splitter21.SetMinimumPaneSize( 300 )
		
		self.panel_parts = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
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
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_part = wx.BitmapButton( self.panel_parts, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_add_part, 0, wx.ALL, 5 )
		
		self.button_edit_part = wx.BitmapButton( self.panel_parts, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_edit_part, 0, wx.ALL, 5 )
		
		self.button_remove_part = wx.BitmapButton( self.panel_parts, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_remove_part, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.search_parts = wx.SearchCtrl( self.panel_parts, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_parts.ShowSearchButton( True )
		self.search_parts.ShowCancelButton( False )
		self.search_parts.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer61.Add( self.search_parts, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.button_refresh_parts = wx.BitmapButton( self.panel_parts, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer61.Add( self.button_refresh_parts, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer61, 0, 0, 5 )
		
		
		bSizer12.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		self.tree_parts = wx.dataview.DataViewCtrl( self.panel_parts, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.tree_parts, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_parts.SetSizer( bSizer12 )
		self.panel_parts.Layout()
		bSizer12.Fit( self.panel_parts )
		self.panel_edit_part = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self.panel_edit_part, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_name = wx.TextCtrl( self.panel_edit_part, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_part_name, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_staticText4 = wx.StaticText( self.panel_edit_part, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_description = wx.TextCtrl( self.panel_edit_part, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_part_description, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.panel_edit_part, wx.ID_ANY, u"Footprint", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.choice_part_footprint = wx.Choicebook( self.panel_edit_part, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CHB_DEFAULT )
		fgSizer1.Add( self.choice_part_footprint, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.panel_edit_part, wx.ID_ANY, u"Comment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_comment = wx.TextCtrl( self.panel_edit_part, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.edit_part_comment.SetMinSize( wx.Size( -1,120 ) )
		
		fgSizer1.Add( self.edit_part_comment, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer13.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		button_part_edit = wx.StdDialogButtonSizer()
		self.button_part_editApply = wx.Button( self.panel_edit_part, wx.ID_APPLY )
		button_part_edit.AddButton( self.button_part_editApply )
		self.button_part_editCancel = wx.Button( self.panel_edit_part, wx.ID_CANCEL )
		button_part_edit.AddButton( self.button_part_editCancel )
		button_part_edit.Realize();
		
		bSizer13.Add( button_part_edit, 0, wx.EXPAND, 5 )
		
		
		self.panel_edit_part.SetSizer( bSizer13 )
		self.panel_edit_part.Layout()
		bSizer13.Fit( self.panel_edit_part )
		self.m_splitter21.SplitHorizontally( self.panel_parts, self.panel_edit_part, 442 )
		bSizer7.Add( self.m_splitter21, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
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
		self.tree_parts.Bind( wx.dataview.EVT_DATAVIEW_ITEM_COLLAPSED, self.onTreePartsItemCollapsed, id = wx.ID_ANY )
		self.tree_parts.Bind( wx.dataview.EVT_DATAVIEW_ITEM_DROP, self.onTreePartsItemDrop, id = wx.ID_ANY )
		self.tree_parts.Bind( wx.dataview.EVT_DATAVIEW_ITEM_EXPANDED, self.onTreePartsItemExpanded, id = wx.ID_ANY )
		self.tree_parts.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreePartsSelectionChanged, id = wx.ID_ANY )
		self.edit_part_name.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.edit_part_description.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.choice_part_footprint.Bind( wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.onChoiceEditPartPartChanged )
		self.edit_part_comment.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.button_part_editApply.Bind( wx.EVT_BUTTON, self.onButtonPartEditApply )
		self.button_part_editCancel.Bind( wx.EVT_BUTTON, self.onButtonPartEditCancel )
	
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
	
	def onTreePartsItemCollapsed( self, event ):
		event.Skip()
	
	def onTreePartsItemDrop( self, event ):
		event.Skip()
	
	def onTreePartsItemExpanded( self, event ):
		event.Skip()
	
	def onTreePartsSelectionChanged( self, event ):
		event.Skip()
	
	def onTextEditPartPartText( self, event ):
		event.Skip()
	
	
	def onChoiceEditPartPartChanged( self, event ):
		event.Skip()
	
	
	def onButtonPartEditApply( self, event ):
		event.Skip()
	
	def onButtonPartEditCancel( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 294 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	
	def m_splitter21OnIdle( self, event ):
		self.m_splitter21.SetSashPosition( 442 )
		self.m_splitter21.Unbind( wx.EVT_IDLE )
	

