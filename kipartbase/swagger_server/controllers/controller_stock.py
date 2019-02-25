from swagger_server.controllers.controller_storage import find_storage
from swagger_server.controllers.controller_part import find_part
from swagger_server.controllers.helpers import raise_on_error, ControllerError
from swagger_server.models.error import Error
import api.models

def update_stock(stock):
    """
    update_stock
    Add an amount of parts to stock
    :param stock: Storage
    :type stock: dict | bytes

    :rtype: None
    """
    
    print(stock)
    
    try:
        part_id = int(stock['part_id'])
        storage = stock['storage']
        amount = int(stock['amount'])
        reason = stock['reason']
    except Exception as e:
        return Error(code=1000, message=e.format()), 403

    try:
        part = raise_on_error(find_part(part_id))
    except ControllerError as e:
        return e.error, 403

    try:
        fpart = api.models.Part.objects.get(id=part_id)
    except:
        return Error(code=1000, message='Part %d does not exists'%part_id), 403
 
    if amount==0:
        return 200

    found = False
    for fstorage in fpart.storages.all():
        if fstorage.storage.name==storage['name']:
            found = True
            fstorage.quantity = fstorage.quantity+amount
            if fstorage.quantity<0:
                fstorage.quantity = 0
            fstorage.save()
    if found==False:
        return Error(code=1000, message="Storage '%s' not found"%storage['name']), 403
                    
    return 200
