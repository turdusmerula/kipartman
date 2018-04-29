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


class PartData(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'description': 'str',
        'comment': 'str',
        'octopart': 'str',
        'octopart_uid': 'str',
        'updated': 'datetime',
        'value_parameter': 'PartParameterRef'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'comment': 'comment',
        'octopart': 'octopart',
        'octopart_uid': 'octopart_uid',
        'updated': 'updated',
        'value_parameter': 'value_parameter'
    }

    def __init__(self, name=None, description=None, comment=None, octopart=None, octopart_uid=None, updated=None, value_parameter=None):
        """
        PartData - a model defined in Swagger
        """

        self._name = None
        self._description = None
        self._comment = None
        self._octopart = None
        self._octopart_uid = None
        self._updated = None
        self._value_parameter = None

        if name is not None:
          self.name = name
        if description is not None:
          self.description = description
        if comment is not None:
          self.comment = comment
        if octopart is not None:
          self.octopart = octopart
        if octopart_uid is not None:
          self.octopart_uid = octopart_uid
        if updated is not None:
          self.updated = updated
        if value_parameter is not None:
          self.value_parameter = value_parameter

    @property
    def name(self):
        """
        Gets the name of this PartData.

        :return: The name of this PartData.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this PartData.

        :param name: The name of this PartData.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this PartData.

        :return: The description of this PartData.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this PartData.

        :param description: The description of this PartData.
        :type: str
        """

        self._description = description

    @property
    def comment(self):
        """
        Gets the comment of this PartData.

        :return: The comment of this PartData.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """
        Sets the comment of this PartData.

        :param comment: The comment of this PartData.
        :type: str
        """

        self._comment = comment

    @property
    def octopart(self):
        """
        Gets the octopart of this PartData.

        :return: The octopart of this PartData.
        :rtype: str
        """
        return self._octopart

    @octopart.setter
    def octopart(self, octopart):
        """
        Sets the octopart of this PartData.

        :param octopart: The octopart of this PartData.
        :type: str
        """

        self._octopart = octopart

    @property
    def octopart_uid(self):
        """
        Gets the octopart_uid of this PartData.

        :return: The octopart_uid of this PartData.
        :rtype: str
        """
        return self._octopart_uid

    @octopart_uid.setter
    def octopart_uid(self, octopart_uid):
        """
        Sets the octopart_uid of this PartData.

        :param octopart_uid: The octopart_uid of this PartData.
        :type: str
        """

        self._octopart_uid = octopart_uid

    @property
    def updated(self):
        """
        Gets the updated of this PartData.

        :return: The updated of this PartData.
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this PartData.

        :param updated: The updated of this PartData.
        :type: datetime
        """

        self._updated = updated

    @property
    def value_parameter(self):
        """
        Gets the value_parameter of this PartData.

        :return: The value_parameter of this PartData.
        :rtype: PartParameterRef
        """
        return self._value_parameter

    @value_parameter.setter
    def value_parameter(self, value_parameter):
        """
        Sets the value_parameter of this PartData.

        :param value_parameter: The value_parameter of this PartData.
        :type: PartParameterRef
        """

        self._value_parameter = value_parameter

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
        if not isinstance(other, PartData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
