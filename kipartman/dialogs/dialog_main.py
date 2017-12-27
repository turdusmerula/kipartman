# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 22 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DialogMain
###########################################################################

class DialogMain ( wx.Frame ):
	
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
		
		self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		bSizer5.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.info = wx.InfoBar( self )
		self.info.SetShowHideEffects( wx.SHOW_EFFECT_NONE, wx.SHOW_EFFECT_NONE )
		self.info.SetEffectDuration( 500 )
		bSizer5.Add( self.info, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer5 )
		self.Layout()
		self.status = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_KILL_FOCUS, self.onKillFocus )
		self.Bind( wx.EVT_MENU, self.onMenuViewConfigurationSelection, id = self.menu_view_configuration.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuHelpAboutSelection, id = self.menu_about.GetId() )
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
	
	def onNotebookPageChanged( self, event ):
		event.Skip()
	

