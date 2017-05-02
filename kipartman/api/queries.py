from rest_client import queries

class PartsQuery(queries.QuerySet):
    path = '/parts'

class PartQuery(queries.QuerySet):
    path = '/parts'


class PartCategoriesQuery(queries.QuerySet):
    path = '/parts/categories'
#    serializer_class = 

class PartCategoryQuery(queries.Query):
    pass


class FootprintsQuery(queries.QuerySet):
    path = '/footprints'

class FootprintQuery(queries.QuerySet):
    path = '/footprints'


class FootprintCategoriesQuery(queries.QuerySet):
    path = '/parts/categories'
    
class FootprintCategoryQuery(queries.Query):
    pass

