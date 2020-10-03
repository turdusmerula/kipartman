from api.models import Storage, StorageCategory
from datetime import date, datetime
import mptt

class StorageCategoryException(Exception):
    def __init__(self, error):
        super(StorageCategoryException, self).__init__(error)

def find(filters=[]):
    request = StorageCategory.objects
    
    for filter in filters:
        request = filter.apply(request)
    
    return request.order_by('id').all()

def find_childs(parent_category=None):
    if parent_category is None:
        return StorageCategory.objects.filter(parent_id=None)
    return StorageCategory.objects.filter(parent_id=parent_category.id)

def create():
    return StorageCategory()

def save(category):
    if category.parent is not None:
        # check that instance will not be child of itself
        parent = category.parent
        while parent is not None:
            if parent.pk==category.pk:
                raise StorageCategoryException('Category recursion forbidden')
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
        current_child = StorageCategory.objects.get(id=child.id)
        current_child.move_to(parent, 'last-child')
    Storage.objects.filter(category=category.pk).update(category=category.parent)
    # delete category
    category.delete()
    # cleanup tree inconsistencies
    StorageCategory._tree_manager.rebuild()
    return None
