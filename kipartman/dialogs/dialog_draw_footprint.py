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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1485,851 ), style = wx.DEFAULT_FRAME_STYLE|wx.MINIMIZE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.panel_draw = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.image_draw = wx.StaticBitmap( self.panel_draw, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.image_draw.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.image_draw.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		bSizer6.Add( self.image_draw, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_draw.SetSizer( bSizer6 )
		self.panel_draw.Layout()
		bSizer6.Fit( self.panel_draw )
		self.m_panel2 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.splitter_edit_object = wx.SplitterWindow( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.splitter_edit_object.Bind( wx.EVT_IDLE, self.splitter_edit_objectOnIdle )
		
		self.m_panel3 = wx.Panel( self.splitter_edit_object, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel6 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer61 = wx.BoxSizer( wx.VERTICAL )
		
		self.tree_layers = wx.dataview.DataViewCtrl( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer61.Add( self.tree_layers, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel6.SetSizer( bSizer61 )
		self.m_panel6.Layout()
		bSizer61.Fit( self.m_panel6 )
		self.m_notebook1.AddPage( self.m_panel6, u"Layers", False )
		
		bSizer8.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_panel3.SetSizer( bSizer8 )
		self.m_panel3.Layout()
		bSizer8.Fit( self.m_panel3 )
		self.panel_edit_object = wx.Panel( self.splitter_edit_object, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_edit_object.SplitHorizontally( self.m_panel3, self.panel_edit_object, 294 )
		bSizer7.Add( self.splitter_edit_object, 1, wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer7 )
		self.m_panel2.Layout()
		bSizer7.Fit( self.m_panel2 )
		self.m_splitter1.SplitVertically( self.panel_draw, self.m_panel2, 1191 )
		bSizer1.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.status_bar = self.CreateStatusBar( 3, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.menu = wx.MenuBar( 0 )
		self.menu_file = wx.Menu()
		self.menu_file_save = wx.MenuItem( self.menu_file, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_file.Append( self.menu_file_save )
		
		self.menu_file_save_as = wx.MenuItem( self.menu_file, wx.ID_ANY, u"Save as ...", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_file.Append( self.menu_file_save_as )
		
		self.menu.Append( self.menu_file, u"File" ) 
		
		self.menu_draw = wx.Menu()
		self.menu_draw_pad = wx.MenuItem( self.menu_draw, wx.ID_ANY, u"Pad", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_draw.Append( self.menu_draw_pad )
		
		self.menu_draw_pad_row = wx.MenuItem( self.menu_draw, wx.ID_ANY, u"Pad row", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_draw.Append( self.menu_draw_pad_row )
		
		self.menu_draw_pad_array = wx.MenuItem( self.menu_draw, wx.ID_ANY, u"Pad array", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_draw.Append( self.menu_draw_pad_array )
		
		self.menu_draw_polyline = wx.MenuItem( self.menu_draw, wx.ID_ANY, u"Polyline", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_draw.Append( self.menu_draw_polyline )
		
		self.menu_draw_arc = wx.MenuItem( self.menu_draw, wx.ID_ANY, u"Arc", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_draw.Append( self.menu_draw_arc )
		
		self.menu_draw_circle = wx.MenuItem( self.menu_draw, wx.ID_ANY, u"Circle", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_draw.Append( self.menu_draw_circle )
		
		self.menu_draw_text = wx.MenuItem( self.menu_draw, wx.ID_ANY, u"Text", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_draw.Append( self.menu_draw_text )
		
		self.menu.Append( self.menu_draw, u"Draw" ) 
		
		self.menu_tool = wx.Menu()
		self.menu_tool_dimension = wx.MenuItem( self.menu_tool, wx.ID_ANY, u"Dimension", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_tool.Append( self.menu_tool_dimension )
		
		self.menu_tool_angle = wx.MenuItem( self.menu_tool, wx.ID_ANY, u"Angle", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_tool.Append( self.menu_tool_angle )
		
		self.menu_tool_grid = wx.MenuItem( self.menu_tool, wx.ID_ANY, u"Grid", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_tool.Append( self.menu_tool_grid )
		
		self.menu_tool_vertical = wx.MenuItem( self.menu_tool, wx.ID_ANY, u"Vertical", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_tool.Append( self.menu_tool_vertical )
		
		self.menu_tool_horizontal = wx.MenuItem( self.menu_tool, wx.ID_ANY, u"Horizontal", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_tool.Append( self.menu_tool_horizontal )
		
		self.menu_tool_line = wx.MenuItem( self.menu_tool, wx.ID_ANY, u"Line", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_tool.Append( self.menu_tool_line )
		
		self.menu.Append( self.menu_tool, u"Tool" ) 
		
		self.menu_zoom = wx.Menu()
		self.menu_zoom_reset = wx.MenuItem( self.menu_zoom, wx.ID_ANY, u"Reset", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_zoom.Append( self.menu_zoom_reset )
		
		self.menu_zoom_in = wx.MenuItem( self.menu_zoom, wx.ID_ANY, u"Zoom in", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_zoom.Append( self.menu_zoom_in )
		
		self.menu_zoom_out = wx.MenuItem( self.menu_zoom, wx.ID_ANY, u"Zoom out", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_zoom.Append( self.menu_zoom_out )
		
		self.menu.Append( self.menu_zoom, u"Zoom" ) 
		
		self.menu_edit = wx.Menu()
		self.menu_edit_duplicate = wx.MenuItem( self.menu_edit, wx.ID_ANY, u"Duplicate", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_edit.Append( self.menu_edit_duplicate )
		
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
		self.image_draw.Bind( wx.EVT_SIZE, self.onImageDrawSize )
		self.Bind( wx.EVT_MENU, self.onMenuFileSaveSelection, id = self.menu_file_save.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuFileSaveAsSelection, id = self.menu_file_save_as.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDrawPadSelection, id = self.menu_draw_pad.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDrawPadRowSelection, id = self.menu_draw_pad_row.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDrawPadArraySelection, id = self.menu_draw_pad_array.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDrawPolylineSelection, id = self.menu_draw_polyline.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDrawArcSelection, id = self.menu_draw_arc.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDrawCircleSelection, id = self.menu_draw_circle.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDrawTextSelection, id = self.menu_draw_text.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuToolDimensionSelection, id = self.menu_tool_dimension.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuToolAngleSelection, id = self.menu_tool_angle.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuToolGridSelection, id = self.menu_tool_grid.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuToolVerticalSelection, id = self.menu_tool_vertical.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuToolHorizontalSelection, id = self.menu_tool_horizontal.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuToolLineSelection, id = self.menu_tool_line.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuZoomResetSelection, id = self.menu_zoom_reset.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuZoomInSelection, id = self.menu_zoom_in.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuZoomOutSelection, id = self.menu_zoom_out.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuEditDuplicateSelection, id = self.menu_edit_duplicate.GetId() )
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
	
	def onImageDrawSize( self, event ):
		event.Skip()
	
	def onMenuFileSaveSelection( self, event ):
		event.Skip()
	
	def onMenuFileSaveAsSelection( self, event ):
		event.Skip()
	
	def onMenuDrawPadSelection( self, event ):
		event.Skip()
	
	def onMenuDrawPadRowSelection( self, event ):
		event.Skip()
	
	def onMenuDrawPadArraySelection( self, event ):
		event.Skip()
	
	def onMenuDrawPolylineSelection( self, event ):
		event.Skip()
	
	def onMenuDrawArcSelection( self, event ):
		event.Skip()
	
	def onMenuDrawCircleSelection( self, event ):
		event.Skip()
	
	def onMenuDrawTextSelection( self, event ):
		event.Skip()
	
	def onMenuToolDimensionSelection( self, event ):
		event.Skip()
	
	def onMenuToolAngleSelection( self, event ):
		event.Skip()
	
	def onMenuToolGridSelection( self, event ):
		event.Skip()
	
	def onMenuToolVerticalSelection( self, event ):
		event.Skip()
	
	def onMenuToolHorizontalSelection( self, event ):
		event.Skip()
	
	def onMenuToolLineSelection( self, event ):
		event.Skip()
	
	def onMenuZoomResetSelection( self, event ):
		event.Skip()
	
	def onMenuZoomInSelection( self, event ):
		event.Skip()
	
	def onMenuZoomOutSelection( self, event ):
		event.Skip()
	
	def onMenuEditDuplicateSelection( self, event ):
		event.Skip()
	
	def onMenuEditMoveSelection( self, event ):
		event.Skip()
	
	def onMenuEditRemoveSelection( self, event ):
		event.Skip()
	
	def onMenuEditRotateSelection( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 1191 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	
	def splitter_edit_objectOnIdle( self, event ):
		self.splitter_edit_object.SetSashPosition( 294 )
		self.splitter_edit_object.Unbind( wx.EVT_IDLE )
	

