import json
import os
import wx
import rest
from bom.bom import Bom

class BasketException(BaseException):
    def __init__(self, error):
        self.error = error

class BomQuantity(object):
    def __init__(self, bom, quantity):
        self.bom = bom
        self.quantity = quantity

class Basket(object):
    def __init__(self):
        self.filename = None
        self.saved = True
        self.boms = {}
        self.distributors = {}


    def LoadFile(self, filename):
        print "Load Basket", filename
        self.saved = True
    
    def SaveFile(self, filename):
        print "Save Basket", filename
        self.saved = True

    def Save(self):
        if self.filename:
            self.SaveFile(self.filename)
            return True
        else:
            return False


    def HasBom(self, bom_file):
        return self.boms.has_key(bom_file)
    
    def AddBom(self, bom_file, quantity):
        if self.boms.has_key(bom_file)==False:
            bom = Bom()
            bom.LoadFile(bom_file)
            self.boms[bom_file] = BomQuantity(bom, 1)
        else:
            self.boms[bom_file].quantity = self.boms[bom_file].quantity+quantity
        return self.boms[bom_file]
    
    def RemoveBom(self, bom_file):
        if self.boms.has_key(bom_file):
            self.boms.pop(bom_file)
    
    def SetBomQuantity(self, bom_file, quantity):
        if self.boms.has_key(bom_file)==False:
            self.boms[bom_file][0] = 1
        else:
            self.boms[bom_file][0] = quantity

