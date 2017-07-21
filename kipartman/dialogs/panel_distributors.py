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
## Class PanelDistributors
###########################################################################

class PanelDistributors ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		self.m_splitter2.SetMinimumPaneSize( 300 )
		
		self.panel_distributors = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_add_distributor = wx.BitmapButton( self.panel_distributors, wx.ID_ANY, wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_add_distributor, 0, wx.ALL, 5 )
		
		self.button_edit_distributor = wx.BitmapButton( self.panel_distributors, wx.ID_ANY, wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_edit_distributor, 0, wx.ALL, 5 )
		
		self.button_remove_distributor = wx.BitmapButton( self.panel_distributors, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.button_remove_distributor, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_refresh_distributors = wx.BitmapButton( self.panel_distributors, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer6.Add( self.button_refresh_distributors, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer6, 0, 0, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		self.tree_distributors = wx.dataview.DataViewCtrl( self.panel_distributors, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.tree_distributors, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_distributors.SetSizer( bSizer2 )
		self.panel_distributors.Layout()
		bSizer2.Fit( self.panel_distributors )
		self.panel_edit_distributor = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self.panel_edit_distributor, wx.ID_ANY, u"Distributor", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_distributor_name = wx.TextCtrl( self.panel_edit_distributor, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_distributor_name, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.panel_edit_distributor, wx.ID_ANY, u"Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_distributor_address = wx.TextCtrl( self.panel_edit_distributor, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		fgSizer1.Add( self.edit_distributor_address, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.panel_edit_distributor, wx.ID_ANY, u"Website", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_distributor_website = wx.TextCtrl( self.panel_edit_distributor, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_distributor_website, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText7 = wx.StaticText( self.panel_edit_distributor, wx.ID_ANY, u"SKU URL", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		fgSizer1.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_distributor_sku_url = wx.TextCtrl( self.panel_edit_distributor, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_distributor_sku_url, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText8 = wx.StaticText( self.panel_edit_distributor, wx.ID_ANY, u"Email", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		fgSizer1.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_distributor_email = wx.TextCtrl( self.panel_edit_distributor, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_distributor_email, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText9 = wx.StaticText( self.panel_edit_distributor, wx.ID_ANY, u"Phone", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		fgSizer1.Add( self.m_staticText9, 0, wx.ALL, 5 )
		
		self.edit_distributor_phone = wx.TextCtrl( self.panel_edit_distributor, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_distributor_phone, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText11 = wx.StaticText( self.panel_edit_distributor, wx.ID_ANY, u"Comment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		fgSizer1.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_distributor_comment = wx.TextCtrl( self.panel_edit_distributor, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		fgSizer1.Add( self.edit_distributor_comment, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		bSizer3.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1Apply = wx.Button( self.panel_edit_distributor, wx.ID_APPLY )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Apply )
		self.m_sdbSizer1Cancel = wx.Button( self.panel_edit_distributor, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();
		
		bSizer3.Add( m_sdbSizer1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		self.panel_edit_distributor.SetSizer( bSizer3 )
		self.panel_edit_distributor.Layout()
		bSizer3.Fit( self.panel_edit_distributor )
		self.m_splitter2.SplitVertically( self.panel_distributors, self.panel_edit_distributor, 294 )
		bSizer1.Add( self.m_splitter2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_add_distributor.Bind( wx.EVT_BUTTON, self.onButtonAddDistributorClick )
		self.button_edit_distributor.Bind( wx.EVT_BUTTON, self.onButtonEditDistributorClick )
		self.button_remove_distributor.Bind( wx.EVT_BUTTON, self.onButtonRemoveDistributorClick )
		self.button_refresh_distributors.Bind( wx.EVT_BUTTON, self.onButtonRefreshDistributorsClick )
		self.m_sdbSizer1Apply.Bind( wx.EVT_BUTTON, self.onApplyButtonClick )
		self.m_sdbSizer1Cancel.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()
	
	def onButtonAddDistributorClick( self, event ):
		event.Skip()
	
	def onButtonEditDistributorClick( self, event ):
		event.Skip()
	
	def onButtonRemoveDistributorClick( self, event ):
		event.Skip()
	
	def onButtonRefreshDistributorsClick( self, event ):
		event.Skip()
	
	def onApplyButtonClick( self, event ):
		event.Skip()
	
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 294 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	

