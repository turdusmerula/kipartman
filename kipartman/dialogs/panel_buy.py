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
## Class PanelBuy
###########################################################################

class PanelBuy ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1149,803 ), style = wx.TAB_TRAVERSAL )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.m_panel1 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer4.Add( bSizer111, 0, wx.EXPAND, 0 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_splitter31 = wx.SplitterWindow( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
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
		bSizer17.Add( self.m_staticText3111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_bom = wx.BitmapButton( self.m_panel311, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer18.Add( self.button_add_bom, 0, wx.ALL, 5 )
		
		self.button_remove_bom = wx.BitmapButton( self.m_panel311, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer18.Add( self.button_remove_bom, 0, wx.ALL, 5 )
		
		self.spin_bom_boards = wx.SpinCtrl( self.m_panel311, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 999999999, 0 )
		bSizer18.Add( self.spin_bom_boards, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer17.Add( bSizer18, 1, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.button_refresh = wx.BitmapButton( self.m_panel311, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer17.Add( self.button_refresh, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
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
		self.m_splitter311.SplitHorizontally( self.m_panel311, self.m_panel411, 0 )
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
		self.m_splitter31.SplitHorizontally( self.m_panel31, self.m_panel41, 0 )
		bSizer8.Add( self.m_splitter31, 1, wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer4 )
		self.m_panel1.Layout()
		bSizer4.Fit( self.m_panel1 )
		self.panel_buy = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer28 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_toolBar1 = wx.ToolBar( self.panel_buy, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.tool_save_basket = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/save-32x32.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Save basket file", wx.EmptyString, None ) 
		
		self.m_toolBar1.Realize() 
		
		bSizer28.Add( self.m_toolBar1, 1, wx.EXPAND, 5 )
		
		
		bSizer5.Add( bSizer28, 0, wx.EXPAND, 5 )
		
		self.m_splitter3 = wx.SplitterWindow( self.panel_buy, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )
		
		self.m_panel3 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer41 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer112 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_wish_parts = wx.BitmapButton( self.m_panel3, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer112.Add( self.button_add_wish_parts, 0, wx.ALL, 5 )
		
		self.spin_add_wish_parts = wx.SpinCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 999999999, 0 )
		bSizer112.Add( self.spin_add_wish_parts, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer41.Add( bSizer112, 0, wx.EXPAND, 5 )
		
		self.tree_distributors = wx.dataview.DataViewCtrl( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_VARIABLE_LINE_HEIGHT )
		bSizer41.Add( self.tree_distributors, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( bSizer41 )
		self.m_panel3.Layout()
		bSizer41.Fit( self.m_panel3 )
		self.m_panel4 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_edit_wish = wx.BitmapButton( self.m_panel4, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer13.Add( self.button_edit_wish, 0, wx.ALL, 5 )
		
		self.button_delete_wish = wx.BitmapButton( self.m_panel4, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer13.Add( self.button_delete_wish, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( bSizer13, 0, wx.EXPAND, 5 )
		
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
		self.m_splitter1.SplitVertically( self.m_panel1, self.panel_buy, 638 )
		bSizer3.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		self.menu_prices = wx.Menu()
		self.menu_item_prices_view_all = wx.MenuItem( self.menu_prices, wx.ID_ANY, u"View all prices", wx.EmptyString, wx.ITEM_CHECK )
		self.menu_prices.AppendItem( self.menu_item_prices_view_all )
		self.menu_item_prices_view_all.Check( True )
		
		self.menu_prices.AppendSeparator()
		
		self.menu_item_prices_select_bestprice = wx.MenuItem( self.menu_prices, wx.ID_ANY, u"Select best price", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_prices.AppendItem( self.menu_item_prices_select_bestprice )
		
		self.menu_item_prices_automatic_order = wx.MenuItem( self.menu_prices, wx.ID_ANY, u"Automatic complete order", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_prices.AppendItem( self.menu_item_prices_automatic_order )
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelBuyOnContextMenu ) 
		
		
		# Connect Events
		self.button_add_bom.Bind( wx.EVT_BUTTON, self.onButtonAddBomClick )
		self.button_remove_bom.Bind( wx.EVT_BUTTON, self.onButtonRemoveBomClick )
		self.spin_bom_boards.Bind( wx.EVT_SPINCTRL, self.onSpinBomBoardsCtrl )
		self.button_refresh.Bind( wx.EVT_BUTTON, self.onButtonRefreshClick )
		self.tree_boms.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreeBomsSelectionChanged, id = wx.ID_ANY )
		self.tree_bom_parts.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreeBomPartsSelectionChanged, id = wx.ID_ANY )
		self.tree_part_equivalents.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreePartEquivalentsSelectionChanged, id = wx.ID_ANY )
		self.Bind( wx.EVT_TOOL, self.onToolSaveBasketClicked, id = self.tool_save_basket.GetId() )
		self.button_add_wish_parts.Bind( wx.EVT_BUTTON, self.onButtonAddWishPartsClick )
		self.tree_distributors.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreeDistributorsSelectionChanged, id = wx.ID_ANY )
		self.button_edit_wish.Bind( wx.EVT_BUTTON, self.onButtonEditWishClick )
		self.button_delete_wish.Bind( wx.EVT_BUTTON, self.onButtonDeleteWishClick )
		self.Bind( wx.EVT_MENU, self.onMenuItemPricesViewAllSelection, id = self.menu_item_prices_view_all.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemPricesSelectBestpriceSelection, id = self.menu_item_prices_select_bestprice.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemPricesAutomaticOrderSelection, id = self.menu_item_prices_automatic_order.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onButtonAddBomClick( self, event ):
		event.Skip()
	
	def onButtonRemoveBomClick( self, event ):
		event.Skip()
	
	def onSpinBomBoardsCtrl( self, event ):
		event.Skip()
	
	def onButtonRefreshClick( self, event ):
		event.Skip()
	
	def onTreeBomsSelectionChanged( self, event ):
		event.Skip()
	
	def onTreeBomPartsSelectionChanged( self, event ):
		event.Skip()
	
	def onTreePartEquivalentsSelectionChanged( self, event ):
		event.Skip()
	
	def onToolSaveBasketClicked( self, event ):
		event.Skip()
	
	def onButtonAddWishPartsClick( self, event ):
		event.Skip()
	
	def onTreeDistributorsSelectionChanged( self, event ):
		event.Skip()
	
	def onButtonEditWishClick( self, event ):
		event.Skip()
	
	def onButtonDeleteWishClick( self, event ):
		event.Skip()
	
	def onMenuItemPricesViewAllSelection( self, event ):
		event.Skip()
	
	def onMenuItemPricesSelectBestpriceSelection( self, event ):
		event.Skip()
	
	def onMenuItemPricesAutomaticOrderSelection( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 638 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	
	def m_splitter31OnIdle( self, event ):
		self.m_splitter31.SetSashPosition( 0 )
		self.m_splitter31.Unbind( wx.EVT_IDLE )
	
	def m_splitter311OnIdle( self, event ):
		self.m_splitter311.SetSashPosition( 0 )
		self.m_splitter311.Unbind( wx.EVT_IDLE )
	
	def m_splitter3OnIdle( self, event ):
		self.m_splitter3.SetSashPosition( 351 )
		self.m_splitter3.Unbind( wx.EVT_IDLE )
	
	def PanelBuyOnContextMenu( self, event ):
		self.PopupMenu( self.menu_prices, event.GetPosition() )
		

