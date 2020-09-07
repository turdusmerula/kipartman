from api.models import Part, PartCategory
from datetime import date, datetime
import mptt

def find(filters=[]):
    request = PartCategory.objects
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def find_childs(parent_category=None):
    if parent_category is None:
        return PartCategory.objects.filter(parent_id=None)
    return PartCategory.objects.filter(parent_id=parent_category.id)

####################################################    
# def add(category):
#     category.save()
# 
# 
# def delete(category):
#     # set childrens to parent id
#     for child in category.get_children():
#         if category.is_child_node():
#             parent = category.get_ancestors(ascending=True)[0]
#         else:
#             parent = None 
#         current_child = PartCategory.objects.get(id=child.id)
#         current_child.move_to(parent, 'last-child')
#     Part.objects.filter(category=category.pk).update(category=category.parent)
#     # delete category
#     category.delete()
#     # cleanup tree inconsistencies
#     PartCategory._tree_manager.rebuild()
#     return None
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
#         fcategory = deserialize_PartCategoryNew(category, api.models.PartCategory.objects.get(pk=category_id))
#     except:
#         return Error(code=1000, message='Category %d does not exists'%category_id), 403
#     
#     if category.parent:
#         # check that instance will not be child of itself
#         # TODO: with mptt there is surely a non recursive way to do this
#         try:
#             fcategory.parent = api.models.PartCategory.objects.get(pk=category.parent.id)
#         except:
#             return Error(code=1000, message='Parent %d does not exists'%category.parent.id), 403
#             
#         fparent = fcategory.parent
#         while fparent is not None:
#             if fparent.pk==category_id:
#                 return Error(code=1000, message='Category cannot be child of itself'), 403
#             if fparent.parent:
#                 fparent = api.models.PartCategory.objects.get(pk=fparent.parent.pk)
#             else:
#                 fparent = None
#     else:
#         fcategory.parent = None
#     
#     fcategory.save()
#     
#     return serialize_PartCategory(fcategory)
