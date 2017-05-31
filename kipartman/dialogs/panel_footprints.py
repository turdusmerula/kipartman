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
## Class PanelFootprints
###########################################################################

class PanelFootprints ( wx.Panel ):
	
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
		
		self.m_splitter21 = wx.SplitterWindow( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter21.Bind( wx.EVT_IDLE, self.m_splitter21OnIdle )
		
		self.panel_footprints = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
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
		
		self.button_add_footprint = wx.BitmapButton( self.panel_footprints, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_add_footprint, 0, wx.ALL, 5 )
		
		self.button_edit_footprint = wx.BitmapButton( self.panel_footprints, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_edit_footprint, 0, wx.ALL, 5 )
		
		self.button_remove_footprint = wx.BitmapButton( self.panel_footprints, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer10.Add( self.button_remove_footprint, 0, wx.ALL, 5 )
		
		
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
		
		self.tree_footprints = wx.dataview.DataViewCtrl( self.panel_footprints, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.tree_footprints, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer12.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		self.panel_footprints.SetSizer( bSizer12 )
		self.panel_footprints.Layout()
		bSizer12.Fit( self.panel_footprints )
		self.panel_edit_footprint = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel_edit_footprint.SetMinSize( wx.Size( -1,300 ) )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.VERTICAL )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self.panel_edit_footprint, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_footprint_name = wx.TextCtrl( self.panel_edit_footprint, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_footprint_name, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText2 = wx.StaticText( self.panel_edit_footprint, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_footprint_description = wx.TextCtrl( self.panel_edit_footprint, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_footprint_description, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.panel_edit_footprint, wx.ID_ANY, u"Comment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_footprint_comment = wx.TextCtrl( self.panel_edit_footprint, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.edit_footprint_comment.SetMinSize( wx.Size( -1,110 ) )
		
		fgSizer1.Add( self.edit_footprint_comment, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.panel_edit_footprint, wx.ID_ANY, u"Image", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.file_footprint_image = wx.FilePickerCtrl( self.panel_edit_footprint, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		fgSizer1.Add( self.file_footprint_image, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer15.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		button_footprint_edit = wx.StdDialogButtonSizer()
		self.button_footprint_editApply = wx.Button( self.panel_edit_footprint, wx.ID_APPLY )
		button_footprint_edit.AddButton( self.button_footprint_editApply )
		self.button_footprint_editCancel = wx.Button( self.panel_edit_footprint, wx.ID_CANCEL )
		button_footprint_edit.AddButton( self.button_footprint_editCancel )
		button_footprint_edit.Realize();
		
		bSizer15.Add( button_footprint_edit, 0, wx.EXPAND, 5 )
		
		
		bSizer14.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		self.bitmap_edit_footprint = wx.StaticBitmap( self.panel_edit_footprint, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.bitmap_edit_footprint, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer14.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		
		self.panel_edit_footprint.SetSizer( bSizer14 )
		self.panel_edit_footprint.Layout()
		bSizer14.Fit( self.panel_edit_footprint )
		self.m_splitter21.SplitHorizontally( self.panel_footprints, self.panel_edit_footprint, 476 )
		bSizer3.Add( self.m_splitter21, 1, wx.EXPAND, 5 )
		
		
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
		self.button_add_footprint.Bind( wx.EVT_BUTTON, self.onButtonAddFootprintClick )
		self.button_edit_footprint.Bind( wx.EVT_BUTTON, self.onButtonEditFootprintClick )
		self.button_remove_footprint.Bind( wx.EVT_BUTTON, self.onButtonRemoveFootprintClick )
		self.search_footprints.Bind( wx.EVT_TEXT_ENTER, self.onSearchFootprintsTextEnter )
		self.button_refresh_footprints.Bind( wx.EVT_BUTTON, self.onButtonRefreshFootprintsClick )
		self.tree_footprints.Bind( wx.dataview.EVT_DATAVIEW_ITEM_BEGIN_DRAG, self.onTreeFootprintsItemBeginDrag, id = wx.ID_ANY )
		self.tree_footprints.Bind( wx.dataview.EVT_DATAVIEW_ITEM_COLLAPSED, self.onTreeFootprintsItemCollapsed, id = wx.ID_ANY )
		self.tree_footprints.Bind( wx.dataview.EVT_DATAVIEW_ITEM_DROP, self.onTreeFootprintsItemDrop, id = wx.ID_ANY )
		self.tree_footprints.Bind( wx.dataview.EVT_DATAVIEW_ITEM_EXPANDED, self.onTreeFootprintsItemExpanded, id = wx.ID_ANY )
		self.tree_footprints.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreeFootprintsSelectionChanged, id = wx.ID_ANY )
		self.file_footprint_image.Bind( wx.EVT_FILEPICKER_CHANGED, self.onFileFootprintImageChanged )
		self.button_footprint_editApply.Bind( wx.EVT_BUTTON, self.onButtonFootprintEditApply )
		self.button_footprint_editCancel.Bind( wx.EVT_BUTTON, self.onButtonFootprintEditCancel )
	
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
	
	def onButtonAddFootprintClick( self, event ):
		event.Skip()
	
	def onButtonEditFootprintClick( self, event ):
		event.Skip()
	
	def onButtonRemoveFootprintClick( self, event ):
		event.Skip()
	
	def onSearchFootprintsTextEnter( self, event ):
		event.Skip()
	
	def onButtonRefreshFootprintsClick( self, event ):
		event.Skip()
	
	def onTreeFootprintsItemBeginDrag( self, event ):
		event.Skip()
	
	def onTreeFootprintsItemCollapsed( self, event ):
		event.Skip()
	
	def onTreeFootprintsItemDrop( self, event ):
		event.Skip()
	
	def onTreeFootprintsItemExpanded( self, event ):
		event.Skip()
	
	def onTreeFootprintsSelectionChanged( self, event ):
		event.Skip()
	
	def onFileFootprintImageChanged( self, event ):
		event.Skip()
	
	def onButtonFootprintEditApply( self, event ):
		event.Skip()
	
	def onButtonFootprintEditCancel( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 294 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	
	def m_splitter21OnIdle( self, event ):
		self.m_splitter21.SetSashPosition( 476 )
		self.m_splitter21.Unbind( wx.EVT_IDLE )
	

