# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from helper.class_tool import add_method, overload_method
import copy

import django.db.models.manager

@add_method(django.db.models.manager.BaseManager)
def add_pending(self, el):
    instance = self.instance
    field = self.field.remote_field
    if field.one_to_many:
        if hasattr(instance, "_add_pendings_")==False:
            setattr(instance, "_add_pendings_", {})
        add_pendings = getattr(instance, "_add_pendings_")
        if field.name not in add_pendings:
            add_pendings[field.name] = []
    else:
        raise f"{field.name}: add_pending only implemented for one_to_many relation "
    
    if hasattr(el, "_remove_pending_"):
        delattr(el, "_remove_pending_")
        
    add_pendings[field.name].append(el)

@add_method(django.db.models.manager.BaseManager)
def remove_pending(self, el):
    instance = self.instance
    field = self.field.remote_field

    if field.one_to_many:
        if hasattr(instance, "_remove_pendings_")==False:
            setattr(instance, "_remove_pendings_", {})
        remove_pendings = getattr(instance, "_remove_pendings_")
        if field.name not in remove_pendings:
            remove_pendings[field.name] = []
    else:
        raise f"{field.name}: remove_pending only implemented for one_to_many relation "
    
    if el not in remove_pendings[field.name]:
        remove_pendings[field.name].append(el)
    setattr(el, "_remove_pending_", True)


@add_method(django.db.models.manager.BaseManager)
def add_pendings(self):
    instance = self.instance
    field = self.field.remote_field
    if field.one_to_many:
        if hasattr(instance, "_add_pendings_"):
            add_pendings = getattr(instance, "_add_pendings_")
            if field.name in add_pendings:
                return add_pendings[field.name]
    else:
        raise f"{field.name}: pending functionality only implemented for one_to_many relation "

    return []

@add_method(django.db.models.manager.BaseManager)
def remove_pendings(self):
    instance = self.instance
    field = self.field.remote_field
    if field.one_to_many:
        if hasattr(instance, "_remove_pendings_"):
            remove_pendings = getattr(instance, "_remove_pendings_")
            if field.name in remove_pendings:
                return remove_pendings[field.name]
    else:
        raise f"{field.name}: pending functionality only implemented for one_to_many relation "

    return []

@add_method(django.db.models.manager.BaseManager)
def pendings(self):
    instance = self.instance
    field = self.field.remote_field
    res = []
    if field.one_to_many:
        if hasattr(instance, "_add_pendings_"):
            add_pendings = getattr(instance, "_add_pendings_")
            if field.name in add_pendings:
                res += add_pendings[field.name]
        if hasattr(instance, "_remove_pendings_"):
            remove_pendings = getattr(instance, "_remove_pendings_")
            if field.name in remove_pendings:
                res += remove_pendings[field.name]
    else:
        raise f"{field.name}: add_pending only implemented for one_to_many relation "

    return res



@overload_method(models.Model)
def save(self, overload, *args, **kwargs):

    res = overload(self, *args, **kwargs)
    
    if hasattr(self, "_remove_pendings_"):
        pendings = getattr(self, "_remove_pendings_")
        for field in pendings:
            while(len(pendings[field])>0):
                el = pendings[field].pop()
                el.delete()

    if hasattr(self, "_add_pendings_"):
        pendings = getattr(self, "_add_pendings_")
        for field in pendings:
            for el in pendings[field]:
                el.save()
    
    return res

@add_method(models.Model)
def removed_pending(self):
    if hasattr(self, "_remove_pending_"):
        return getattr(self, "_remove_pending_")
    
    return False



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
    footprint = models.ForeignKey('VersionedFile', related_name='footprint', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    symbol = models.ForeignKey('VersionedFile', related_name='symbol', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    childs = models.ManyToManyField('Part', blank=True)
    #parameters is defined inside PartParameter by ForeignKey part
    #offers is defined inside PartOffer by ForeignKey part
    #manufacturers is defined inside PartManufacturer by ForeignKey part
    #storages is defined inside PartStorage by ForeignKey part
    #attachements: is defined inside PartAttachement by ForeignKey part
    #references: is defined inside PartReference by ForeignKey part
    value_parameter = models.TextField(null=True, blank=True, default=None)
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
    min_value = models.FloatField(null=True)
    min_prefix = models.ForeignKey('UnitPrefix', related_name='min', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    nom_value = models.FloatField(null=True)
    nom_prefix = models.ForeignKey('UnitPrefix', related_name='nom', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    max_value = models.FloatField(null=True)
    max_prefix = models.ForeignKey('UnitPrefix', related_name='max', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
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

class Parameter(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    unit = models.ForeignKey('Unit', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    numeric = models.BooleanField()
    updated = models.DateTimeField(auto_now=True)

class ParameterAlias(models.Model):
    parameter = models.ForeignKey('Parameter', related_name='alias', null=False, blank=False, default=None, on_delete=models.CASCADE)
    
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


class Library(models.Model):
    path = models.TextField(blank=True, default='')
    #symbols is defined inside PartParameter by ForeignKey part
    mtime = models.FloatField()
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class LibrarySymbol(models.Model):
    library = models.ForeignKey('Library', related_name='symbols', null=False, blank=False, default=None, on_delete=models.CASCADE)
    name = models.TextField()
    content = models.TextField()
    metadata = models.TextField()
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
    