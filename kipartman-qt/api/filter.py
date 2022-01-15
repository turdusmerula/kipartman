from PyQt6.QtCore import QObject
from PyQt6.QtCore import QEvent, pyqtSignal


class Filter(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def Apply(self, context):
        return context
    
    def __str__(self):
        return f"{self.name}: {self.description}"

class FilterGroup(QObject):
    filterChanged = pyqtSignal()

    def __init__(self, name, description):
        super(FilterGroup, self).__init__()
        self.name = name
        self.description = description
        self.filters = []

    def Append(self, filter):
        self.filters.append(filter)
        self.filterChanged.emit()
    
    def Remove(self, filter):
        self.filters.remove(filter)
        self.filterChanged.emit()
    
    def Clear(self):
        self.filters.clear()
        self.filterChanged.emit()

    def IsEmpty(self):
        return len(self.filters)==0

    def Apply(self, context, filter=Filter):
        for f in self.filters:
            if isinstance(f, filter):
                context = f.Apply(context)
        return context

class FilterSet(QObject):
    filterChanged = pyqtSignal()
    
    def __init__(self):
        super(FilterSet, self).__init__()
        self.groups = []

    def Append(self, group):
        self.groups.append(group)
        group.filterChanged.connect(self.groupFilterChanged)
        self.filterChanged.emit()

    def Remove(self, group):
        group.filterChanged.disconnect()
        self.groups.remove(group)
        self.filterChanged.emit()
        
    def Clear(self):
        for group in self.groups:
            group.filterChanged.disconnect()
        self.groups.clear()

    def groupFilterChanged(self):
        self.filterChanged.emit()

    def Apply(self, context, filter=Filter):
        for group in self.groups:
            context = group.Apply(context, filter)
        return context


class FilterRequest(Filter):
    """ Base class for filters that applies on django requests """
    
    def __init__(self, name, description):
        super(FilterRequest, self).__init__(name, description)
