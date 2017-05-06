# -*- coding: utf-8 -*-
from rest_client import fields
from rest_client import models

class PartCategory(models.Model):
    id = fields.IntField(read_only=True)
    path = fields.TextField(read_only=True)
    name = fields.TextField()
    parent = fields.HyperlinkField('PartCategory')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Part(models.Model):
    category = fields.HyperlinkField('PartCategory')
    metapart = fields.BooleanField()
    name = fields.TextField()
    description = fields.TextField()
    footprint = fields.HyperlinkField('Footprint')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class FootprintCategory(models.Model):
    parent = fields.HyperlinkField('FootprintCategory')
    name = fields.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Footprint(models.Model):
    category = fields.HyperlinkField('FootprintCategory')
    name = fields.TextField()
    description = fields.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    

