import json
import os
import wx
import rest

class BasketException(BaseException):
    def __init__(self, error):
        self.error = error
        
class Basket(object):
    def __init__(self, pcb):
        self.filename = None
        self.saved = True

    def LoadFile(self, filename):
        print "Load Basket", filename
        self.saved = True
    
    def SaveFile(self, filename):
        print "Save Basket", filename
        self.saved = True

    def Save(self):
        self.SaveFile(self.filename)
