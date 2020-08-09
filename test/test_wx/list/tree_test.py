import wx
from list1 import Frame1
import sys
import os
import wx.lib.newevent
from six.moves import _thread

# add plugin to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../kipartman')))
print(sys.path)
from helper.tree import TreeModel, TreeManager, TreeContainerItem

data = []

# class DataTreeViewListModel(wx.dataview.DataViewListModel):
#     def __init__(self, data):
#         super(DataTreeViewListModel, self).__init__()
#         self.data = data 
#     
#         
#     def GetCount(self):
#         print("----")
#         return len(self.data)
# 
#     def GetValueByRow(self, row, col):
#         item = self.data[row]
#         print("___")
#         if col==0:
#             return str(item['id'])
#         elif col==1:
#             return item['name']
#         elif col==2:
#             return item['description']
#     
#     def GetColumnCount(self):
#         print("$$$")
#         return 3
#     
#     def GetColumnType(self, col):
#         print("===", col)
#         return "str"
#     
#     def GetChildren(self, item, children):
#         print("---", item, children)
#         return len(children)
#     
#     def GetRow(self, item):
#         print("***")
#         return 0

class DataModelTest(TreeContainerItem):
    def __init__(self, item):
        super(DataModelTest, self).__init__()
        self.item = item
        
    def GetValue(self, col):
        if col==0:
            return str(self.item['id'])
        elif col==1:
            return self.item['name']
        elif col==2:
            return self.item['description']

    def HasContainerColumns(self):
        return False

    def GetAttr(self, col, attr):
        return False

class TreeModelTest(TreeModel):
    def __init__(self):
        super(TreeModelTest, self).__init__()
        self.columns = {}

class TreeManagerTest(TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        model = TreeModelTest()
        super(TreeManagerTest, self).__init__(tree_view, model, *args, **kwargs)

    def FindTestItem(self, id):
        for data in self.data:
            if isinstance(data, DataModelTest) and data.item.id==id:
                return data
        return None

    def AppendTestItem(self, parent_item, item):
        parentobj = None
        if parent_item is not None:
            parentobj = self.FindTestItem(parent_item.id)
            
        itemobj = DataModelTest(item)
        self.AppendItem(parentobj, itemobj)
        self.Expand(parentobj)
        return itemobj


# This creates a new Event class and a EVT binder function
(AddItemEvent, EVT_ADD_ITEM) = wx.lib.newevent.NewEvent()
class LoadThread:
    def __init__(self, win, tree_manager, data):
        self.win = win
        self.tree_manager = tree_manager
        self.data = data

    def Start(self):
        self.keepGoing = True
        self.running = True
        _thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.keepGoing = False

    def IsRunning(self):
        return self.running

    def Run(self):
        for item in self.data:
            if self.keepGoing==False:
                break

            evt = AddItemEvent(item=item)
            wx.QueueEvent(self.win, evt)
            
        print("loaded")
        self.running = False

class NewFrame1 ( Frame1 ):
    def __init__(self, parent): 
        super(NewFrame1, self).__init__(parent)

        # create list
        self.tree_test_manager = TreeManagerTest(self.tree_test)
        self.tree_test_manager.AddIntegerColumn("id")
        self.tree_test_manager.AddTextColumn("name")
        self.tree_test_manager.AddTextColumn("description")

        self.Bind(EVT_ADD_ITEM, self.OnAddItem)

        global data
        ld = LoadThread(self, self.tree_test_manager, data)
        ld.Start()
        
    def OnAddItem(self, event):
        self.tree_test_manager.AppendTestItem(None, event.item)
        print(event.item['id'])
        
def main(args=None):
    global data
    
    for i in range(0, 1000):
        data.append({'id': i, 'name': f"name {i}", 'description': f"description {i}"})
    print(len(data))
    app = wx.App()
    
    f = NewFrame1(None)    
    f.Show()

    app.MainLoop() 

if __name__ == "__main__":
    main()

