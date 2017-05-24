# helper to maintain a state inside a tree

class ItemState:
    def __init__(self, selected=False, expanded=True):
        self.selected = selected
        self.expanded = expanded

class TreeState:
    def __init__(self, tree):
        self.tree = tree
        self.state = {}
    
    def update(self, item, selected=None, expanded=None):
        data = self.tree.GetItemData(item)
        if data:
            path = data.path
        else:
            path = None
        self.state[path] = ItemState(selected=self.tree.IsSelected(item), expanded=self.tree.IsExpanded(item))
        if not selected is None:
            self.state[path].selected = selected
        if not expanded is None:
            self.state[path].expanded = expanded
        print "state:", self.state[path].selected, self.state[path].expanded 

    def remove(self, path):
        self.state.pop(path)        

    def selected(self, path):
        if self.state.has_key(path):
            return self.state[path].selected
        else:
            return False
    
    def expanded(self, path):
        if self.state.has_key(path):
            return self.state[path].expanded
        else:
            return False
    
    def debug(self):
        print "State:"
        for state in self.state:
            print "    ", state, "selected:", self.state[state].selected, "expanded: ", self.state[state].expanded
