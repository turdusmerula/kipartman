# coding: utf-8

from __future__ import absolute_import
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class PartCategoryRef(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, id=None):
        """
        PartCategoryRef - a model defined in Swagger

        :param id: The id of this PartCategoryRef.
        :type id: int
        """
        self.swagger_types = {
            'id': int
        }

        self.attribute_map = {
            'id': 'id'
        }

        self._id = id

    @classmethod
    def from_dict(cls, dikt):
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PartCategoryRef of this PartCategoryRef.
        :rtype: PartCategoryRef
        """
        return deserialize_model(dikt, cls)

    @property
    def id(self):
        """
        Gets the id of this PartCategoryRef.

        :return: The id of this PartCategoryRef.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this PartCategoryRef.

        :param id: The id of this PartCategoryRef.
        :type id: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

