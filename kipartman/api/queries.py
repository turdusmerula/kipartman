from rest_client import queries
from api import models

class PartsQuery(queries.QuerySet):
    path = '/parts/{part}'
    model = models.Part

class PartCategoriesQuery(queries.QuerySet):
    path = '/parts-categories/{category}'
    model = models.PartCategory

class FootprintsQuery(queries.QuerySet):
    path = '/footprints'
    model = models.Footprint

class FootprintCategoriesQuery(queries.QuerySet):
    path = '/footprints-categories'
    model = models.FootprintCategory

