# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Apr 29 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PanelEditFootprint
###########################################################################

class PanelEditFootprint ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 926,343 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_splitter3 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )
		
		self.m_panel7 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer162 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.edit_footprint_name = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer162.Add( self.edit_footprint_name, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.button_snapeda = wx.Button( self.m_panel7, wx.ID_ANY, u"SnapEDA", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer162.Add( self.button_snapeda, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( bSizer162, 1, wx.EXPAND, 5 )
		
		self.m_staticText2 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_footprint_description = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_footprint_description, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Comment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_footprint_comment = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.edit_footprint_comment.SetMinSize( wx.Size( -1,90 ) )
		
		fgSizer1.Add( self.edit_footprint_comment, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText42 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Snapeda", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )
		fgSizer1.Add( self.m_staticText42, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer172 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_open_url_snapeda = wx.Button( self.m_panel7, wx.ID_ANY, u"<None>", wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT|wx.NO_BORDER )
		bSizer172.Add( self.button_open_url_snapeda, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.button_remove_url_snapeda = wx.BitmapButton( self.m_panel7, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer172.Add( self.button_remove_url_snapeda, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer1.Add( bSizer172, 1, wx.EXPAND, 5 )
		
		self.m_staticText4 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Image", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_open_file_image = wx.Button( self.m_panel7, wx.ID_ANY, u"<None>", wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT|wx.NO_BORDER )
		bSizer17.Add( self.button_open_file_image, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.button_add_file_image = wx.BitmapButton( self.m_panel7, wx.ID_ANY, wx.Bitmap( u"resources/browse-16x16.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer17.Add( self.button_add_file_image, 0, wx.ALL, 5 )
		
		self.button_remove_file_image = wx.BitmapButton( self.m_panel7, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer17.Add( self.button_remove_file_image, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer1.Add( bSizer17, 1, wx.EXPAND, 5 )
		
		self.m_staticText41 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Footprint", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		fgSizer1.Add( self.m_staticText41, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer171 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_open_file_footprint = wx.Button( self.m_panel7, wx.ID_ANY, u"<None>", wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT|wx.NO_BORDER )
		bSizer171.Add( self.button_open_file_footprint, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.button_add_file_footprint = wx.BitmapButton( self.m_panel7, wx.ID_ANY, wx.Bitmap( u"resources/browse-16x16.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer171.Add( self.button_add_file_footprint, 0, wx.ALL, 5 )
		
		self.button_remove_file_footprint = wx.BitmapButton( self.m_panel7, wx.ID_ANY, wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer171.Add( self.button_remove_file_footprint, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer1.Add( bSizer171, 1, wx.EXPAND, 5 )
		
		
		bSizer15.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		button_footprint_edit = wx.StdDialogButtonSizer()
		self.button_footprint_editApply = wx.Button( self.m_panel7, wx.ID_APPLY )
		button_footprint_edit.AddButton( self.button_footprint_editApply )
		self.button_footprint_editCancel = wx.Button( self.m_panel7, wx.ID_CANCEL )
		button_footprint_edit.AddButton( self.button_footprint_editCancel )
		button_footprint_edit.Realize();
		
		bSizer15.Add( button_footprint_edit, 0, wx.EXPAND, 5 )
		
		
		self.m_panel7.SetSizer( bSizer15 )
		self.m_panel7.Layout()
		bSizer15.Fit( self.m_panel7 )
		self.m_panel8 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		self.bitmap_edit_footprint = wx.StaticBitmap( self.m_panel8, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.bitmap_edit_footprint, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel8.SetSizer( bSizer16 )
		self.m_panel8.Layout()
		bSizer16.Fit( self.m_panel8 )
		self.m_splitter3.SplitVertically( self.m_panel7, self.m_panel8, 0 )
		bSizer1.Add( self.m_splitter3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_snapeda.Bind( wx.EVT_BUTTON, self.onButtonSnapedaClick )
		self.button_open_url_snapeda.Bind( wx.EVT_BUTTON, self.onButtonOpenUrlSnapedaClick )
		self.button_remove_url_snapeda.Bind( wx.EVT_BUTTON, self.onButtonRemoveUrlSnapedaClick )
		self.button_open_file_image.Bind( wx.EVT_BUTTON, self.onButtonOpenFileImageClick )
		self.button_add_file_image.Bind( wx.EVT_BUTTON, self.onButtonAddFileImageClick )
		self.button_remove_file_image.Bind( wx.EVT_BUTTON, self.onButtonRemoveFileImageClick )
		self.button_open_file_footprint.Bind( wx.EVT_BUTTON, self.onButtonOpenFileFootprintClick )
		self.button_add_file_footprint.Bind( wx.EVT_BUTTON, self.onButtonAddFileFootprintClick )
		self.button_remove_file_footprint.Bind( wx.EVT_BUTTON, self.onButtonRemoveFileFootprintClick )
		self.button_footprint_editApply.Bind( wx.EVT_BUTTON, self.onButtonFootprintEditApply )
		self.button_footprint_editCancel.Bind( wx.EVT_BUTTON, self.onButtonFootprintEditCancel )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()
	
	def onButtonSnapedaClick( self, event ):
		event.Skip()
	
	def onButtonOpenUrlSnapedaClick( self, event ):
		event.Skip()
	
	def onButtonRemoveUrlSnapedaClick( self, event ):
		event.Skip()
	
	def onButtonOpenFileImageClick( self, event ):
		event.Skip()
	
	def onButtonAddFileImageClick( self, event ):
		event.Skip()
	
	def onButtonRemoveFileImageClick( self, event ):
		event.Skip()
	
	def onButtonOpenFileFootprintClick( self, event ):
		event.Skip()
	
	def onButtonAddFileFootprintClick( self, event ):
		event.Skip()
	
	def onButtonRemoveFileFootprintClick( self, event ):
		event.Skip()
	
	def onButtonFootprintEditApply( self, event ):
		event.Skip()
	
	def onButtonFootprintEditCancel( self, event ):
		event.Skip()
	
	def m_splitter3OnIdle( self, event ):
		self.m_splitter3.SetSashPosition( 0 )
		self.m_splitter3.Unbind( wx.EVT_IDLE )
	

