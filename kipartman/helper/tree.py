import logging
import datetime
import platform
import wx.dataview
#import wx.dataview.DataViewTreeCtrl
import json
from array import array

class Tree:
    def __init__(self, tree):
        self.tree = tree 
        
    def sort(self, root=None):
        to_sort = []
        if root is None:
            to_sort.append(self.tree.GetRootItem())
        else:
            to_sort.append(root)
        
        for item in to_sort:
            if self.tree.ItemHasChildren(item):
                self.tree.SortChildren(item)
            child, cookie = self.tree.GetFirstChild(item)
            if child and self.tree.ItemHasChildren(child):
                to_sort.append(child)
            while child.IsOk():
                if self.tree.ItemHasChildren(child):
                    to_sort.append(child)
                child, cookie = self.tree.GetNextChild(item, cookie)


class TreeItem(object):
    def __init__(self):
        self.parent = None
        
    def GetValue(self, col):
        return ''
    
    def GetAttr(self, col, attr):
        return False

    def GetParent(self):
        return self.parent

    def IsContainer(self):
        return False

    def HasContainerColumns(self):
        return False

    def GetDragData(self):
        return None
    
    def SetValue(self, value, col):
        return False
    
#    def Compare(self, item):
#        return 0
    
class TreeContainerItem(TreeItem):
    def __init__(self):
        super(TreeContainerItem, self).__init__()
        self.childs = None
        
    def HasContainerColumns(self):
        return True

    def IsContainer(self):
        return True

class TreeContainerLazyItem(TreeItem):
    def __init__(self):
        super(TreeContainerLazyItem, self).__init__()
        self.childs = []
        self.loaded = False
    
    def lazy_load(self, manager):
        if self.loaded:
            return
        # remove dummy item
        parent = manager.model.ObjectToItem(self)
        #TODO: WorkAround: Part Expander expansion with no children
        if len(self.childs)>0 :
            item = manager.model.ObjectToItem(self.childs[0])
            manager.model.ItemDeleted(parent, item)
        # empty child list
        self.childs = []
        self.loaded = True
        return self.Load(manager)

    # override this for lazy loading childs
    def Load(self, manager):
        pass

    def HasContainerColumns(self):
        return True

    def IsContainer(self):
        return True

class TreeModel(wx.dataview.PyDataViewModel):
    def __init__(self):
        super(TreeModel, self).__init__()
        self.columns_type = []
        self.root_nodes = []
        self.sort_function = []

    def ClearItems(self):
        self.root_nodes = []
        
    def GetColumnCount(self):
        return len(self.columns_type)

    def GetColumnType(self, col):
        return self.columns_type[col]

    def GetChildren(self, item, children):
        if not item:
            for node in self.root_nodes:
                children.append(self.ObjectToItem(node))
            return len(self.root_nodes)
        obj = self.ItemToObject(item)
        if obj is None or obj.childs is None:
            return 0
        for node in obj.childs:
            children.append(self.ObjectToItem(node))
        return len(obj.childs)
    
    def IsContainer(self, item):
        if not item:
            return True
        obj = self.ItemToObject(item)
        if obj:
            return obj.IsContainer()
        return False
        
    def HasContainerColumns(self, item):
        if not item:
            return False
        obj = self.ItemToObject(item)
        return obj.HasContainerColumns()

    def GetParent(self, item):
        if not item:
            return wx.dataview.NullDataViewItem
        obj = self.ItemToObject(item)
        if obj is None:
            return wx.dataview.NullDataViewItem
        if obj.GetParent():
            return self.ObjectToItem(obj.GetParent())
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        if not item or item.IsOk()==False:
            return ""
        obj = self.ItemToObject(item)
        value = obj.GetValue(col)
        if value is None:
            return ""
        return value

    def GetAttr(self, item, col, attr):
        obj = self.ItemToObject(item)
        return obj.GetAttr(col, attr)

    def SetValue(self, value, item, col):
        obj = self.ItemToObject(item)
        res = obj.SetValue(value, col)
        self.ItemChanged(item)
        return res
        
    def Compare(self, item1, item2, column, ascending):
        if self.sort_function[column] is None:
            return 0
        else:
            value1 = self.GetValue(item1, column)
            value2 = self.GetValue(item2, column)

            # empty element are always treated inferior
            if value1=="" and value2!="":
                return 1
            elif value1!="" and value2=="":
                return -1
            elif value1=="" and value2=="":
                return super(TreeModel, self).Compare(item1, item2, column, ascending)

            if not ascending: # swap sort order?
                value2, value1 = value1, value2

            return self.sort_function[column](value1, value2)
        
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

def CompareInteger(item1, item2):
    val1 = int(item1)
    val2 = int(item2)
    if val2>val1:
        return -1
    elif val2<val1:
        return 1
    return 0

