import connexion
from swagger_server.models.symbol import Symbol
from swagger_server.models.symbol_data import SymbolData
from swagger_server.models.symbol_new import SymbolNew

from swagger_server.models.symbol_category import SymbolCategory
from swagger_server.models.symbol_category_ref import SymbolCategoryRef

from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime
 
from swagger_server.controllers.controller_symbol_category import find_symbols_category,\
    find_symbols_categories
from swagger_server.controllers.controller_upload_file import find_upload_file
from swagger_server.controllers.helpers import raise_on_error, ControllerError

import api.models
from django.db.models import Q
#import jsonpickle
def serialize_SymbolData(fsymbol, symbol=None):
    if symbol is None:
        symbol = SymbolData()
    symbol.name = fsymbol.name
    symbol.description = fsymbol.description
    symbol.comment = fsymbol.comment
    if fsymbol.snapeda:
        symbol.snapeda = fsymbol.snapeda
    if fsymbol.snapeda_uid:
        symbol.snapeda_uid = fsymbol.snapeda_uid
    if fsymbol.updated:
        symbol.updated = fsymbol.updated
    return symbol

def serialize_Symbol(fsymbol, symbol=None):
    if symbol is None:
        symbol = Symbol()
    symbol.id = fsymbol.id
    serialize_SymbolData(fsymbol, symbol)
    if fsymbol.category:
        symbol.category = raise_on_error(find_symbols_category(fsymbol.category.id))
    if fsymbol.image:
        symbol.image = raise_on_error(find_upload_file(fsymbol.image.id))
    if fsymbol.symbol:
        symbol.symbol = raise_on_error(find_upload_file(fsymbol.symbol.id))
    return symbol


def deserialize_SymbolData(symbol, fsymbol=None):
    if fsymbol is None:
        fsymbol = api.models.Symbol()
    fsymbol.name = symbol.name
    fsymbol.description = symbol.description
    fsymbol.comment = symbol.comment
    if symbol.snapeda:
        fsymbol.snapeda = symbol.snapeda
    if symbol.snapeda_uid:
        fsymbol.snapeda_uid = symbol.snapeda_uid
    if symbol.updated:
        fsymbol.updated = symbol.updated
    return fsymbol


def deserialize_SymbolNew(symbol, fsymbol=None):
    fsymbol = deserialize_SymbolData(symbol, fsymbol)
    if symbol.category:
        fsymbol.category = api.models.SymbolCategory.objects.get(id=symbol.category.id)
    else:
        fsymbol.category = None
        
    if symbol.image:
        fsymbol.image = api.models.File.objects.get(id=symbol.image.id)
    else:
        fsymbol.image = None
        
    if symbol.symbol:
        fsymbol.symbol = api.models.File.objects.get(id=symbol.symbol.id)
    else:
        fsymbol.symbol = None

    return fsymbol


def add_symbol(symbol):
    """
    add_symbol
    Creates a new symbol
    :param symbol: Symbol to add
    :type symbol: dict | bytes

    :rtype: Symbol
    """
    if connexion.request.is_json:
        symbol = SymbolNew.from_dict(connexion.request.get_json())

    try:
        fsymbol = deserialize_SymbolNew(symbol)
    except ControllerError as e:
        return e.error, 403

        
    fsymbol.save()
    
    return serialize_Symbol(fsymbol)


def delete_symbol(symbol_id):
    """
    delete_symbol
    Delete symbol
    :param symbol_id: Symbol id
    :type symbol_id: int

    :rtype: None
    """
    try:
        fsymbol = api.models.Symbol.objects.get(pk=symbol_id)
    except:
        return Error(code=1000, message='Symbol %d does not exists'%symbol_id), 403
    # delete symbol
    fsymbol.delete()
    return None


def find_symbol(symbol_id):
    """
    find_symbol
    Return a symbol
    :param symbol_id: Symbol id
    :type symbol_id: int

    :rtype: Symbol
    """
    try:
        fsymbol = api.models.Symbol.objects.get(pk=symbol_id)
    except:
        return Error(code=1000, message='Symbol %d does not exists'%symbol_id), 403
    
    try:
        symbol = serialize_Symbol(fsymbol)
    except ControllerError as e:
        return e.error, 403
    
    return symbol

def find_symbols(category=None, search=None):
    """
    find_symbols
    Return all symbols
    :param category: Filter by category
    :type category: int
    :param search: Search for symbol matching pattern
    :type search: str

    :rtype: List[Symbol]
    """
    symbols = []
    
    fsymbol_query = api.models.Symbol.objects
    
    if search:
        fsymbol_query = fsymbol_query.filter(
                    Q(name__contains=search) |
                    Q(description__contains=search) |
                    Q(comment__contains=search)
                )

    if category:
        # extract category
        categories = api.models.SymbolCategory.objects.get(pk=int(category)).get_descendants(include_self=True)
        category_ids = [category.id for category in categories]
        # add a category filter
        fsymbol_query = fsymbol_query.filter(category__in=category_ids)

    for fsymbol in fsymbol_query.all():
        symbols.append(serialize_Symbol(fsymbol))

    return symbols

def update_symbol(symbol_id, symbol):
    """
    update_symbol
    Update symbol
    :param symbol_id: Symbol id
    :type symbol_id: int
    :param symbol: Symbol to update
    :type symbol: dict | bytes

    :rtype: Symbol
    """
    if connexion.request.is_json:
        symbol = SymbolNew.from_dict(connexion.request.get_json())
    else:
        return Error(code=1000, message='Missing payload'), 403

    try:
        fsymbol = deserialize_SymbolNew(symbol, api.models.Symbol.objects.get(pk=symbol_id))
    except:
        return Error(code=1000, message='Symbol %d does not exists'%symbol_id), 403     

    fsymbol.save()
    
    return serialize_Symbol(fsymbol)
