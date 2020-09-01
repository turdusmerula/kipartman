import datetime
import wx.dataview
import json
from helper.exception import print_stack
from helper.log import log

_treeitem_hash = 0

# base class for tree item container
class TreeItem(object):
    def __init__(self):
#         global _treeitem_hash
#         self._id = _treeitem_hash
#         _treeitem_hash += 1
        
        self.parent = None
        
        self.values = {}
#         self.is_container = None

#     def __hash__(self):
#         return self._id

#     def set_parent(self, manager, parent):
#         self.parent = parent
#         manager.model.ItemChanged(manager.model.ObjectToItem(parent), manager.model.ObjectToItem(self))    
    def _get_value(self, col):
        if col not in self.values:
            self.values[col] = self.GetValue(col)
        return self.values[col]
            
    def GetValue(self, col):
        return ''

    def HasValue(self, col):
        return True
    
    def SetValue(self, value, col):
        return False

    def IsEnabled(self, col):
        return True
    
    def ValueChanged(self, col):
        return False

    def GetAttr(self, col, attr):
        return False

    def GetParent(self):
        return self.parent

#     def _is_container(self):
#         if self.is_container is None:
#             self.is_container = self.IsContainer()
#         return self.is_container
    
    def IsContainer(self):
        return False

    def HasContainerColumns(self):
        return False

    def GetDragData(self):
        return None
    
    def Update(self):
        self.values = {}
#         self.is_container = None

class TreeContainerItem(TreeItem):
    def __init__(self, childs=None):
        super(TreeContainerItem, self).__init__()
        self.childs = None

    def AddChild(self, obj):
        if self.childs is None:
            self.childs = []
        self.childs.append(obj)
        obj.parent = self
        
    def AddChilds(self, parent, objs):
        if len(objs)==0:
            self.childs = []
        for obj in objs:
            self.AddChild(parent, obj)
    
    def RemoveChild(self, obj):
        self.childs.remove(obj)
        obj.parent = None
        
    def HasContainerColumns(self):
        return True

    def IsContainer(self):
        return True # if ( self.childs is not None and len(self.childs)>0 ) else False

class TreeDummyItem(TreeItem):
    pass

class TreeContainerLazyItem(TreeContainerItem):
    def __init__(self):
        super(TreeContainerLazyItem, self).__init__()
        self.loaded = False

    def _lazy_load(self, manager):
        if self.loaded:
            return

        # remove dummy item
        if self.childs is not None and len(self.childs)>0 :
            manager.model.ItemDeleted(manager.model.ObjectToItem(self), manager.model.ObjectToItem(self.childs[0]))
             
        # empty child list
        self.childs = []
        self.loaded = True
        self.Load()
        
        if self.childs is not None:
            for child in self.childs:
                manager.model.ItemAdded(manager.model.ObjectToItem(self), manager.model.ObjectToItem(child))
                if isinstance(child, TreeContainerLazyItem) and child.IsContainer():
                    # add a dummy item to allow this item to appear with childs, it will be remove by lazy_load func
                    manager.Append(child, TreeDummyItem())
                
#         manager.model.ItemChanged(manager.model.ObjectToItem(self))

    # override this for lazy loading childs
    def Load(self):
        pass
    
    def Loaded(self):
        return self.loaded
    
    # override this for lazy loading to indicate if item contains childs
    def IsContainer(self):
        return False

class TreeModel(wx.dataview.PyDataViewModel):
    def __init__(self, root_objs=[]):
        super(TreeModel, self).__init__()
        self.columns_type = {}
        self.columns_name = {}
        
        self.root_objs = root_objs

