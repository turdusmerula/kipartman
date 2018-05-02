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
## Class DialogProject
###########################################################################

class DialogProject ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Kipartman", pos = wx.DefaultPosition, size = wx.Size( 1160,686 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		self.menu_bar = wx.MenuBar( 0 )
		self.menu_view = wx.Menu()
		self.menu_view_configuration = wx.MenuItem( self.menu_view, wx.ID_ANY, u"Configuration", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_view.Append( self.menu_view_configuration )
		
		self.menu_bar.Append( self.menu_view, u"View" ) 
		
		self.menu_help = wx.Menu()
		self.menu_about = wx.MenuItem( self.menu_help, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_help.Append( self.menu_about )
		
		self.menu_bar.Append( self.menu_help, u"Help" ) 
		
		self.SetMenuBar( self.menu_bar )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.sizer_project = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.sizer_project.Bind( wx.EVT_IDLE, self.sizer_projectOnIdle )
		
		self.panel_project = wx.Panel( self.sizer_project, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_refresh_project = wx.BitmapButton( self.panel_project, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.button_refresh_project, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.ALIGN_RIGHT, 5 )
		
		self.tree_project = wx.dataview.DataViewCtrl( self.panel_project, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer2.Add( self.tree_project, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_project.SetSizer( bSizer2 )
		self.panel_project.Layout()
		bSizer2.Fit( self.panel_project )
		self.menu_project = wx.Menu()
		self.menu_project_open = wx.MenuItem( self.menu_project, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_project.Append( self.menu_project_open )
		
		self.menu_project.AppendSeparator()
		
		self.menu_project_new_bom = wx.MenuItem( self.menu_project, wx.ID_ANY, u"New BOM", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_project.Append( self.menu_project_new_bom )
		
		self.panel_project.Bind( wx.EVT_RIGHT_DOWN, self.panel_projectOnContextMenu ) 
		
		self.panel_file = wx.Panel( self.sizer_project, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer41 = wx.BoxSizer( wx.VERTICAL )
		
		self.notebook = wx.Notebook( self.panel_file, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		bSizer41.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.panel_file.SetSizer( bSizer41 )
		self.panel_file.Layout()
		bSizer41.Fit( self.panel_file )
		self.sizer_project.SplitVertically( self.panel_project, self.panel_file, 294 )
		bSizer5.Add( self.sizer_project, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer5 )
		self.Layout()
		self.status = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_KILL_FOCUS, self.onKillFocus )
		self.Bind( wx.EVT_MENU, self.onMenuViewConfigurationSelection, id = self.menu_view_configuration.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuHelpAboutSelection, id = self.menu_about.GetId() )
		self.button_refresh_project.Bind( wx.EVT_BUTTON, self.onButtonRefreshProjectClick )
		self.Bind( wx.EVT_MENU, self.onMenuProjectOpenSelection, id = self.menu_project_open.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuProjectNewBomSelection, id = self.menu_project_new_bom.GetId() )
		self.notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onNotebookPageChanged )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onKillFocus( self, event ):
		event.Skip()
	
	def onMenuViewConfigurationSelection( self, event ):
		event.Skip()
	
	def onMenuHelpAboutSelection( self, event ):
		event.Skip()
	
	def onButtonRefreshProjectClick( self, event ):
		event.Skip()
	
	def onMenuProjectOpenSelection( self, event ):
		event.Skip()
	
	def onMenuProjectNewBomSelection( self, event ):
		event.Skip()
	
	def onNotebookPageChanged( self, event ):
		event.Skip()
	
	def sizer_projectOnIdle( self, event ):
		self.sizer_project.SetSashPosition( 294 )
		self.sizer_project.Unbind( wx.EVT_IDLE )
	
	def panel_projectOnContextMenu( self, event ):
		self.panel_project.PopupMenu( self.menu_project, event.GetPosition() )
		

