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
## Class DialogDrawFootprint
###########################################################################

class DialogDrawFootprint ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1118,762 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.m_panel1 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.image_draw = wx.StaticBitmap( self.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.image_draw.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.image_draw.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		bSizer6.Add( self.image_draw, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer6 )
		self.m_panel1.Layout()
		bSizer6.Fit( self.m_panel1 )
		self.m_panel2 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.splitter_edit_object = wx.SplitterWindow( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.splitter_edit_object.Bind( wx.EVT_IDLE, self.splitter_edit_objectOnIdle )
		
		self.m_panel3 = wx.Panel( self.splitter_edit_object, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.tree_objects = wx.dataview.DataViewCtrl( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.tree_objects, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( bSizer8 )
		self.m_panel3.Layout()
		bSizer8.Fit( self.m_panel3 )
		self.panel_edit_object = wx.Panel( self.splitter_edit_object, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_edit_object.SplitHorizontally( self.m_panel3, self.panel_edit_object, 438 )
		bSizer7.Add( self.splitter_edit_object, 1, wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer7 )
		self.m_panel2.Layout()
		bSizer7.Fit( self.m_panel2 )
		self.m_splitter1.SplitVertically( self.m_panel1, self.m_panel2, 750 )
		bSizer1.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.status_bar = self.CreateStatusBar( 3, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.menu = wx.MenuBar( 0 )
		self.menu_draw = wx.Menu()
		self.menu_draw_pad = wx.MenuItem( self.menu_draw, wx.ID_ANY, u"Pad", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_draw.Append( self.menu_draw_pad )
		
		self.menu.Append( self.menu_draw, u"Draw" ) 
		
		self.menu_tool = wx.Menu()
		self.menu_tool_dimension = wx.MenuItem( self.menu_tool, wx.ID_ANY, u"Dimension", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_tool.Append( self.menu_tool_dimension )
		
		self.menu_tool_grid = wx.MenuItem( self.menu_tool, wx.ID_ANY, u"Grid", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_tool.Append( self.menu_tool_grid )
		
		self.menu.Append( self.menu_tool, u"Tool" ) 
		
		self.menu_zoom = wx.Menu()
		self.menu_zoom_reset = wx.MenuItem( self.menu_zoom, wx.ID_ANY, u"Reset", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_zoom.Append( self.menu_zoom_reset )
		
		self.menu.Append( self.menu_zoom, u"Zoom" ) 
		
		self.menu_edit = wx.Menu()
		self.menu_edit_move = wx.MenuItem( self.menu_edit, wx.ID_ANY, u"Move", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_edit.Append( self.menu_edit_move )
		
		self.menu_edit_remove = wx.MenuItem( self.menu_edit, wx.ID_ANY, u"Remove", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_edit.Append( self.menu_edit_remove )
		
		self.menu_edit_rotate = wx.MenuItem( self.menu_edit, wx.ID_ANY, u"Rotate", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_edit.Append( self.menu_edit_rotate )
		
		self.menu.Append( self.menu_edit, u"Edit" ) 
		
		self.SetMenuBar( self.menu )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.image_draw.Bind( wx.EVT_LEFT_DCLICK, self.onImageDrawLeftDClick )
		self.image_draw.Bind( wx.EVT_LEFT_DOWN, self.onImageDrawLeftDown )
		self.image_draw.Bind( wx.EVT_LEFT_UP, self.onImageDrawLeftUp )
		self.image_draw.Bind( wx.EVT_MIDDLE_DCLICK, self.onImageDrawMiddleDClick )
		self.image_draw.Bind( wx.EVT_MIDDLE_DOWN, self.onImageDrawMiddleDown )
		self.image_draw.Bind( wx.EVT_MIDDLE_UP, self.onImageDrawMiddleUp )
		self.image_draw.Bind( wx.EVT_MOTION, self.onImageDrawMotion )
		self.image_draw.Bind( wx.EVT_LEFT_DOWN, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_LEFT_UP, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_MIDDLE_DOWN, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_MIDDLE_UP, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_RIGHT_DOWN, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_RIGHT_UP, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_MOTION, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_LEFT_DCLICK, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_MIDDLE_DCLICK, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_RIGHT_DCLICK, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_LEAVE_WINDOW, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_ENTER_WINDOW, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_MOUSEWHEEL, self.onImageDrawMouseEvents )
		self.image_draw.Bind( wx.EVT_MOUSEWHEEL, self.onImageDrawMouseWheel )
		self.image_draw.Bind( wx.EVT_RIGHT_DCLICK, self.onImageDrawRightDClick )
		self.image_draw.Bind( wx.EVT_RIGHT_DOWN, self.onImageDrawRightDown )
		self.image_draw.Bind( wx.EVT_RIGHT_UP, self.onImageDrawRightUp )
		self.Bind( wx.EVT_MENU, self.onMenuDrawPadSelection, id = self.menu_draw_pad.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuToolDimensionSelection, id = self.menu_tool_dimension.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuToolGridSelection, id = self.menu_tool_grid.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuZoomResetSelection, id = self.menu_zoom_reset.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuEditMoveSelection, id = self.menu_edit_move.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuEditRemoveSelection, id = self.menu_edit_remove.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuEditRotateSelection, id = self.menu_edit_rotate.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onImageDrawLeftDClick( self, event ):
		event.Skip()
	
	def onImageDrawLeftDown( self, event ):
		event.Skip()
	
	def onImageDrawLeftUp( self, event ):
		event.Skip()
	
	def onImageDrawMiddleDClick( self, event ):
		event.Skip()
	
	def onImageDrawMiddleDown( self, event ):
		event.Skip()
	
	def onImageDrawMiddleUp( self, event ):
		event.Skip()
	
	def onImageDrawMotion( self, event ):
		event.Skip()
	
	def onImageDrawMouseEvents( self, event ):
		event.Skip()
	
	def onImageDrawMouseWheel( self, event ):
		event.Skip()
	
	def onImageDrawRightDClick( self, event ):
		event.Skip()
	
	def onImageDrawRightDown( self, event ):
		event.Skip()
	
	def onImageDrawRightUp( self, event ):
		event.Skip()
	
	def onMenuDrawPadSelection( self, event ):
		event.Skip()
	
	def onMenuToolDimensionSelection( self, event ):
		event.Skip()
	
	def onMenuToolGridSelection( self, event ):
		event.Skip()
	
	def onMenuZoomResetSelection( self, event ):
		event.Skip()
	
	def onMenuEditMoveSelection( self, event ):
		event.Skip()
	
	def onMenuEditRemoveSelection( self, event ):
		event.Skip()
	
	def onMenuEditRotateSelection( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 750 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	
	def splitter_edit_objectOnIdle( self, event ):
		self.splitter_edit_object.SetSashPosition( 438 )
		self.splitter_edit_object.Unbind( wx.EVT_IDLE )
	