def CompareFloat(item1, item2):
    val1 = float(item1)
    val2 = float(item2)
    if val2>val1:
        return -1
    elif val2<val1:
        return 1
    return 0

def CompareString(item1, item2):
    if item2>item1:
        return -1
    elif item2<item1:
        return 1
    return 0 

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

        self.context_menu = context_menu
        
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
            pos = event.GetPosition()
            self.tree_view.PopupMenu(self.context_menu, pos)
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
        obj = self.model.ItemToObject(item)
        if isinstance(obj, TreeContainerLazyItem):
            obj.lazy_load(self)
        
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
        self.model.columns_type.append('string')
        self.model.sort_function.append(CompareString)
        column.Sortable = True
        column.Reorderable = True
        column.SortOrder = True
        return column
    
    def AddFloatColumn(self, title):
        column = self.tree_view.AppendTextColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type.append('float')
        self.model.sort_function.append(CompareFloat)
        column.Sortable = True
        column.Reorderable = True
        return column

    def AddIntegerColumn(self, title):
        column = self.tree_view.AppendTextColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type.append('integer')
        self.model.sort_function.append(CompareInteger)
        column.Sortable = True
        column.Reorderable = True
        return column

    def AddToggleColumn(self, title):
        column = self.tree_view.AppendToggleColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE, mode=wx.dataview.DATAVIEW_CELL_ACTIVATABLE)
        self.model.columns_type.append('integer')
        self.model.sort_function.append(CompareString)
        column.Sortable = True
        column.Reorderable = True
        return column

    def AddCustomColumn(self, title, type, sort_function):
        column = self.tree_view.AppendTextColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type.append(type)
        self.model.sort_function.append(sort_function)
        column.Sortable = True
        column.Reorderable = True
        return column

    def AddBitmapColumn(self, title):
        column = self.tree_view.AppendBitmapColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type.append('bitmap')
        # TODO: add support for sorting bitmaps by labels
        self.model.sort_function.append(None)
        column.Sortable = True
        column.Reorderable = True
        return column
        
    def RemoveColumn(self, index):
        for column in self.tree_view.GetColumns():
            if column.GetModelColumn()==index:
                self.tree_view.DeleteColumn(column)
                return
        
    def ClearItems(self):
        self.data = []
        self.model.ClearItems()
        self.model.Cleared()
    
    def AppendItem(self, parent, obj):
        self.data.append(obj)
#        self.tree_view.AssociateModel(None)
        if parent:
            if parent.childs is None:
                parent.childs = []
            parent.childs.append(obj)
            obj.parent = parent
            self.model.ItemAdded(self.model.ObjectToItem(parent), self.model.ObjectToItem(obj))
        else:
            obj.parent = None
            self.model.root_nodes.append(obj)
            self.model.ItemAdded(wx.dataview.NullDataViewItem, self.model.ObjectToItem(obj))
        return self.model.ObjectToItem(obj)

    def UpdateItem(self, obj):
        self.model.ItemChanged(self.model.ObjectToItem(obj))
            
    def DeleteItem(self, parent, obj):
        self.data.remove(obj)
        if parent:
            obj.parent = None
            parent.childs.remove(obj)
            self.model.ItemDeleted(self.model.ObjectToItem(parent), self.model.ObjectToItem(obj))
        else:
            obj.parent = None
            self.model.root_nodes.remove(obj)
            self.model.ItemDeleted(wx.dataview.NullDataViewItem, self.model.ObjectToItem(obj))
            
    def MoveItem(self, source_parent, dest_parent, obj):
        self.DeleteItem(source_parent, obj)
        return self.AppendItem(dest_parent, obj)
        
    def Expand(self, obj):
        item = self.model.ObjectToItem(obj)
        if item:
            self.tree_view.Expand(item)
    
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


    def SaveState(self):
        """
        Backup objects state 
        """
        self.data_state = []
        for obj in self.data:
            self.data_state.append(obj)
    
    def DropStateObject(self, obj):
        if self.data_state.count(obj)>0:
            self.data_state.remove(obj)
            self.UpdateItem(obj)
            return True
        return False
    
    def PurgeState(self, remove_empty_parent=True):
        """
        Remove from data every elements from state
        """

        # split list in container and non container elements
        non_container = []
        container = []
        for data in self.data_state:
            if isinstance(data, TreeContainerItem) or isinstance(data, TreeContainerLazyItem):
                container.append(data)
            else:
                non_container.append(data)
        
        # remove non container elements first to avoid removing parent before its childs
        while len(non_container)>0:
            obj = non_container[0]
            self.DeleteItem(obj.parent, obj)
            non_container.remove(obj)

        while len(container)>0:
            # only remove container with empty childs
            for obj in container:
                if obj.childs is None or len(obj.childs)==0:
                    break
            if obj.childs and len(obj.childs)>0:
                break # this is an error, we should never get there
            self.DeleteItem(obj.parent, obj)
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
