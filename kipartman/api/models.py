# -*- coding: utf-8 -*-
from rest_client import fields
from rest_client import models

class PartCategory(models.Model):
    id = fields.IntegerField(read_only=True, default=-1)
    path = fields.TextField(read_only=True)
    name = fields.TextField()
    parent = fields.HyperlinkField('PartCategory')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Part(models.Model):
    id = fields.IntegerField(read_only=True, default=-1)
    path = fields.TextField(read_only=True)
    name = fields.TextField()
    description = fields.TextField()
    category = fields.HyperlinkField('PartCategory')
    footprint = fields.HyperlinkField('Footprint')
    comment = fields.TextField()
    parts = fields.IndexListField(model='Part')
    parameters = fields.ListField(model='PartParameter', read_only=True)
    distributors = fields.ListField(model='PartDistributor', read_only=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class FootprintCategory(models.Model):
    id = fields.IntegerField(read_only=True, default=-1)
    path = fields.TextField(read_only=True)
    parent = fields.HyperlinkField('FootprintCategory')
    name = fields.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Footprint(models.Model):
    id = fields.IntegerField(read_only=True, default=-1)
    path = fields.TextField(read_only=True)
    category = fields.HyperlinkField('FootprintCategory')
    name = fields.TextField()
    description = fields.TextField()
    comment = fields.TextField()
    def __unicode__(self): 
        return '%d: %s' % (self.id, self.name)

class Unit(models.Model):
    id = fields.IntegerField(read_only=True, default=-1)
    path = fields.TextField(read_only=True)
    name = fields.TextField()
    symbol = fields.TextField(default='')

class UnitPrefix(models.Model):
    id = fields.IntegerField(read_only=True, default=-1)
    path = fields.TextField(read_only=True)
    name = fields.TextField()
    # suffix name
    symbol = fields.TextField()
    # value contains the exponent part
    power = fields.TextField()

class PartParameter(models.Model):
    id = fields.IntegerField(read_only=True, default=-1)
    path = fields.TextField(read_only=True)
    part = fields.HyperlinkField('Part')
    name = fields.TextField()
    description = fields.TextField()
    unit = fields.HyperlinkField('Unit', null=True)
    numeric = fields.BooleanField()
    text_value = fields.TextField(null=True)
    min_value = fields.FloatField(null=True)
    min_prefix = fields.HyperlinkField('UnitPrefix', null=True)
    nom_value = fields.FloatField(null=True)
    nom_prefix = fields.HyperlinkField('UnitPrefix', null=True)
    max_value = fields.FloatField(null=True)
    max_prefix = fields.HyperlinkField('UnitPrefix', null=True)

    def _value_string(self, value, prefix, unit):
        res = ""
        if value is None:
            return res
        res = res+"%g"%value+" "
        if not prefix is None:
            res = res+prefix.symbol
        if not unit is None:
            res = res+unit.symbol
        return res

    def min_string(self):
        return self._value_string(self.min_value, self.min_prefix, self.unit)
    def nom_string(self):
        return self._value_string(self.nom_value, self.nom_prefix, self.unit)
    def max_string(self):
        return self._value_string(self.max_value, self.max_prefix, self.unit)

    def unit_string(self):
        if self.unit is None:
            return ""
        return self.unit.name

class PartDistributor(models.Model):
    id = fields.IntegerField(read_only=True, default=-1)
    path = fields.TextField(read_only=True)
    part = fields.HyperlinkField('Part')
    distributor = fields.HyperlinkField('Distributor')
    packaging_unit = fields.IntegerField()
    unit_price = fields.FloatField()
    currency = fields.TextField()
    sku = fields.TextField()
    def item_price(self):
        return self.unit_price*self.packaging_unit

class Distributor(models.Model):
    id = fields.IntegerField(read_only=True, default=-1)
    path = fields.TextField(read_only=True)
    name = fields.TextField()
    address = fields.TextField()
    website = fields.TextField()
    sku_url = fields.TextField()
    email = fields.TextField()
    phone = fields.TextField()
    comment = fields.TextField()
    