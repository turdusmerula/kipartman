# coding: utf-8

from __future__ import absolute_import
from swagger_server.models.part_reference_data import PartReferenceData
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class PartReference(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, description=None, manufacturer=None, type=None, uid=None, updated=None):
        """
        PartReference - a model defined in Swagger

        :param name: The name of this PartReference.
        :type name: str
        :param description: The description of this PartReference.
        :type description: str
        :param manufacturer: The manufacturer of this PartReference.
        :type manufacturer: str
        :param type: The type of this PartReference.
        :type type: str
        :param uid: The uid of this PartReference.
        :type uid: str
        :param updated: The updated of this PartReference.
        :type updated: datetime
        """
        self.swagger_types = {
            'name': str,
            'description': str,
            'manufacturer': str,
            'type': str,
            'uid': str,
            'updated': datetime
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'manufacturer': 'manufacturer',
            'type': 'type',
            'uid': 'uid',
            'updated': 'updated'
        }

        self._name = name
        self._description = description
        self._manufacturer = manufacturer
        self._type = type
        self._uid = uid
        self._updated = updated

    @classmethod
    def from_dict(cls, dikt):
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PartReference of this PartReference.
        :rtype: PartReference
        """
        return deserialize_model(dikt, cls)

    @property
    def name(self):
        """
        Gets the name of this PartReference.

        :return: The name of this PartReference.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this PartReference.

        :param name: The name of this PartReference.
        :type name: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this PartReference.

        :return: The description of this PartReference.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this PartReference.

        :param description: The description of this PartReference.
        :type description: str
        """

        self._description = description

    @property
    def manufacturer(self):
        """
        Gets the manufacturer of this PartReference.

        :return: The manufacturer of this PartReference.
        :rtype: str
        """
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, manufacturer):
        """
        Sets the manufacturer of this PartReference.

        :param manufacturer: The manufacturer of this PartReference.
        :type manufacturer: str
        """

        self._manufacturer = manufacturer

    @property
    def type(self):
        """
        Gets the type of this PartReference.

        :return: The type of this PartReference.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this PartReference.

        :param type: The type of this PartReference.
        :type type: str
        """

        self._type = type

    @property
    def uid(self):
        """
        Gets the uid of this PartReference.

        :return: The uid of this PartReference.
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """
        Sets the uid of this PartReference.

        :param uid: The uid of this PartReference.
        :type uid: str
        """

        self._uid = uid

    @property
    def updated(self):
        """
        Gets the updated of this PartReference.

        :return: The updated of this PartReference.
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this PartReference.

        :param updated: The updated of this PartReference.
        :type updated: datetime
        """

        self._updated = updated