#         self.UseWeakRefs(True)

    def Load(self):
        pass
    
    def AddChild(self, obj):
        self.root_objs.append(obj)
        obj.parent = None
        
    def AddChilds(self, objs):
        if len(objs)==0:
            self.root_objs = []
        for obj in objs:
            self.AddChild(obj)

    def RemoveChild(self, obj):
        self.root_objs.remove(obj)
        obj.parent = None
        
    def ClearItems(self):
        self.root_objs = []
        
    def GetColumnCount(self):
        return len(self.columns_type)

    def GetColumnType(self, col):
        return self.columns_type[col]

    def GetColumnName(self, col):
        return self.columns_name[col]

    def GetChildren(self, item, children):
        if item.IsOk()==False:
            for obj in self.root_objs:
                children.append(self.ObjectToItem(obj))
            return len(self.root_objs)
            
        obj = self.ItemToObject(item)
        if isinstance(obj, TreeContainerItem) and obj.childs is not None:
            for childobj in obj.childs:
                children.append(self.ObjectToItem(childobj))
            return len(obj.childs)
        
        return 0
    
    def IsContainer(self, item):
        if item.IsOk()==False:
            return True # root node is always a container
        obj = self.ItemToObject(item)
        return obj.IsContainer()
    
    # override this function to return False for columns with no data
    def HasContainerColumns(self, item):
        if item.IsOk()==False:
            return False
        obj = self.ItemToObject(item)
        return obj.HasContainerColumns()

    def GetParent(self, item):
        if item.IsOk()==False:
            return wx.dataview.NullDataViewItem
        obj = self.ItemToObject(item)
        if obj is None or obj.GetParent() is None:
            return wx.dataview.NullDataViewItem
        return self.ObjectToItem(obj.GetParent())
    
    # unless GetValue this functions return the real type of elements, not str (used mainly for compare natural types)
    def GetColumnValue(self, item, col):
        if item.IsOk()==False:
            return ''
        obj = self.ItemToObject(item)
        return obj._get_value(col)

    def GetValue(self, item, col):
        return str(self.GetColumnValue(item, col))

    # override this to provide attributes
    def GetAttr(self, item, col, attr):
        obj = self.ItemToObject(item)
        return obj.GetAttr(col, attr)

    # override this to set item value
    def SetValue(self, value, item, col):
        obj = self.ItemToObject(item)
        res = obj.SetValue(value, col)
        self.ItemChanged(item)
        return res
    
    # override this to indicate if a column has value
    def HasValue(self, item, col):
        obj = self.ItemToObject(item)
        return obj.HasValue(col)

    # override this to indicate if a line is enabled
    def IsEnabled(self, item, col):
        obj = self.ItemToObject(item)
        return obj.IsEnabled(col)
    
    # override this to provide custom compare function
    def Compare(self, item1, item2, column, ascending):
        val1 = self.GetColumnValue(item1, column)
        val2 = self.GetColumnValue(item2, column)
#         print("---", val1, val2)
        if val1==val2:
            return 1 if ascending == (item1.__hash__() > item2.__hash__()) else -1
        else:
            return 1 if ascending == (val1>val2) else -1

class TreeDropTarget(wx.TextDropTarget):
    def __init__(self, manager):
        super(TreeDropTarget, self).__init__()
        self.manager = manager

 #TODO: set drag cursor depending on accept/reject drop
    '''
    @TODO: FIX - onDragOver, in MSW does not show over dataviewitems, 
    @TODO: CHECK onDragOver, in Linux does this fire ?
    @TODO: FIX - (return) only wx.DragCopy works, wx.DragMove shows (ICON Notpossible)
    '''
    def OnDragOver(self, x, y, d):
        if 'logging' in globals():logging.debug(
             "{:%H:%M:%S.%f}  TreeDropTarget:OnDragOver : SuggestedResult:{}".format(
                    datetime.datetime.now(),
                    d
                    ))
        return wx.DragNone  #wx.DragMove

    def OnDropText(self, x, y, text):
        if 'logging' in globals():logging.debug(
            "{:%H:%M:%S.%f}  TreeDropTarget:OnDropText : Position:X{}Y{} Text:{}".format(
                                            datetime.datetime.now(),
                                            x,y,text
                                            ))

        payload = json.loads(text)
        for target in self.manager.drop_targets:
            if payload['type']==target['type']:
                if 'logging' in globals():logging.debug( 
                        "{:%H:%M:%S.%f}  TreeDropTarget:OnDropText(payload process) : target:{} payload:{}".format(
                            datetime.datetime.now(),target['trigger'],payload['data']))
                return target['trigger'](x, y, payload['data'])
        return wx.DragError

class TreeDataObject(wx.TextDataObject):
    def __init__(self, data): 
        super(TreeDataObject, self).__init__()
        self.data = data
        self.SetText(json.dumps({'type': data.__class__.__name__, 'data': data.GetDragData()}))

