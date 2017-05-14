# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class PartCategory(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='children', db_index=True)
#    parent = models.ForeignKey('PartCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    class MPTTMeta:
        order_insertion_by = ['name']
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Part(models.Model):
    category = models.ForeignKey('PartCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    metapart = models.BooleanField()
    name = models.TextField()
    description = models.TextField(blank=True)
    footprint = models.ForeignKey('Footprint', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class FootprintCategory(models.Model):
    parent = models.ForeignKey('FootprintCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Footprint(models.Model):
    category = models.ForeignKey('FootprintCategory', on_delete=models.DO_NOTHING)
    name = models.TextField()
    description = models.TextField(blank=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    
