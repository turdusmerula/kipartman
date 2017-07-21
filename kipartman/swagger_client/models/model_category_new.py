# coding: utf-8

"""
    Kipartman

    Kipartman api specifications

    OpenAPI spec version: 1.0.0
    Contact: --
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ModelCategoryNew(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, description=None, parent=None):
        """
        ModelCategoryNew - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'description': 'str',
            'parent': 'ModelCategoryRef'
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'parent': 'parent'
        }

        self._name = name
        self._description = description
        self._parent = parent

    @property
    def name(self):
        """
        Gets the name of this ModelCategoryNew.

        :return: The name of this ModelCategoryNew.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ModelCategoryNew.

        :param name: The name of this ModelCategoryNew.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this ModelCategoryNew.

        :return: The description of this ModelCategoryNew.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ModelCategoryNew.

        :param description: The description of this ModelCategoryNew.
        :type: str
        """

        self._description = description

    @property
    def parent(self):
        """
        Gets the parent of this ModelCategoryNew.

        :return: The parent of this ModelCategoryNew.
        :rtype: ModelCategoryRef
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """
        Sets the parent of this ModelCategoryNew.

        :param parent: The parent of this ModelCategoryNew.
        :type: ModelCategoryRef
        """

        self._parent = parent

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, ModelCategoryNew):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