class TreeImageList(wx.ImageList):
    def __init__(self, width, height, mask=True, initialCount=1):
        super(TreeImageList, self).__init__(width, height, mask, initialCount)
        self.labels = {}
    
    def Add(self, label, *args, **kwargs):
        self.labels[label] = self.GetImageCount()
        return super(TreeImageList, self).Add(*args, **kwargs)

    def AddFile(self, label, path):
        icon = wx.Image(path)
        return self.Add(label, icon.ConvertToBitmap())
    
    def GetBitmap(self, label):
        index = self.labels[label]
        return super(TreeImageList, self).GetBitmap(index)

    def GetIcon(self, label):
        index = self.labels[label]
        return super(TreeImageList, self).GetIcon(index)

    def GetSize(self, label):
        index = self.labels[label]
        return super(TreeImageList, self).GetSize(index)

    def Remove(self, label):
        index = self.labels[label]
        self.labels.pop(label)
        return super(TreeImageList, self).Remove(index)

    def RemoveAll(self, label):
        self.labels.clear()
        return super(TreeImageList, self).RemoveAll()

    def Replace(self, label, *args, **kwargs):
        index = self.labels[label]
        return super(TreeImageList, self).Replace(index, *args, **kwargs)

class TreeManager(object):
    drag_item = None
    drag_source = None
    
    def __init__(self, tree_view, model=None, context_menu=None):
        #TODO ISSUE#8 Debug assist to Try various options
        self.onItemDropPossible_returnResult = 1
        self.onItemDropPossible_eventAction = 1

        self.tree_view = tree_view

        if model==None:
            self.model = TreeModel()
        else:
            self.model = model
        self.tree_view.AssociateModel(self.model)

        if context_menu:
            self.context_menu = context_menu
            context_menu.AppendSeparator()
        else:
            self.context_menu = wx.Menu()
            
        menu_item_copy = wx.MenuItem( self.context_menu, wx.ID_ANY, u"Copy", wx.EmptyString, wx.ITEM_NORMAL )
        self.context_menu.Append( menu_item_copy )
        tree_view.Bind( wx.EVT_MENU, self.onMenuItemCopy, id = menu_item_copy.GetId() )

        self.sorting_column = None
        
        # create drag and drop targets
        self.drop_targets = []
        self.tree_view.EnableDragSource(wx.DataFormat(wx.TextDataObject().GetFormat()))
        self.tree_view.EnableDropTarget(wx.DataFormat(wx.TextDataObject().GetFormat()))
        self.tree_view.SetDropTarget(TreeDropTarget(self))

        # data elements
        self.data = []
        self.data_state = []
        
        self.OnColumnHeaderClick = None
        self.OnColumnHeaderRightClick = None
        self.OnColumnReordered = None
        self.OnColumnSorted = None
        self.OnItemActivated = None
        self.OnItemBeginDrag = None
        self.OnItemCollapsed = None
        self.OnItemCollapsing = None
        self.OnItemBeforeContextMenu = None
        self.OnItemContextMenu = None
        self.OnItemDrop = None
        self.OnItemDropPossible = None
        self.OnItemEditingDone = None
        self.OnItemEditingStarted = None
        self.OnItemExpanded = None
        self.OnItemExpanding = None
        self.OnItemStartEditing = None
        self.OnItemValueChanged = None
        self.OnSelectionChanged = None
        
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_COLUMN_HEADER_CLICK, self._onColumnHeaderClick, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK, self._onColumnHeaderRightClick, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_COLUMN_REORDERED, self._onColumnReordered, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_COLUMN_SORTED, self._onColumnSorted, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self._onItemActivated, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_BEGIN_DRAG, self._onItemBeginDrag, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_COLLAPSED, self._onItemCollapsed, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_COLLAPSING, self._onItemCollapsing, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self._onItemContextMenu, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_DROP, self._onItemDrop, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_DROP_POSSIBLE, self._onItemDropPossible, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_EDITING_DONE, self._onItemEditingDone, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_EDITING_STARTED, self._onItemEditingStarted, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_EXPANDED, self._onItemExpanded, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_EXPANDING, self._onItemExpanding, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_START_EDITING, self._onItemStartEditing, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self._onItemValueChanged, id = wx.ID_ANY )
        self.tree_view.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self._onSelectionChanged, id = wx.ID_ANY )

    def onMenuItemCopy( self, event ):
        [ item, col ] = self.tree_view.HitTest(self.context_menu_pos)
        index = -1
        if col:
            index = col.GetModelColumn() ;
        data = ""
        if self.context_menu_data and index!=-1:
            data = self.context_menu_data.GetValue(index)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(data))
            wx.TheClipboard.Close()
        log.debug("Copy", data, index)

    def _onColumnHeaderClick( self, event ):
        event.manager = self
        if self.OnColumnHeaderClick:
            return self.OnColumnHeaderClick(event)
        event.Skip()
    
    def _onColumnHeaderRightClick( self, event ):
        event.manager = self
        if self.OnColumnHeaderRightClick:
            return self.OnColumnHeaderRightClick(event)
        event.Skip()
    
    def _onColumnReordered( self, event ):
        event.manager = self
        if self.OnColumnReordered:
            return self.OnColumnReordered(event)
        event.Skip()
    
    def _onColumnSorted( self, event ):
        event.manager = self
        if self.OnColumnSorted:
            return self.OnColumnSorted(event)
        event.Skip()
    
    def _onItemActivated( self, event ):
        event.manager = self
        if self.OnItemActivated:
            return self.OnItemActivated(event)
        event.Skip()
    
    def _onItemBeginDrag( self, event ):
        event.manager = self
        '''
        @TODO: Confirm SetDragFlags under Linux
        according to documentation https://wxpython.org/Phoenix/docs/html/wx.dataview.DataViewEvent.html#wx-dataview-dataviewevent

        Currently it is only honoured by the generic version of wx.dataview.DataViewCtrl (used e.g. under MSW)'
        '''
        # Suppress the standard drag symbol on MSW (copy)
        event.SetDragFlags(wx.Drag_DefaultMove)

        TreeManager.drag_item = event.GetItem()
        TreeManager.drag_source = self
        
        if self.drag_item is None:
            event.Skip()
            return wx.DragCancel
        try:
            drag_data = self.model.ItemToObject(event.GetItem())
        except Exception as inst:
            print_stack()
            if 'logging' in globals(): logging.debug('DRAG ERROR:{} {} {} {}'.format(type(inst), inst.message,inst.args,event.GetItem()))
            return wx.DragCancel
        if drag_data.GetDragData() is None:
            event.Skip()
            return wx.DragCancel

        event.SetDataObject(TreeDataObject(drag_data))
        if 'logging' in globals():logging.debug('DRAG onItemBeginDrag STATE:{}'.format(self.OnItemBeginDrag))
        dragSource = wx.DropSource(self.tree_view.TopLevelParent)
        dataObject = TreeDataObject(drag_data)

        if self.OnItemBeginDrag:
            return self.OnItemBeginDrag(event)
        return wx.Drag_DefaultMove

    
    def _onItemCollapsed( self, event ):
        event.manager = self
        if self.OnItemCollapsed:
            return self.OnItemCollapsed(event)
        event.Skip()
    
    def _onItemCollapsing( self, event ):
        event.manager = self
        if self.OnItemCollapsing:
            return self.OnItemCollapsing(event)
        event.Skip()
    
    def _onItemContextMenu( self, event ):
        event.manager = self
        
        if self.OnItemBeforeContextMenu:
            self.OnItemBeforeContextMenu(event)
        if self.context_menu:
            self.context_menu_pos = self.tree_view.ScreenToClient(wx.GetMousePosition())
            if event.GetItem():
                self.context_menu_data = self.model.ItemToObject(event.GetItem())
            else:
                self.context_menu_data = None
            self.tree_view.PopupMenu(self.context_menu, event.GetPosition())
        if self.OnItemContextMenu:
            return self.OnItemContextMenu(event)
        event.Skip()
    
    def _onItemDrop( self, event ):
        event.manager = self
        if 'logging' in globals():logging.debug("{:%H:%M:%S.%f}  TreeManager:onItemDrop self:{} event:{} {}".format(datetime.datetime.now(),
                                    self,
                                    event.GetClassName(),
                                    hex(id(event)).upper(),
                                    ))
        drag_data = self.drag_source.model.ItemToObject(self.drag_source.drag_item)
        if drag_data.GetDragData() is None:
            event.Skip()
            return wx.DragCancel
        sourceDataObject = TreeDataObject(drag_data)
        event.SetDataObject(sourceDataObject)

        mouse_x,mouse_y = wx.GetMousePosition()
        if platform.system()=='Windows':
            #TODO 17W47.5 WORKAROUND for defect 17561.
            # WORKAROUND y-25
            # Q: Can we determine What is the Header Row Height , so we can adjust, also need to detect if the header is displayed ???
            # Q: When will wxWidget fix this? Anything we can do ?, is it specific to MSW
            # BACKGROUND
            '''
            The generic versions of wxDataViewCtrl::HitTest() and wxDataViewCtrl::GetItemRect() do not take the size of the optional header of the control into account. Instead they just forward the calls to the client area (m_clientArea) without correcting the y-coordinate by the height of the optional header (m_headerArea). This leads to wrong results.
    
            From <http://trac.wxwidgets.org/ticket/17561#no1> 
    
            '''
            mouse_x, mouse_y = self.tree_view.ScreenToClient((mouse_x, mouse_y-25))
            #TODO 17W47.7 WORKAROUND for defect xxxxx.
            # WORKAROUND as DropTarget is not called for Dataview Items, call it manually in onDrop
            # BACKGROUND
            '''
            
            '''
        else:
            mouse_x, mouse_y = self.tree_view.ScreenToClient((mouse_x, mouse_y))


        self.tree_view.DropTarget.OnDropText(
            mouse_x, mouse_y, 
            sourceDataObject.Text)

        if self.OnItemDrop:
            return self.OnItemDrop(event)
        event.Allow()
        return True
    
    def _onItemDropPossible( self, event ):
        event.manager = self
        if self.OnItemDropPossible:
            return self.OnItemDropPossible(event) 
            #return False
        '''
        @TODO: Implement Drag Feedback 
         Ok/Not Ok for drop by event.Allow or event.Skip
        
        Hit test on ?
        
        Define:  onItemDropPossible_eventAction 
        if onItemDropPossible_eventAction:
            event.Allow()
        else:
            event.Skip()
            
        @TODO: Undestand as below the event.Skip(False) vs event.Skip(True)
        '''

        #Control the Drag Cursor
        #self.onItemDropPossible_eventAction = 1
        if self.onItemDropPossible_eventAction == 1:
            #Generates a working drag cursor
            event.Allow()
        elif self.onItemDropPossible_eventAction == 2:
            #'banned' cursor (on MSWindows--the cursor that is a circle with a line diagonally through it).
            event.Skip(True)
        elif self.onItemDropPossible_eventAction == 3:
            #Generates a working drag cursor
            event.Skip(False)
        else:
            pass

        #TODO: Debug assist code for Issue#8 DnD, Parts to Categories on MSW
        # if self.onItemDropPossible_returnResult == 1:
        #     return wx.Drag_DefaultMove
        # elif self.onItemDropPossible_returnResult == 2:
        #     return wx.Drag_CopyOnly
        # elif self.onItemDropPossible_returnResult == 3:
        #     return wx.Drag_AllowMove
        # else:
        #     pass

        return wx.Drag_DefaultMove
    
    def _onItemEditingDone( self, event ):
        event.manager = self
        if self.OnItemEditingDone:
            return self.OnItemEditingDone(event)
        event.Skip()
    
    def _onItemEditingStarted( self, event ):
        event.manager = self
        if self.OnItemEditingStarted:
            return self.OnItemEditingStarted(event)
        event.Skip()
    
    def _onItemExpanded( self, event ):
        event.manager = self
        if self.OnItemExpanded:
            return self.OnItemExpanded(event)
        event.Skip()
    
    def _onItemExpanding( self, event ):
        event.manager = self
        item = event.GetItem()
        
        # perform lazy load before expanding
        obj = self.model.ItemToObject(item)
        if isinstance(obj, TreeContainerLazyItem):
            obj._lazy_load(self)
        
        if self.OnItemExpanding:
            return self.OnItemExpanding(event)
        event.Skip()
    
    def _onItemStartEditing( self, event ):
        event.manager = self
        if self.OnItemStartEditing:
            return self.OnItemStartEditing(event)
        event.Skip()
        
    
    def _onItemValueChanged( self, event ):
        event.manager = self
        if self.OnItemValueChanged:
            return self.OnItemValueChanged(event)
        event.Skip()
    
    def _onSelectionChanged( self, event ):
        event.manager = self
        if self.OnSelectionChanged:
            return self.OnSelectionChanged(event)
        event.Skip()


    def AddTextColumn(self, title):
        column = self.tree_view.AppendTextColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type[column.GetModelColumn()] = 'string'
        self.model.columns_name[column.GetModelColumn()] = title
        column.Sortable = True
        column.Reorderable = True
        column.SortOrder = True
        return column
    
    def AddFloatColumn(self, title):
        column = self.tree_view.AppendTextColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type[column.GetModelColumn()] = 'float'
        self.model.columns_name[column.GetModelColumn()] = title
        column.Sortable = True
        column.Reorderable = True
        return column

    def AddIntegerColumn(self, title):
        column = self.tree_view.AppendTextColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type[column.GetModelColumn()] = 'integer'
        self.model.columns_name[column.GetModelColumn()] = title
        column.Sortable = True
        column.Reorderable = True
        return column

    def AddToggleColumn(self, title):
        column = self.tree_view.AppendToggleColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE, mode=wx.dataview.DATAVIEW_CELL_ACTIVATABLE)
        self.model.columns_type[column.GetModelColumn()] = 'integer'
        self.model.columns_name[column.GetModelColumn()] = title
        column.Sortable = True
        column.Reorderable = True
        return column

    def AddCustomColumn(self, title, type):
        column = self.tree_view.AppendTextColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type[column.GetModelColumn()] = type
        self.model.columns_name[column.GetModelColumn()] = title
        column.Sortable = True
        column.Reorderable = True
        return column

    def AddBitmapColumn(self, title):
        column = self.tree_view.AppendBitmapColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type[column.GetModelColumn()] = 'bitmap'
        self.model.columns_name[column.GetModelColumn()] = title
        column.Sortable = True
        column.Reorderable = True
        return column
        
    def RemoveColumns(self, start_index, end_index=-1):
        to_remove = []
        for column in self.tree_view.GetColumns():
            if column.GetModelColumn()>=start_index and end_index==-1:
                to_remove.append(column)
            elif column.GetModelColumn()>=start_index and column.GetModelColumn()<=end_index:
                to_remove.append(column)
        for column in to_remove:
            self.model.columns_name.pop(column.GetModelColumn())
            self.model.columns_type.pop(column.GetModelColumn())
            self.tree_view.DeleteColumn(column)

    def RemoveColumn(self, index):
        for column in self.tree_view.GetColumns():
            if column.GetModelColumn()==index:
                self.model.columns_name.pop(index)
                self.model.columns_type.pop(index)
                self.tree_view.DeleteColumn(column)
                return
                
    def ClearColumns(self):
        while len(self.tree_view.GetColumns())>0:
            self.tree_view.DeleteColumn(self.tree_view.GetColumns()[0])
    
    
    def Load(self):
        pass
        
    def Clear(self):
        self.data = []
        self.model.ClearItems()
        self.model.Cleared()
    
