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
## Class PanelBom
###########################################################################

class PanelBom ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1120,759 ), style = wx.TAB_TRAVERSAL )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.m_panel1 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_toolBar1 = wx.ToolBar( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.tool_open_brd = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/open-32x32.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Open a kicad board", wx.EmptyString, None ) 
		
		self.tool_refresh_brd = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/refresh-32x32.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Refresh module list", wx.EmptyString, None ) 
		
		self.m_toolBar1.Realize() 
		
		bSizer4.Add( self.m_toolBar1, 0, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.tree_modules = wx.dataview.DataViewCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.tree_modules, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.button_add_bom_module = wx.Button( self.m_panel1, wx.ID_ANY, u">>", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer6.Add( self.button_add_bom_module, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.button_remove_bom_module = wx.Button( self.m_panel1, wx.ID_ANY, u"<<", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer6.Add( self.button_remove_bom_module, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer8.Add( bSizer6, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer4.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer4 )
		self.m_panel1.Layout()
		bSizer4.Fit( self.m_panel1 )
		self.m_panel2 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.toolbar_bom = wx.ToolBar( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.tool_save_bom = self.toolbar_bom.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/save-32x32.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Save kipartman BOM file", wx.EmptyString, None ) 
		
		self.toolbar_bom.Realize() 
		
		bSizer9.Add( self.toolbar_bom, 0, wx.EXPAND, 5 )
		
		
		bSizer5.Add( bSizer9, 0, wx.EXPAND, 5 )
		
		self.m_splitter3 = wx.SplitterWindow( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )
		
		self.m_panel3 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer41 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_bom_part = wx.BitmapButton( self.m_panel3, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer51.Add( self.button_add_bom_part, 0, wx.ALL, 5 )
		
		self.button_remove_bom_part = wx.BitmapButton( self.m_panel3, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer51.Add( self.button_remove_bom_part, 0, wx.ALL, 5 )
		
		
		bSizer41.Add( bSizer51, 0, wx.EXPAND, 5 )
		
		self.tree_bom_parts = wx.dataview.DataViewCtrl( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_VARIABLE_LINE_HEIGHT )
		bSizer41.Add( self.tree_bom_parts, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( bSizer41 )
		self.m_panel3.Layout()
		bSizer41.Fit( self.m_panel3 )
		self.m_panel4 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.tree_bom_modules = wx.dataview.DataViewCtrl( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_VARIABLE_LINE_HEIGHT )
		bSizer10.Add( self.tree_bom_modules, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer10 )
		self.m_panel4.Layout()
		bSizer10.Fit( self.m_panel4 )
		self.m_splitter3.SplitHorizontally( self.m_panel3, self.m_panel4, 0 )
		bSizer5.Add( self.m_splitter3, 1, wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer5 )
		self.m_panel2.Layout()
		bSizer5.Fit( self.m_panel2 )
		self.m_splitter1.SplitVertically( self.m_panel1, self.m_panel2, 387 )
		bSizer3.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onToolOpenBrdClicked, id = self.tool_open_brd.GetId() )
		self.Bind( wx.EVT_TOOL, self.onToolRefreshBrd, id = self.tool_refresh_brd.GetId() )
		self.button_add_bom_module.Bind( wx.EVT_BUTTON, self.onButtonAddBomModuleClick )
		self.button_remove_bom_module.Bind( wx.EVT_BUTTON, self.onButtonRemoveBomModuleClick )
		self.Bind( wx.EVT_TOOL, self.onToolSaveBomClicked, id = self.tool_save_bom.GetId() )
		self.button_add_bom_part.Bind( wx.EVT_BUTTON, self.onButtonAddBomPartClick )
		self.button_remove_bom_part.Bind( wx.EVT_BUTTON, self.onButtonRemoveBomPartClick )
		self.tree_bom_parts.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onTreeBomPartsSelectionChanged, id = wx.ID_ANY )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onToolOpenBrdClicked( self, event ):
		event.Skip()
	
	def onToolRefreshBrd( self, event ):
		event.Skip()
	
	def onButtonAddBomModuleClick( self, event ):
		event.Skip()
	
	def onButtonRemoveBomModuleClick( self, event ):
		event.Skip()
	
	def onToolSaveBomClicked( self, event ):
		event.Skip()
	
	def onButtonAddBomPartClick( self, event ):
		event.Skip()
	
	def onButtonRemoveBomPartClick( self, event ):
		event.Skip()
	
	def onTreeBomPartsSelectionChanged( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 387 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	
	def m_splitter3OnIdle( self, event ):
		self.m_splitter3.SetSashPosition( 0 )
		self.m_splitter3.Unbind( wx.EVT_IDLE )
	

