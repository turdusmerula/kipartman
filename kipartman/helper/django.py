from helper.class_tool import add_method, overload_method
import django.db.models.manager


@add_method(django.db.models.manager.BaseManager)
def add_pending(self, el):
    """
    allow a relation to carry elements to be persisted later during save.
    """

    instance = self.instance
    if hasattr(instance, "_add_pendings_")==False:
        setattr(instance, "_add_pendings_", {})

    if hasattr(self, "field") and self.field.many_to_one:
        _add_pending_many_to_one(self, el)
    else:
        raise f"add_pending not implemented for this relation "

    if hasattr(el, "_remove_pending_"):
        delattr(el, "_remove_pending_")

def _add_pending_many_to_one(self, el):
    instance = self.instance
    relation_field = self.field.remote_field
    field = self.field
    name = relation_field.name
      
    add_pendings = getattr(instance, "_add_pendings_")
    if name not in add_pendings:
        add_pendings[name] = []
      
    add_pendings[name].append((el, field))

def _add_pending_many_to_many(self, el):
#     instance = self.instance
#     if hasattr(self, "target_field"):
#         # field is a many to many relation
#         relation_field = self.target_field
#         field = self.target_field
#     else:
#         relation_field = self.field.remote_field
#         field = self.field
#          
#     if relation_field.one_to_many:
#         name = field.name
#     elif relation_field.many_to_one:
#         name = self.prefetch_cache_name
#     else:
#         raise f"{field.name}: add_pending not implemented for this relation "
#  
#     if hasattr(instance, "_add_pendings_")==False:
#         setattr(instance, "_add_pendings_", {})
#     add_pendings = getattr(instance, "_add_pendings_")
#      
#     if name not in add_pendings:
#         add_pendings[name] = []
#  
#     if hasattr(el, "_remove_pending_"):
#         delattr(el, "_remove_pending_")
#      
#     add_pendings[name].append((el, field))
    pass


@add_method(django.db.models.manager.BaseManager)
def remove_pending(self, el):
    instance = self.instance
    if hasattr(instance, "_remove_pendings_")==False:
        setattr(instance, "_remove_pendings_", {})
        
    if hasattr(self, "field") and self.field.many_to_one:
        _remove_pending_many_to_one(self, el)
    else:
        raise f"remove_pending not implemented for this relation "
  
    setattr(el, "_remove_pending_", True)
 
def _remove_pending_many_to_one(self, el):
    instance = self.instance
    field = self.field.remote_field
    name = field.name
         
    remove_pendings = getattr(instance, "_remove_pendings_")
    if name not in remove_pendings:
        remove_pendings[name] = []
     
    if el not in remove_pendings[name]:
        remove_pendings[name].append(el)

def _remove_pending_many_to_many(self, el):
#     instance = self.instance
#     if hasattr(self, "target_field"):
#         # field is a many to many relation
#         field = self.target_field
#     else:
#         field = self.field.remote_field
#          
#     if field.one_to_many:
#         name = field.name
#     elif field.many_to_one:
#         name = self.name
#     else:
#         raise f"{field.name}: remove_pending only implemented for one_to_many relation "
#  
#     if hasattr(instance, "_remove_pendings_")==False:
#         setattr(instance, "_remove_pendings_", {})
#     remove_pendings = getattr(instance, "_remove_pendings_")
#  
#     if name not in remove_pendings:
#         remove_pendings[name] = []
#      
#     if el not in remove_pendings[name]:
#         remove_pendings[name].append(el)
#  
#     setattr(el, "_remove_pending_", True)
    pass


@add_method(django.db.models.manager.BaseManager)
def add_pendings(self):
    """
    return list of elements pending to be added by save
    """
    instance = self.instance
    if hasattr(self, "target_field"):
        # field is a many to many relation
        field = self.target_field
        name = self.name
    else:
        field = self.field.remote_field
        name = field.name
 
    if field.one_to_many:
        name = field.name
    elif field.many_to_one:
        name = self.name
    else:
        raise f"{field.name}: pending functionality only implemented for one_to_many relation "
 
    if hasattr(instance, "_add_pendings_"):
        add_pendings = getattr(instance, "_add_pendings_")
        if name in add_pendings:
            return [el for el, elfield in add_pendings[name]]
 
    return []
 
@add_method(django.db.models.manager.BaseManager)
def remove_pendings(self):
    """
    return list of elements pending to be removed by save
    """
    instance = self.instance
    field = self.field.remote_field
    if field.one_to_many:
        if hasattr(instance, "_remove_pendings_"):
            remove_pendings = getattr(instance, "_remove_pendings_")
            if field.name in remove_pendings:
                return remove_pendings[field.name]
    else:
        raise f"{field.name}: pending functionality only implemented for one_to_many relation "
 
    return []
 
@add_method(django.db.models.manager.BaseManager)
def pendings(self):
    """
    return list of elements where an action is pending on save
    """
    instance = self.instance
    field = self.field.remote_field
    res = []
    if field.one_to_many:
        if hasattr(instance, "_add_pendings_"):
            add_pendings = getattr(instance, "_add_pendings_")
            if field.name in add_pendings:
                res += [el for el, elfield in add_pendings[field.name]]
        if hasattr(instance, "_remove_pendings_"):
            remove_pendings = getattr(instance, "_remove_pendings_")
            if field.name in remove_pendings:
                res += remove_pendings[field.name]
    else:
        raise f"{field.name}: add_pending only implemented for one_to_many relation "
 
    return res
 
 

@overload_method(django.db.models.Model)
def save(self, overload, *args, **kwargs):
 
    res = overload(self, *args, **kwargs)
     
    if hasattr(self, "_remove_pendings_"):
        pendings = getattr(self, "_remove_pendings_")
        for field in pendings:
            while(len(pendings[field])>0):
                el = pendings[field].pop()
                el.delete()
 
    if hasattr(self, "_add_pendings_"):
        pendings = getattr(self, "_add_pendings_")
        for field in pendings:
            for el, elfield in pendings[field]:
                if elfield.many_to_one:
                    setattr(el, f"{elfield.remote_field.field.name}_{elfield.remote_field.field_name}", self.id)
                    el.save()
                elif elfield.many_to_many:
                    getattr(self, field).add(el)
                else:
                    raise f"save not implemented for this relation "
        pendings.clear()
     
    return res


@add_method(django.db.models.Model)
def removed_pending(self):
    if hasattr(self, "_remove_pending_"):
        return getattr(self, "_remove_pending_")
     
    return False
