# coding: utf-8

from __future__ import absolute_import
from .base_model_ import Model as BaseModel
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class ModelData(BaseModel):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, description=None, comment=None, snapeda=None, snapeda_uid=None, updated=None):
        """
        ModelData - a model defined in Swagger

        :param name: The name of this ModelData.
        :type name: str
        :param description: The description of this ModelData.
        :type description: str
        :param comment: The comment of this ModelData.
        :type comment: str
        :param snapeda: The snapeda of this ModelData.
        :type snapeda: str
        :param snapeda_uid: The snapeda_uid of this ModelData.
        :type snapeda_uid: str
        :param updated: The updated of this ModelData.
        :type updated: datetime
        """
        self.swagger_types = {
            'name': str,
            'description': str,
            'comment': str,
            'snapeda': str,
            'snapeda_uid': str,
            'updated': datetime
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'comment': 'comment',
            'snapeda': 'snapeda',
            'snapeda_uid': 'snapeda_uid',
            'updated': 'updated'
        }

        self._name = name
        self._description = description
        self._comment = comment
        self._snapeda = snapeda
        self._snapeda_uid = snapeda_uid
        self._updated = updated

    @classmethod
    def from_dict(cls, dikt):
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ModelData of this ModelData.
        :rtype: ModelData
        """
        return deserialize_model(dikt, cls)

    @property
    def name(self):
        """
        Gets the name of this ModelData.

        :return: The name of this ModelData.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ModelData.

        :param name: The name of this ModelData.
        :type name: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this ModelData.

        :return: The description of this ModelData.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ModelData.

        :param description: The description of this ModelData.
        :type description: str
        """

        self._description = description

    @property
    def comment(self):
        """
        Gets the comment of this ModelData.

        :return: The comment of this ModelData.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """
        Sets the comment of this ModelData.

        :param comment: The comment of this ModelData.
        :type comment: str
        """

        self._comment = comment

    @property
    def snapeda(self):
        """
        Gets the snapeda of this ModelData.

        :return: The snapeda of this ModelData.
        :rtype: str
        """
        return self._snapeda

    @snapeda.setter
    def snapeda(self, snapeda):
        """
        Sets the snapeda of this ModelData.

        :param snapeda: The snapeda of this ModelData.
        :type snapeda: str
        """

        self._snapeda = snapeda

    @property
    def snapeda_uid(self):
        """
        Gets the snapeda_uid of this ModelData.

        :return: The snapeda_uid of this ModelData.
        :rtype: str
        """
        return self._snapeda_uid

    @snapeda_uid.setter
    def snapeda_uid(self, snapeda_uid):
        """
        Sets the snapeda_uid of this ModelData.

        :param snapeda_uid: The snapeda_uid of this ModelData.
        :type snapeda_uid: str
        """

        self._snapeda_uid = snapeda_uid

    @property
    def updated(self):
        """
        Gets the updated of this ModelData.

        :return: The updated of this ModelData.
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this ModelData.

        :param updated: The updated of this ModelData.
        :type updated: datetime
        """

        self._updated = updated

