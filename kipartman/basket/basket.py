import json
import os
import wx
from bom.bom import Bom
from helper.log import log

class BasketException(BaseException):
    def __init__(self, error):
        self.error = error

class BomQuantity(object):
    def __init__(self, path, quantity):
        self.path = path
        self.quantity = quantity
        self.bom = None
    
    def load(self):    
        self.bom = Bom()
        self.bom.LoadFile(self.path)

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
        log.info("Load Basket", filename)
        
        if(os.path.isfile(filename)==False):
            raise Exception("Error: %s does not exists" % filename)
        
        with open(filename, 'r', encoding='utf-8') as infile:
            content = json.load(infile)

        for bom in content['boms']:
            self.boms[bom['path']] = BomQuantity(bom['path'], int(bom['quantity']))
            
        # TODO: show error messages from part_not_found, module_not_found and part_id_not_found
        self.filename = filename
        self.saved = True
                
    def SaveFile(self, filename):
        log.info("Save Basket", filename)
        
        with open(filename, 'w', encoding='utf-8') as outfile:
            boms = []
            for bom in self.boms:
                boms.append({'path': bom, 'quantity': self.boms[bom].quantity})
            
            json.dump({ 'boms': boms}, outfile, sort_keys=True,
                  indent=4, separators=(',', ': '))

        self.filename = filename
        self.saved = True

    def Save(self):
        if self.filename:
            self.SaveFile(self.filename)
            return True
        else:
            return False


    def HasBom(self, bom_file):
        return bom_file in self.boms
    
    def AddBom(self, bom_file, quantity):
        if bom_file not in self.boms:
            self.boms[bom_file] = BomQuantity(bom_file, 1)
        else:
            self.boms[bom_file].quantity = self.boms[bom_file].quantity+quantity
        return self.boms[bom_file]
    
    def RemoveBom(self, bom_file):
        if bom_file in self.boms:
            self.boms.pop(bom_file)
    
    def SetBomQuantity(self, bom_file, quantity):
        if bom_file not in self.boms:
            self.boms[bom_file] = BomQuantity(bom_file, 1)
        else:
            self.boms[bom_file].quantity = quantity
    
    
    def ClearWishes(self):
        self.distributors.clear()
        
    def AddWish(self, distributor, sku, quantity, unit_price):
        if distributor.name not in self.distributors:
            self.distributors[distributor.name] = []
        self.distributors[distributor.name].append(WishPart(distributor, sku, quantity, unit_price))
    
    def RemoveWish(self, distributor, sku):
        if distributor.name not in self.distributors:
            return 
        for wish in self.distributors[distributor.name]:
            if wish.sku==sku:
                self.distributors[distributor.name].pop(wish)
                return 
