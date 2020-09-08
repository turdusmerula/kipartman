# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep  1 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui

###########################################################################
## Class DialogMain
###########################################################################

class DialogMain ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Kipartman", pos = wx.DefaultPosition, size = wx.Size( 1160,686 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.menu_bar = wx.MenuBar( 0 )
		self.menu_file = wx.Menu()
		self.menu_file_project = wx.MenuItem( self.menu_file, wx.ID_ANY, u"Open project", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_file.Append( self.menu_file_project )

		self.menu_file.AppendSeparator()

		self.menu_buy_parts = wx.MenuItem( self.menu_file, wx.ID_ANY, u"Buy parts", u"Open the buy parts window", wx.ITEM_NORMAL )
		self.menu_file.Append( self.menu_buy_parts )

		self.menu_bar.Append( self.menu_file, u"File" )

		self.menu_view = wx.Menu()
		self.menu_view_configuration = wx.MenuItem( self.menu_view, wx.ID_ANY, u"Configuration", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_view.Append( self.menu_view_configuration )

		self.menu_view.AppendSeparator()

		self.menu_view_parts = wx.MenuItem( self.menu_view, wx.ID_ANY, u"Parts", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_view.Append( self.menu_view_parts )

		self.menu_view_symbols = wx.MenuItem( self.menu_view, wx.ID_ANY, u"Symbols", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_view.Append( self.menu_view_symbols )

		self.menu_view_test = wx.MenuItem( self.menu_view, wx.ID_ANY, u"Test", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_view.Append( self.menu_view_test )

		self.menu_bar.Append( self.menu_view, u"View" )

		self.menu_help = wx.Menu()
		self.menu_about = wx.MenuItem( self.menu_help, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_help.Append( self.menu_about )

		self.menu_bar.Append( self.menu_help, u"Help" )

		self.SetMenuBar( self.menu_bar )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.info = wx.InfoBar( self )
		self.info.SetShowHideEffects( wx.SHOW_EFFECT_NONE, wx.SHOW_EFFECT_NONE )
		self.info.SetEffectDuration( 500 )
		bSizer5.Add( self.info, 0, wx.ALL|wx.EXPAND, 5 )

		self.notebook = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_CLOSE_BUTTON|wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB|wx.aui.AUI_NB_DEFAULT_STYLE|wx.aui.AUI_NB_TAB_MOVE|wx.aui.AUI_NB_TAB_SPLIT )

		bSizer5.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer5 )
		self.Layout()
		self.status = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_KILL_FOCUS, self.onKillFocus )
		self.Bind( wx.EVT_MENU, self.onMenuFileProjetSelection, id = self.menu_file_project.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuBuyPartsSelection, id = self.menu_buy_parts.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuViewConfigurationSelection, id = self.menu_view_configuration.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuViewPartsSelection, id = self.menu_view_parts.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuViewSymbolsSelection, id = self.menu_view_symbols.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuViewTestSelection, id = self.menu_view_test.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuHelpAboutSelection, id = self.menu_about.GetId() )
		self.notebook.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.onNotebookPageChanged )
		self.notebook.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGING, self.onNotebookPageChanging )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onKillFocus( self, event ):
		event.Skip()

	def onMenuFileProjetSelection( self, event ):
		event.Skip()

	def onMenuBuyPartsSelection( self, event ):
		event.Skip()

	def onMenuViewConfigurationSelection( self, event ):
		event.Skip()

	def onMenuViewPartsSelection( self, event ):
		event.Skip()

	def onMenuViewSymbolsSelection( self, event ):
		event.Skip()

	def onMenuViewTestSelection( self, event ):
		event.Skip()

	def onMenuHelpAboutSelection( self, event ):
		event.Skip()

	def onNotebookPageChanged( self, event ):
		event.Skip()

	def onNotebookPageChanging( self, event ):
		event.Skip()


