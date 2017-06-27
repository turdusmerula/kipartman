from rest_client import queries
from api import models

class PartsQuery(queries.QuerySet):
    path = '/parts/{part}'
    model = models.Part

class PartCategoriesQuery(queries.QuerySet):
    path = '/parts-categories/{category}'
    model = models.PartCategory

class PartParametersQuery(queries.QuerySet):
    path = '/part-parameters/{parameter}'
    model = models.PartParameter

class PartDistributorsQuery(queries.QuerySet):
    path = '/part-distributors/{distributor}'
    model = models.PartDistributor

class PartManufacturersQuery(queries.QuerySet):
    path = '/part-manufacturers/{manufacturer}'
    model = models.PartManufacturer

class FootprintsQuery(queries.QuerySet):
    path = '/footprints/{footprint}'
    model = models.Footprint

class FootprintCategoriesQuery(queries.QuerySet):
    path = '/footprints-categories/{category}'
    model = models.FootprintCategory


class DistributorsQuery(queries.QuerySet):
    path = '/distributors/{distributor}'
    model = models.Distributor

class ManufacturersQuery(queries.QuerySet):
    path = '/manufacturers/{manufacturer}'
    model = models.Manufacturer

class UnitsQuery(queries.QuerySet):
    path = '/units/{unit}'
    model = models.Unit

class UnitPrefixesQuery(queries.QuerySet):
    path = '/unitprefixes/{unitprefix}'
    model = models.UnitPrefix
