from dialogs.panel_parts import PanelParts
from api.queries import PartCategoriesQuery
from api.models import PartCategory

from rest_client import fields
from rest_client import models
from rest_client import registry

import wrapt

class PartsFrame(PanelParts): 
    def __init__(self, parent): 
        PanelParts.__init__(self, parent)

    def _loadCategories(self):
        i1 = fields.IntField(default=10)
        print "i1: ", i1
        
        print "registry: ", registry.registry
        
        cat = PartCategory(name="toto", parent=None, id=1, path="http://localhost:8100/parts/1")
        cat2 = PartCategory(name="tata", parent=cat, id=2, path="http://localhost:8100/parts/2")
        cat3 = PartCategory(name="tutu", parent="http://localhost:8100/api/parts/categories/4", id=2, path="http://localhost:8100/parts/2")
#        cat3 = PartCategory(name="tata", parent="http://localhost:8100/api/parts/categories/4", id=3, path="http://localhost:8100/api/parts/categories/3")

        print "---"
        cat.id = 100
        cat2.id = 200
        cat3.id = 300
        print "---"
        
        print "cat: ", cat.id, cat.path, cat.name
        print "cat2: ", cat2.id, cat2.path, cat2.name, cat2.parent.name
        print "cat3: ", cat3.id, cat3.path, cat3.name, cat3.parent.name
#        print "cat2: ", cat2.id, cat2.path, cat2.name, cat2.parent.path
#        print "cat3: ", cat3.id, cat3.path, cat3.name, cat3.parent.path
        # get all categories
        categories = PartCategoriesQuery().get()
        for category in categories:
            print "Category: ", type(category), category.name
            print category.parent.name, category.parent.path

    def _loadParts(self):
        None

    # Virtual event handlers, overide them in your derived class
    def load(self): 
        self._loadCategories()
        self._loadParts()

