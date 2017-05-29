# -*- coding: utf-8 -*-
from rest_client import fields
from rest_client import models

class PartCategory(models.Model):
    id = fields.IntegerField(read_only=True)
    path = fields.TextField(read_only=True)
    name = fields.TextField()
    parent = fields.HyperlinkField('PartCategory')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Part(models.Model):
    id = fields.IntegerField(read_only=True)
    path = fields.TextField(read_only=True)
    name = fields.TextField()
    description = fields.TextField()
    category = fields.HyperlinkField('PartCategory')
    footprint = fields.HyperlinkField('Footprint')
    comment = fields.TextField()
    parts = fields.ListField(model='Part')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class FootprintCategory(models.Model):
    id = fields.IntegerField(read_only=True)
    path = fields.TextField(read_only=True)
    parent = fields.HyperlinkField('FootprintCategory')
    name = fields.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Footprint(models.Model):
    id = fields.IntegerField(read_only=True)
    path = fields.TextField(read_only=True)
    category = fields.HyperlinkField('FootprintCategory')
    name = fields.TextField()
    description = fields.TextField()
    comment = fields.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    

