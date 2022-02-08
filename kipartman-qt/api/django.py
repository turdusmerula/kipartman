from django.db import models

# class Model(models.Model):
#     def __init__(self, *args, **kwargs):
#         super(Model, self).__init__(*args, **kwargs)
#
#     def get_fields_map(self):
#         res = {}
#         for field in self._meta.fields:
#             res[field.attname] = getattr(self, field.attname)
#         return res