from database.models import Part, PartCategory
from datetime import date, datetime
import mptt

class PartCategoryException(Exception):
    def __init__(self, error):
        super(PartCategoryException, self).__init__(error)

def find(filters=[]):
    request = PartCategory.objects
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def find_childs(parent_category=None):
    if parent_category is None:
        return PartCategory.objects.filter(parent_id=None)
    return PartCategory.objects.filter(parent_id=parent_category.id)

def create():
    return PartCategory()

def save(category):
    if category.parent is not None:
        # check that instance will not be child of itself
        parent = category.parent
        while parent is not None:
            if parent.pk==category.pk:
                raise PartCategoryException('Category recursion forbidden')
            parent = parent.parent
    
    category.save()
    
    return category

def delete(category):
    # set childrens to parent id
    for child in category.get_children():
        if category.is_child_node():
            parent = category.get_ancestors(ascending=True)[0]
        else:
            parent = None 
        current_child = PartCategory.objects.get(id=child.id)
        current_child.move_to(parent, 'last-child')
    Part.objects.filter(category=category.pk).update(category=category.parent)
    # delete category
    category.delete()
    # cleanup tree inconsistencies
    PartCategory._tree_manager.rebuild()
    return None
    
####################################################    
# def add(category):
#     category.save()
# 
# 
# def delete(category):
# 
#     
#     
# def update(category_id, category):
#     """
#     update_parts_category
#     Update part category
#     :param category_id: Category id
#     :type category_id: int
#     :param category: Category to update
#     :type category: dict | bytes
# 
#     :rtype: PartCategory
#     """
#     if connexion.request.is_json:
#         category = PartCategoryNew.from_dict(connexion.request.get_json())
#     else:
#         return Error(code=1000, message='Missing payload'), 403
#     try:
#         fcategory = deserialize_PartCategoryNew(category, database.models.PartCategory.objects.get(pk=category_id))
#     except:
#         return Error(code=1000, message='Category %d does not exists'%category_id), 403
#     
#     if category.parent:
#         # check that instance will not be child of itself
#         # TODO: with mptt there is surely a non recursive way to do this
#         try:
#             fcategory.parent = database.models.PartCategory.objects.get(pk=category.parent.id)
#         except:
#             return Error(code=1000, message='Parent %d does not exists'%category.parent.id), 403
#             
#         fparent = fcategory.parent
#         while fparent is not None:
#             if fparent.pk==category_id:
#                 return Error(code=1000, message='Category cannot be child of itself'), 403
#             if fparent.parent:
#                 fparent = database.models.PartCategory.objects.get(pk=fparent.parent.pk)
#             else:
#                 fparent = None
#     else:
#         fcategory.parent = None
#     
#     fcategory.save()
#     
#     return serialize_PartCategory(fcategory)
