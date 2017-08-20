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
        return True

    def GetDragData(self):
        return None
    
    def SetValue(self, value, col):
        return False
    
class TreeContainerItem(TreeItem):
    def __init__(self):
        super(TreeContainerItem, self).__init__()
        self.childs = None
        
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
        item = manager.model.ObjectToItem(self.childs[0])
        manager.model.ItemDeleted(parent, item)
        # empty child list
        self.childs = []
        self.loaded = True
        return self.Load(manager)

    # override this for lazy loading childs
    def Load(self, manager):
        pass
    
    def IsContainer(self):
        return True

class TreeModel(wx.dataview.PyDataViewModel):
    def __init__(self):
        super(TreeModel, self).__init__()
        self.columns_type = []
        self.root_nodes = []
    
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
        
class TreeDropTarget(wx.TextDropTarget):
    def __init__(self, manager):
        super(TreeDropTarget, self).__init__()
        self.manager = manager

    #TODO: set drag cursor depending on accept/reject drop
    def OnDropText(self, x, y, text):
        payload = json.loads(text)
        for target in self.manager.drop_targets:
            if payload['type']==target['type']:
                return target['trigger'](x, y, payload['data'])
        return wx.DragError

class TreeDataObject(wx.TextDataObject):
    def __init__(self, data): 
        super(TreeDataObject, self).__init__()
        self.data = data
        self.SetText(json.dumps({'type': data.__class__.__name__, 'data': data.GetDragData()}))

class TreeManager(object):
    drag_item = None
    drag_source = None
    
    def __init__(self, tree_view):
        self.tree_view = tree_view

        self.model = TreeModel()
        self.tree_view.AssociateModel(self.model)

        # create drag and drop targets
        self.drop_targets = []
        self.tree_view.EnableDragSource(wx.DataFormat(wx.TextDataObject().GetFormat()))
        self.tree_view.EnableDropTarget(wx.DataFormat(wx.DF_TEXT))
        self.tree_view.SetDropTarget(TreeDropTarget(self))

        # data elements
        self.data = []
        
        self.OnColumnHeaderClick = None
        self.OnColumnHeaderRightClick = None
        self.OnColumnReordered = None
        self.OnColumnSorted = None
        self.OnItemActivated = None
        self.OnItemBeginDrag = None
        self.OnItemCollapsed = None
        self.OnItemCollapsing = None
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
        
        TreeManager.drag_item = event.GetItem()
        TreeManager.drag_source = self
        
        if self.drag_item is None:
            event.Skip()
            return wx.DragCancel
        
        drag_data = self.model.ItemToObject(event.GetItem())
        if drag_data.GetDragData() is None:
            event.Skip()
            return wx.DragCancel

        event.SetDataObject(TreeDataObject(drag_data))
        
        if self.OnItemBeginDrag:
            return self.OnItemBeginDrag(event)
    
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
        if self.OnItemContextMenu:
            return self.OnItemContextMenu(event)
        event.Skip()
    
    def _onItemDrop( self, event ):
        event.manager = self
        if self.OnItemDrop:
            return self.OnItemDrop(event)
        event.Skip()
    
    def _onItemDropPossible( self, event ):
        event.manager = self
        if self.OnItemDropPossible:
            return self.OnItemDropPossible(event)
        event.Skip()
    
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
        column.Sortable = True
        column.Reorderable = True
    
    def AddFloatColumn(self, title):
        column = self.tree_view.AppendTextColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type.append('float')
        column.Sortable = True
        column.Reorderable = True

    def AddIntegerColumn(self, title):
        column = self.tree_view.AppendTextColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE)
        self.model.columns_type.append('integer')
        column.Sortable = True
        column.Reorderable = True

    def AddToggleColumn(self, title):
        column = self.tree_view.AppendToggleColumn(title, len(self.model.columns_type), width=wx.COL_WIDTH_AUTOSIZE, mode=wx.dataview.DATAVIEW_CELL_ACTIVATABLE)
        self.model.columns_type.append('integer')
        column.Sortable = True
        column.Reorderable = True
        
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
            print "select", item
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