#     def AppendItem(self, parent, obj):
#         self.data.append(obj)
# 
#         if parent:
#             if parent.childs is None:
#                 parent.childs = []
#             parent.childs.append(obj)
#             obj.parent = parent
#             self.model.ItemAdded(self.model.ObjectToItem(parent), self.model.ObjectToItem(obj))
#         else:
#             obj.parent = None
#             self.model.root_nodes.append(obj)
#             self.model.ItemAdded(wx.dataview.NullDataViewItem, self.model.ObjectToItem(obj))
# 
#         if isinstance(obj, TreeContainerLazyItem) and obj.IsContainer():
#             # add a fake item to allow this item to appear with childs, it will be remove by lazy_load func
#             self.AppendItem(obj, TreeItem())
# 
#         return self.model.ObjectToItem(obj)
# 
#     def UpdateItem(self, obj):
#         self.model.ItemChanged(self.model.ObjectToItem(obj))
#             
#     def DeleteItem(self, parent, obj):
#         self.data.remove(obj)
#         if parent:
#             obj.parent = None
#             parent.childs.remove(obj)
#             self.model.ItemDeleted(self.model.ObjectToItem(parent), self.model.ObjectToItem(obj))
#         else:
#             obj.parent = None
#             self.model.root_nodes.remove(obj)
#             self.model.ItemDeleted(wx.dataview.NullDataViewItem, self.model.ObjectToItem(obj))
#             
#     def MoveItem(self, source_parent, dest_parent, obj):
#         self.DeleteItem(source_parent, obj)
#         return self.AppendItem(dest_parent, obj)
        
    def Expand(self, obj):
        item = self.model.ObjectToItem(obj)
        if item:
            self.tree_view.Expand(item)
    
    def ExpandAll(self):
        for obj in self.data:
            item = self.model.ObjectToItem(obj)
            if item:
                self.tree_view.Expand(item)

    def Collapse(self, obj):
        item = self.model.ObjectToItem(obj)
        if item:
            self.tree_view.Collapse(item)
    
    def CollapseAll(self):
        for obj in self.data:
            item = self.model.ObjectToItem(obj)
            if item:
                self.tree_view.Collapse(item)

    def Select(self, obj):
        item = self.model.ObjectToItem(obj)
        if item.IsOk():
            self.tree_view.Select(item)
