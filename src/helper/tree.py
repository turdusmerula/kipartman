

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
