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
## Class DialogBuy
###########################################################################

class DialogBuy ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Buy parts", pos = wx.DefaultPosition, size = wx.Size( 1205,752 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.panel_boms = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer4.Add( bSizer111, 0, wx.EXPAND, 0 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_splitter31 = wx.SplitterWindow( self.panel_boms, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter31.Bind( wx.EVT_IDLE, self.m_splitter31OnIdle )
		
		self.m_panel31 = wx.Panel( self.m_splitter31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter311 = wx.SplitterWindow( self.m_panel31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter311.Bind( wx.EVT_IDLE, self.m_splitter311OnIdle )
		
		self.m_panel311 = wx.Panel( self.m_splitter311, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer211 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3111 = wx.StaticText( self.m_panel311, wx.ID_ANY, u"Boms:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3111.Wrap( -1 )
		bSizer17.Add( self.m_staticText3111, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.spin_quantity = wx.SpinCtrl( self.m_panel311, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 9999999, 1 )
		bSizer17.Add( self.spin_quantity, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.toolbar_boms = wx.ToolBar( self.m_panel311, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.toolbar_boms_refresh = self.toolbar_boms.AddLabelTool( wx.ID_ANY, u"Refresh", wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Refresh boms", wx.EmptyString, None ) 
		
		self.toolbar_boms.Realize() 
		
		bSizer17.Add( self.toolbar_boms, 0, wx.EXPAND, 5 )
		
		
		bSizer211.Add( bSizer17, 0, wx.EXPAND, 5 )
		
		self.tree_boms = wx.dataview.DataViewCtrl( self.m_panel311, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer211.Add( self.tree_boms, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel311.SetSizer( bSizer211 )
		self.m_panel311.Layout()
		bSizer211.Fit( self.m_panel311 )
		self.m_panel411 = wx.Panel( self.m_splitter311, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer221 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText311 = wx.StaticText( self.m_panel411, wx.ID_ANY, u"Parts:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText311.Wrap( -1 )
		bSizer221.Add( self.m_staticText311, 0, wx.ALL, 5 )
		
		self.tree_bom_parts = wx.dataview.DataViewCtrl( self.m_panel411, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer221.Add( self.tree_bom_parts, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel411.SetSizer( bSizer221 )
		self.m_panel411.Layout()
		bSizer221.Fit( self.m_panel411 )
		self.m_splitter311.SplitHorizontally( self.m_panel311, self.m_panel411, 158 )
		bSizer21.Add( self.m_splitter311, 1, wx.EXPAND, 5 )
		
		
		self.m_panel31.SetSizer( bSizer21 )
		self.m_panel31.Layout()
		bSizer21.Fit( self.m_panel31 )
		self.m_panel41 = wx.Panel( self.m_splitter31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer22 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText31 = wx.StaticText( self.m_panel41, wx.ID_ANY, u"Equivalent parts:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		bSizer22.Add( self.m_staticText31, 0, wx.ALL, 5 )
		
		self.tree_part_equivalents = wx.dataview.DataViewCtrl( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_MULTIPLE )
		bSizer22.Add( self.tree_part_equivalents, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel41.SetSizer( bSizer22 )
		self.m_panel41.Layout()
		bSizer22.Fit( self.m_panel41 )
		self.m_splitter31.SplitHorizontally( self.m_panel31, self.m_panel41, 575 )
		bSizer8.Add( self.m_splitter31, 1, wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		
		self.panel_boms.SetSizer( bSizer4 )
		self.panel_boms.Layout()
		bSizer4.Fit( self.panel_boms )
		self.panel_buy = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter3 = wx.SplitterWindow( self.panel_buy, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )
		
		self.m_panel3 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer41 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_toolBar2 = wx.ToolBar( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.tool_distributors_view_all_prices = self.m_toolBar2.AddLabelTool( wx.ID_ANY, u"view all prices", wx.Bitmap( u"resources/hide.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, u"View all prices", wx.EmptyString, None ) 
		
		self.m_toolBar2.AddSeparator()
		
		self.tool_distributors_collapse_all = self.m_toolBar2.AddLabelTool( wx.ID_ANY, u"Collapse all", wx.Bitmap( u"resources/collapseall.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Collapse all", wx.EmptyString, None ) 
		
		self.tool_distributors_expand_all = self.m_toolBar2.AddLabelTool( wx.ID_ANY, u"Expand all", wx.Bitmap( u"resources/expandall.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Expand all", wx.EmptyString, None ) 
		
		self.m_toolBar2.Realize() 
		
		bSizer14.Add( self.m_toolBar2, 0, wx.EXPAND, 5 )
		
		
		bSizer41.Add( bSizer14, 0, wx.EXPAND, 5 )
		
		self.tree_distributors = wx.dataview.DataViewCtrl( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_VARIABLE_LINE_HEIGHT )
		bSizer41.Add( self.tree_distributors, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( bSizer41 )
		self.m_panel3.Layout()
		bSizer41.Fit( self.m_panel3 )
		self.m_panel4 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.tree_wish_parts = wx.dataview.DataViewCtrl( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_VARIABLE_LINE_HEIGHT )
		bSizer10.Add( self.tree_wish_parts, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Total:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer11.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_total_price = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_READONLY|wx.TE_RIGHT )
		bSizer11.Add( self.text_total_price, 0, wx.ALL, 5 )
		
		self.static_total_price = wx.StaticText( self.m_panel4, wx.ID_ANY, u"EUR", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.static_total_price.Wrap( -1 )
		bSizer11.Add( self.static_total_price, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer10.Add( bSizer11, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.m_panel4.SetSizer( bSizer10 )
		self.m_panel4.Layout()
		bSizer10.Fit( self.m_panel4 )
		self.m_splitter3.SplitHorizontally( self.m_panel3, self.m_panel4, 351 )
		bSizer5.Add( self.m_splitter3, 1, wx.EXPAND, 5 )
		
		
		self.panel_buy.SetSizer( bSizer5 )
		self.panel_buy.Layout()
		bSizer5.Fit( self.panel_buy )
		self.m_splitter1.SplitVertically( self.panel_boms, self.panel_buy, 639 )
		bSizer3.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		self.menu_main = wx.MenuBar( 0 )
		self.menu_basket = wx.Menu()
		self.menu_basket_open = wx.MenuItem( self.menu_basket, wx.ID_ANY, u"Open", u"Open a basket file", wx.ITEM_NORMAL )
		self.menu_basket.Append( self.menu_basket_open )
		
		self.menu_basket_save = wx.MenuItem( self.menu_basket, wx.ID_ANY, u"Save", u"Save current basket", wx.ITEM_NORMAL )
		self.menu_basket.Append( self.menu_basket_save )
		
		self.menu_basket_save_as = wx.MenuItem( self.menu_basket, wx.ID_ANY, u"Save basket as ...", u"Save basket in a new location ", wx.ITEM_NORMAL )
		self.menu_basket.Append( self.menu_basket_save_as )
		
		self.menu_main.Append( self.menu_basket, u"Basket" ) 
		
		self.menu_boms = wx.Menu()
		self.menu_boms_add = wx.MenuItem( self.menu_boms, wx.ID_ANY, u"Add bom", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_boms.Append( self.menu_boms_add )
		
		self.menu_boms_remove = wx.MenuItem( self.menu_boms, wx.ID_ANY, u"Remove bom", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_boms.Append( self.menu_boms_remove )
		
		self.menu_main.Append( self.menu_boms, u"Bom" ) 
		
		self.menu_prices = wx.Menu()
		self.menu_item_reference_add = wx.MenuItem( self.menu_prices, wx.ID_ANY, u"Add reference", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_prices.Append( self.menu_item_reference_add )
		
		self.menu_prices.AppendSeparator()
		
		self.menu_item_prices_select_bestprice = wx.MenuItem( self.menu_prices, wx.ID_ANY, u"Select best price", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_prices.Append( self.menu_item_prices_select_bestprice )
		
		self.menu_item_prices_automatic_order = wx.MenuItem( self.menu_prices, wx.ID_ANY, u"Automatic complete order", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_prices.Append( self.menu_item_prices_automatic_order )
		
		self.menu_main.Append( self.menu_prices, u"Prices" ) 
		
		self.menu_distributors = wx.Menu()
		self.menu_distributors_refresh_prices = wx.MenuItem( self.menu_distributors, wx.ID_ANY, u"Refresh prices", u"Refresh prices", wx.ITEM_NORMAL )
		self.menu_distributors.Append( self.menu_distributors_refresh_prices )
		
		self.menu_main.Append( self.menu_distributors, u"Distributors" ) 
		
		self.SetMenuBar( self.menu_main )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.spin_quantity.Bind( wx.EVT_SPINCTRL, self.onSpinQuantityCtrl )
		self.Bind( wx.EVT_TOOL, self.onButtonRefreshClick, id = self.toolbar_boms_refresh.GetId() )
		self.tree_bom_parts.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreeBomPartsSelectionChanged, id = wx.ID_ANY )
		self.tree_part_equivalents.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreePartEquivalentsSelectionChanged, id = wx.ID_ANY )
		self.Bind( wx.EVT_TOOL, self.onToolDistributorsViewAllPrices, id = self.tool_distributors_view_all_prices.GetId() )
		self.Bind( wx.EVT_TOOL, self.onToolDistributorsCollapseAll, id = self.tool_distributors_collapse_all.GetId() )
		self.Bind( wx.EVT_TOOL, self.onToolDistributorsExpandAll, id = self.tool_distributors_expand_all.GetId() )
		self.tree_distributors.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreeDistributorsSelectionChanged, id = wx.ID_ANY )
		self.Bind( wx.EVT_MENU, self.onMenuBasketOpenSelection, id = self.menu_basket_open.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuBasketSaveSelection, id = self.menu_basket_save.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuBasketSaveAsSelection, id = self.menu_basket_save_as.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuBomsAddSelection, id = self.menu_boms_add.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuBomsRemoveSelection, id = self.menu_boms_remove.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemPriceAddSelection, id = self.menu_item_reference_add.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemPricesSelectBestpriceSelection, id = self.menu_item_prices_select_bestprice.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemPricesAutomaticOrderSelection, id = self.menu_item_prices_automatic_order.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDistributorsRefreshPrices, id = self.menu_distributors_refresh_prices.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSpinQuantityCtrl( self, event ):
		event.Skip()
	
	def onButtonRefreshClick( self, event ):
		event.Skip()
	
	def onTreeBomPartsSelectionChanged( self, event ):
		event.Skip()
	
	def onTreePartEquivalentsSelectionChanged( self, event ):
		event.Skip()
	
	def onToolDistributorsViewAllPrices( self, event ):
		event.Skip()
	
	def onToolDistributorsCollapseAll( self, event ):
		event.Skip()
	
	def onToolDistributorsExpandAll( self, event ):
		event.Skip()
	
	def onTreeDistributorsSelectionChanged( self, event ):
		event.Skip()
	
	def onMenuBasketOpenSelection( self, event ):
		event.Skip()
	
	def onMenuBasketSaveSelection( self, event ):
		event.Skip()
	
	def onMenuBasketSaveAsSelection( self, event ):
		event.Skip()
	
	def onMenuBomsAddSelection( self, event ):
		event.Skip()
	
	def onMenuBomsRemoveSelection( self, event ):
		event.Skip()
	
	def onMenuItemPriceAddSelection( self, event ):
		event.Skip()
	
	def onMenuItemPricesSelectBestpriceSelection( self, event ):
		event.Skip()
	
	def onMenuItemPricesAutomaticOrderSelection( self, event ):
		event.Skip()
	
	def onMenuDistributorsRefreshPrices( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 639 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	
	def m_splitter31OnIdle( self, event ):
		self.m_splitter31.SetSashPosition( 575 )
		self.m_splitter31.Unbind( wx.EVT_IDLE )
	
	def m_splitter311OnIdle( self, event ):
		self.m_splitter311.SetSashPosition( 158 )
		self.m_splitter311.Unbind( wx.EVT_IDLE )
	
	def m_splitter3OnIdle( self, event ):
		self.m_splitter3.SetSashPosition( 351 )
		self.m_splitter3.Unbind( wx.EVT_IDLE )
	