#             self.tree_view.SetCurrentItem(item)
#             items = wx.dataview.DataViewItemArray()
#             items.append(item)
#            self.tree_view.UnselectAll()
#            self.tree_view.SelectAll()
        if obj is None:
            return
        parent = obj.parent
        while parent:
            self.tree_view.Expand(self.ObjectToItem(parent))
            parent = parent.parent
            
    def SelectItem(self, item):
        self.tree_view.Select(item)
        self.tree_view.SetCurrentItem(item)

    def Sort(self):
        self.model.Resort()


    def ItemToObject(self, item):
        return self.model.ItemToObject(item)
    
    def ObjectToItem(self, obj):
        return self.model.ObjectToItem(obj)


    def DropAccept(self, type, trigger):
        self.drop_targets.append({'type': type.__name__, 'trigger': trigger})



    def Append(self, parent, obj):
        if parent is None:
            self.model.AddChild(obj)
            self.model.ItemAdded(wx.dataview.NullDataViewItem, self.model.ObjectToItem(obj))
        else:
            parent.AddChild(obj)
            self.model.ItemAdded(self.model.ObjectToItem(parent), self.model.ObjectToItem(obj))

        if isinstance(obj, TreeContainerLazyItem) and obj.IsContainer():
            # add a dummy item to allow this item to appear with childs, it will be remove by lazy_load func
            self.Append(obj, TreeDummyItem())

        self.data.append(obj)
        if obj in self.data_state:
            self.data_state.remove(obj)
        
    def Remove(self, obj):
        if obj.parent is None:
            self.model.RemoveChild(obj)
            self.model.ItemDeleted(wx.dataview.NullDataViewItem, self.model.ObjectToItem(obj))
        else:
            parent = obj.parent
            obj.parent.RemoveChild(obj)
            self.model.ItemDeleted(self.model.ObjectToItem(parent), self.model.ObjectToItem(obj))

        self.data.remove(obj)
        if obj in self.data_state:
            self.data_state.remove(obj)
        
    def Update(self, obj):
        obj.Update()
        self.model.ItemChanged(self.model.ObjectToItem(obj))

        if obj in self.data_state:
            self.data_state.remove(obj)
        
    def Refresh(self):
        self.model.Cleared()
        
    def SaveState(self):
        """
        Backup objects state 
        """
        self.data_state = [ obj for obj in self.data ]
        
    def PurgeState(self, remove_empty_parent=True):
        """
        Remove from data every elements from state
        """

        # split list in container and non container elements
        non_container = []
        container = []
        for data in self.data_state:
            if isinstance(data, TreeContainerItem):
                container.append(data)
            else:
                non_container.append(data)
        
        # remove non container elements first to avoid removing parent before its childs
        while len(non_container)>0:
            obj = non_container.pop()
            self.Remove(obj)

        while len(container)>0:
            # only remove container with empty childs
            # implement pseudo recursively to remove childs first
            for obj in container:
                if obj.childs is None or len(obj.childs)==0:
                    self.Remove(obj)
                    container.remove(obj)

        self.data_state = []
            # remove parents if they are empty
#             if remove_empty_parent:
#                 while obj and ( isinstance(obj, TreeContainerItem) or isinstance(obj, TreeContainerLazyItem) ) and len(obj.childs)==0:
#                     try:
#                         self.DeleteItem(obj.parent, obj)
#                         self.data_state.remove(obj)
#                     except:
#                         pass
#                     obj = obj.parent

