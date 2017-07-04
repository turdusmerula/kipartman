import connexion
from swagger_server.models.category import Category
from swagger_server.models.error import Error
from swagger_server.models.new_category import NewCategory
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def add_parts_category(category):
    """
    add_parts_category
    Creates a new part category
    :param category: Category to add
    :type category: dict | bytes

    :rtype: Category
    """
    if connexion.request.is_json:
        category = NewCategory.from_dict(connexion.request.get_json())
    return 'do some magic!'


def delete_parts_category(category_id):
    """
    delete_parts_category
    Delete part category
    :param category_id: Part category to update
    :type category_id: int

    :rtype: None
    """
    return 'do some magic!'


def find_parts_categories():
    """
    find_parts_categories
    Return all categories for parts

    :rtype: List[Category]
    """
    return 'do some magic!'


def update_parts_category(category_id):
    """
    update_parts_category
    Update part category
    :param category_id: Part category to update
    :type category_id: int

    :rtype: Category
    """
    return 'do some magic!'
