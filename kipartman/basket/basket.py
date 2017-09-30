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

class WishPart(object):
    def __init__(self, distributor, sku, quantity, unit_price):
        self.distributor = distributor
        self.sku = sku
        self.quantity = quantity
        self.unit_price = unit_price
        
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
        with open(filename, 'w') as outfile:
            outfile.write("-- Bom files --\n")
            outfile.write("filename;quantity\n")
            for bom in self.boms:
                outfile.write(self.boms[bom].bom.filename+";"+str(self.boms[bom].quantity)+"\n")
            
            for distributor in self.distributors:
                outfile.write("\n-- "+distributor+" --\n")
                outfile.write("sku;quantity;unit-price\n")
                for wish in self.distributors[distributor]:
                    outfile.write(wish.sku+";"+str(wish.quantity)+";"+str(wish.unit_price[0])+"\n")
        self.filename = filename
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
    
    
    def ClearWishes(self):
        self.distributors.clear()
        
    def AddWish(self, distributor, sku, quantity, unit_price):
        if self.distributors.has_key(distributor.name)==False:
            self.distributors[distributor.name] = []
        self.distributors[distributor.name].append(WishPart(distributor, sku, quantity, unit_price))
    
    def RemoveWish(self, distributor, sku):
        if self.distributors.has_key(distributor.name)==False:
            return 
        for wish in self.distributors[distributor.name]:
            if wish.sku==sku:
                self.distributors[distributor.name].pop(wish)
                return 
