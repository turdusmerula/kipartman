from dialogs.panel_select_snapeda import PanelSelectSnapeda
from snapeda.queries import PartsQuery
import wx.lib.newevent
import helper.tree
import os
import tempfile
import cfscrape

SelectSnapedaOkEvent, EVT_SELECT_SNAPEDA_OK_EVENT = wx.lib.newevent.NewEvent()
SelectSnapedaCancelEvent, EVT_SELECT_SNAPEDA_APPLY_EVENT = wx.lib.newevent.NewEvent()

scraper = cfscrape.create_scraper()

none_image = os.path.abspath(os.path.join('resources', 'none-128x128.png'))

def NoneValue(value, default):
    if value:
        return value
    return default

class DataModelSnapedaPart(helper.tree.TreeItem):
    def __init__(self, part):
        super(DataModelSnapedaPart, self).__init__()
        self.part = part
    
    def GetValue(self, col):
        package_type = ""
        if self.part.package() and self.part.package().name():
            package_type = self.part.package().name()
        vMap = { 
            0 : self.part.manufacturer(),
            1 : self.part.name(),
            2 : package_type,
            3 : self.part.short_description(),
            4 : self.part._links().self().href(),
        }
        return vMap[col]

            
class SelectSnapedaFrame(PanelSelectSnapeda):
    def __init__(self, parent, initial_search=None, filter=None, preview='symbol'): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectSnapedaFrame, self).__init__(parent)

        self.search_snapeda.Value = initial_search
        self.filter = filter 
        self.preview = preview
        
        # create snapedas list
        self.tree_snapeda_manager = helper.tree.TreeManager(self.tree_snapedas)
        self.tree_snapeda_manager.AddTextColumn("Manufacturer")
        self.tree_snapeda_manager.AddTextColumn("Part")
        self.tree_snapeda_manager.AddTextColumn("Package Type")
        self.tree_snapeda_manager.AddTextColumn("Description")
        self.tree_snapeda_manager.AddTextColumn("URL")
        self.tree_snapeda_manager.OnSelectionChanged = self.onTreeSnapedasSelChanged

        # set result functions
        self.cancel = None
        self.result = None
    
        self.search()
                
    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
    
    def search(self):
        # apply new filter and reload
        self.tree_snapeda_manager.ClearItems()
        if self.search_snapeda.Value!='':
            q = PartsQuery()
            q.get(self.search_snapeda.Value)
            
            for snapeda in q.results():
                if self.filter is None or self.filter(snapeda)==False:
                    self.tree_snapeda_manager.AppendItem(None, DataModelSnapedaPart(snapeda))

    # Virtual event handlers, overide them in your derived class
    def onSearchSnapedaButton( self, event ):
        self.search()
    
    def onSearchSnapedaEnter( self, event ):
        self.search()

    def onTreeSnapedasSelChanged( self, event ):
        item = self.tree_snapedas.GetSelection()
        if item.IsOk()==False:
            return
        snapedaobj = self.tree_snapeda_manager.ItemToObject(item)
        snapeda = snapedaobj.part
        
        print("--", snapeda.json)
        
        # download image
        image_url = ""
        if len(snapeda.models())>0:
            if self.preview=='footprint' and snapeda.models()[0].package_medium():
                image_url = snapeda.models()[0].package_medium().url()
            if self.preview=='symbol' and snapeda.models()[0].symbol_medium():
                image_url = snapeda.models()[0].symbol_medium().url()
            
        if image_url=="" and len(snapeda.coverart())>0:
            image_url = snapeda.coverart()[0].url()
        if image_url!='':
            try:
                filename = os.path.join(tempfile.gettempdir(), os.path.basename(image_url))
                content = scraper.get(image_url).content
                with open(filename, 'wb') as outfile:
                    outfile.write(content)
                outfile.close()
                 
                self.SetImage(filename)
            except Exception as e:
                wx.MessageBox(format(e), 'Error loading image', wx.OK | wx.ICON_ERROR)
        else:
            self.SetImage()
        
    def SetImage(self, filename=none_image):

        img = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        #img = wx.Bitmap(self.file_footprint_image.GetPath(), wx.BITMAP_TYPE_ANY)
        self.PhotoMaxSize = self.bitmap_preview.GetSize().x
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
        img = img.ConvertToBitmap()

        self.bitmap_preview.SetBitmap(img)

    def onButtonCancelClick( self, event ):
        event = SelectSnapedaCancelEvent()
        wx.PostEvent(self, event)
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        sel = self.tree_snapedas.GetSelection()
        if not sel:
            return
        snapeda = self.tree_snapeda_manager.ItemToObject(self.tree_snapedas.GetSelection())
        
        # trigger result event
        event = SelectSnapedaOkEvent(data=snapeda.part)
        wx.PostEvent(self, event)
        if self.result:
            self.result(snapeda.part)
