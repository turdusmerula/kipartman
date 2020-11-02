# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import copy
from django.utils.translation import gettext_lazy as _
import helper.django
from enum import Enum


class PartValueField(models.TextField):
    description = _("Value field for parts")

    def get_internal_type(self):
        return "TextField"

    def to_python(self, value):
        return value
    
#     def pre_save(self, model_instance, add):
#         value = "{"+f"'pattern': '{model_instance.value}', 'value': '{value}'+
#         print("---", model_instance.value, add)
#         setattr(model_instance, self.attname, value)
#         return value


class PartCategory(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)
    
    @property
    def path(self):
        res = self.name
        parent = self.parent
        while parent:
            res = parent.name+"/"+res
            parent = parent.parent
        return "/"+res
    
    class MPTTMeta:
        order_insertion_by = ['name']
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Part(models.Model):
    def __init__(self, *args, **kwargs):
        self.child_count = 0
        super(Part, self).__init__(*args, **kwargs)
        
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    comment = models.TextField(blank=True, default='')
    category = models.ForeignKey('PartCategory', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    footprint = models.ForeignKey('KicadFootprint', related_name='new_footprint', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    symbol = models.ForeignKey('KicadSymbol', related_name='symbol', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    childs = models.ManyToManyField('Part', blank=True)
    #parameters is defined inside PartParameter by ForeignKey part
    #offers is defined inside PartOffer by ForeignKey part
    #manufacturers is defined inside PartManufacturer by ForeignKey part
    #storages is defined inside PartStorage by ForeignKey part
    #attachements: is defined inside PartAttachement by ForeignKey part
    #references: is defined inside PartReference by ForeignKey part
    value = PartValueField(blank=True, default="{name}")
    metapart = models.BooleanField(null=False, default=False)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class PartReference(models.Model):
    part = models.ForeignKey('Part', related_name='references', null=False, blank=False, default=None, on_delete=models.CASCADE)
    type = models.TextField(null=False, blank=False)
    manufacturer = models.TextField(null=False, blank=True, default="")
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=True, default="")
    uid = models.TextField(null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%d: %s' % (self.id, self.type, self.name, self.uid)
    
class PartParameter(models.Model):
    part = models.ForeignKey('Part', related_name='parameters', null=False, blank=False, default=None, on_delete=models.CASCADE)
    parameter = models.ForeignKey('Parameter', related_name='parameter', on_delete=models.DO_NOTHING, null=False, blank=False)
    text_value = models.TextField(null=True, blank=True)
    value = models.FloatField(null=True)
    prefix = models.ForeignKey('UnitPrefix', related_name='min', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    metaparameter = models.BooleanField(null=False, default=False)
    operator = models.TextField(null=True, default=None)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.id:
            return '%d: %s' % (self.id, self.name)
        else:
            return '<None>: %s' % (self.name)
            


class PartManufacturer(models.Model):
    part = models.ForeignKey('Part', related_name='manufacturers', null=False, blank=False, default=None, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.DO_NOTHING, null=False)
    part_name = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class PartOffer(models.Model):
    part = models.ForeignKey('Part', related_name='offers', null=False, blank=False, default=None, on_delete=models.CASCADE)
    distributor = models.ForeignKey('Distributor', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    packaging_unit = models.IntegerField(default=1)
    min_order_quantity = models.IntegerField(default=1)
    quantity = models.IntegerField()
    available_stock = models.IntegerField(null=True, blank=True, default=None)
    unit_price = models.FloatField()
    packaging = models.TextField(blank=True)
    currency = models.TextField(blank=True)
    sku = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    

class PartStorage(models.Model):
    part = models.ForeignKey('Part', related_name='storages', null=False, blank=False, default=None, on_delete=models.CASCADE)
    storage = models.ForeignKey('Storage', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    quantity = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class PartAttachement(models.Model):
    part = models.ForeignKey('Part', related_name='attachements', null=False, blank=False, default=None, on_delete=models.CASCADE)
    file = models.ForeignKey('File', on_delete=models.DO_NOTHING, null=False)
    description = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %d %s' % (self.part.pk, self.file.pk, self.description)

class ParameterType():
    INTEGER = "integer"
    FLOAT = "float"
    TEXT = "text"
    
class Parameter(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    unit = models.ForeignKey('Unit', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    value_type = models.TextField()
    #alias is defined inside ParameterAlias by ForeignKey parameter
    updated = models.DateTimeField(auto_now=True)

class ParameterAlias(models.Model):
    parameter = models.ForeignKey('Parameter', related_name='alias', null=False, blank=False, default=None, on_delete=models.CASCADE)
    name = models.TextField(null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    
class Manufacturer(models.Model):
    name = models.TextField(blank=False)
    address = models.TextField(null=True, blank=True, default='')
    website = models.TextField(null=True, blank=True, default='')
    email = models.TextField(null=True, blank=True, default='')
    phone = models.TextField(null=True, blank=True, default='')
    comment = models.TextField(null=True, blank=True, default='')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Distributor(models.Model):
    name = models.TextField(blank=False)
    address = models.TextField(null=True, blank=True, default='')
    website = models.TextField(null=True, blank=True, default='')
    sku_url = models.TextField(null=True, blank=True, default='')
    email = models.TextField(null=True, blank=True, default='')
    phone = models.TextField(null=True, blank=True, default='')
    comment = models.TextField(null=True, blank=True, default='')
    allowed = models.BooleanField(null=False, default=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class KicadSymbolLibrary(models.Model):
    path = models.TextField(blank=True, default='')
    #symbols is defined inside PartParameter by ForeignKey part
    mtime_lib = models.FloatField()
    mtime_dcm = models.FloatField()
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class KicadSymbol(models.Model):
    library = models.ForeignKey('KicadSymbolLibrary', related_name='symbols', null=False, blank=False, default=None, on_delete=models.CASCADE)
    name = models.TextField()
    content = models.TextField()
    metadata = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class KicadFootprintLibrary(models.Model):
    path = models.TextField(blank=True, default='')
    #footprints is defined inside PartParameter by ForeignKey part
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class KicadFootprint(models.Model):
    library = models.ForeignKey('KicadFootprintLibrary', related_name='footprints', null=False, blank=False, default=None, on_delete=models.CASCADE)
    name = models.TextField()
    content = models.TextField()
    mtime = models.FloatField()
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class File(models.Model):
    source_name = models.TextField()
    storage_path = models.TextField()
    created = models.DateTimeField(null=True, blank=True, default=None)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s, %s' % (self.id, self.source_name, self.storage_path)


class VersionedFileState(object):
    created = 0
    modified = 1
    deleted = 2
    
class VersionedFile(models.Model):
    source_path = models.TextField()
    storage_path = models.TextField(default='')
    md5 = models.TextField(null=False, blank=True, default='')
    version = models.IntegerField(default=0)
    state = models.IntegerField(default=0)
    metadata = models.TextField(null=True, blank=True, default='')
    category = models.TextField(null=True, blank=True, default='')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.source_path)
    
class VersionedFileHistory(models.Model):
    file = models.ForeignKey('VersionedFile', null=False, blank=False, default=None, on_delete=models.CASCADE)
    source_path = models.TextField()
    storage_path = models.TextField(default='')
    md5 = models.TextField(null=False, blank=True, default='')
    version = models.IntegerField(default=0)
    state = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    operation = models.TextField()


class Unit(models.Model):
    name = models.TextField()
    symbol = models.TextField(default='')
    prefixable = models.BooleanField(default=True)        
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class UnitPrefix(models.Model):
    name = models.TextField()
    # suffix name
    symbol = models.TextField()
    # value contains the exponent part
    power = models.TextField()
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class StorageCategory(MPTTModel):
    parent = TreeForeignKey('StorageCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Storage(models.Model):
    category = models.ForeignKey('StorageCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    comment = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)

class PartStorageHistory(models.Model):
    part = models.ForeignKey('Part', null=False, blank=False, default=None, on_delete=models.CASCADE)
    location = models.ForeignKey('Storage', null=False, blank=False, default=None, on_delete=models.CASCADE)
    reason = models.TextField(blank=False)
    amount = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)

class Currency(models.Model):
    name = models.TextField()
    symbol = models.TextField(default='')
    base = models.TextField(default='EUR')
    ratio = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    