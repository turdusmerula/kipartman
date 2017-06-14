# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class PartCategory(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    name = models.TextField()
    class MPTTMeta:
        order_insertion_by = ['name']
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Part(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    category = models.ForeignKey('PartCategory', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    footprint = models.ForeignKey('Footprint', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    comment = models.TextField(null=True, blank=True, default='')
    parts = models.ManyToManyField('Part', blank=True)
    def parameters(self):
        return PartParameter.objects.filter(part=self)
    def distributors(self):
        return PartDistributor.objects.filter(part=self)
    def manufacturers(self):
        return PartManufacturer.objects.filter(part=self)
#    def attachements(self):
#        return PartAttachement.objects.filter(part=self)

    # octopart fields
    octopart = models.TextField(null=True, blank=True, default=None)
    updated = models.DateTimeField(null=True, blank=True, default=None)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class PartParameter(models.Model):
    part = models.ForeignKey('Part', on_delete=models.DO_NOTHING, null=False, blank=False, default=None)
    name = models.TextField()
    description = models.TextField(blank=True)
    unit = models.ForeignKey('Unit', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    numeric = models.BooleanField()
    text_value = models.TextField(null=True, blank=True)
    min_value = models.FloatField(null=True)
    min_prefix = models.ForeignKey('UnitPrefix', related_name='min', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    nom_value = models.FloatField(null=True)
    nom_prefix = models.ForeignKey('UnitPrefix', related_name='nom', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    max_value = models.FloatField(null=True)
    max_prefix = models.ForeignKey('UnitPrefix', related_name='max', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class PartManufacturer(models.Model):
    part = models.ForeignKey('Part', on_delete=models.DO_NOTHING, null=False, blank=False, default=None)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.DO_NOTHING, null=False)
    part_name = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class PartDistributor(models.Model):
    part = models.ForeignKey('Part', on_delete=models.DO_NOTHING, null=False, blank=False, default=None)
    distributor = models.ForeignKey('Distributor', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    packaging_unit = models.IntegerField()
    unit_price = models.FloatField()
    currency = models.TextField(blank=True)
    sku = models.TextField(blank=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    

class Manufacturer(models.Model):
    name = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Distributor(models.Model):
    name = models.TextField(blank=False)
    address = models.TextField(blank=True, default='')
    website = models.TextField(blank=True, default='')
    sku_url = models.TextField(blank=True, default='')
    email = models.TextField(blank=True, default='')
    phone = models.TextField(blank=True, default='')
    comment = models.TextField(blank=True, default='')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class FootprintCategory(MPTTModel):
    parent = TreeForeignKey('FootprintCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Footprint(models.Model):
    category = models.ForeignKey('FootprintCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True)
    comment = models.TextField(null=True, blank=True, default='')
    image = models.ImageField(null=True, upload_to='images/%y/%m/%d/%H%M/')
    footprint = models.FileField(null=True, upload_to='footprints/%y/%m/%d/%H%M/')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    
    
class File(models.Model):
    filename = models.TextField()
    uuid = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.uuid, self.filename)


class Unit(models.Model):
    name = models.TextField()
    symbol = models.TextField(default='')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class UnitPrefix(models.Model):
    name = models.TextField()
    # suffix name
    symbol = models.TextField()
    # value contains the exponent part
    power = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
