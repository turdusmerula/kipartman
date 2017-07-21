# coding: utf-8

from __future__ import absolute_import
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class ModelCategoryData(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, description=None):
        """
        ModelCategoryData - a model defined in Swagger

        :param name: The name of this ModelCategoryData.
        :type name: str
        :param description: The description of this ModelCategoryData.
        :type description: str
        """
        self.swagger_types = {
            'name': str,
            'description': str
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description'
        }

        self._name = name
        self._description = description

    @classmethod
    def from_dict(cls, dikt):
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ModelCategoryData of this ModelCategoryData.
        :rtype: ModelCategoryData
        """
        return deserialize_model(dikt, cls)

    @property
    def name(self):
        """
        Gets the name of this ModelCategoryData.

        :return: The name of this ModelCategoryData.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ModelCategoryData.

        :param name: The name of this ModelCategoryData.
        :type name: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this ModelCategoryData.

        :return: The description of this ModelCategoryData.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ModelCategoryData.

        :param description: The description of this ModelCategoryData.
        :type description: str
        """

        self._description = description

