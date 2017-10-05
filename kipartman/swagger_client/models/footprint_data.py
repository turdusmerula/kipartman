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


class FootprintData(object):
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
        'snapeda': 'str',
        'snapeda_uid': 'str',
        'updated': 'datetime'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'comment': 'comment',
        'snapeda': 'snapeda',
        'snapeda_uid': 'snapeda_uid',
        'updated': 'updated'
    }

    def __init__(self, name=None, description=None, comment=None, snapeda=None, snapeda_uid=None, updated=None):
        """
        FootprintData - a model defined in Swagger
        """

        self._name = None
        self._description = None
        self._comment = None
        self._snapeda = None
        self._snapeda_uid = None
        self._updated = None

        if name is not None:
          self.name = name
        if description is not None:
          self.description = description
        if comment is not None:
          self.comment = comment
        if snapeda is not None:
          self.snapeda = snapeda
        if snapeda_uid is not None:
          self.snapeda_uid = snapeda_uid
        if updated is not None:
          self.updated = updated

    @property
    def name(self):
        """
        Gets the name of this FootprintData.

        :return: The name of this FootprintData.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FootprintData.

        :param name: The name of this FootprintData.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this FootprintData.

        :return: The description of this FootprintData.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this FootprintData.

        :param description: The description of this FootprintData.
        :type: str
        """

        self._description = description

    @property
    def comment(self):
        """
        Gets the comment of this FootprintData.

        :return: The comment of this FootprintData.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """
        Sets the comment of this FootprintData.

        :param comment: The comment of this FootprintData.
        :type: str
        """

        self._comment = comment

    @property
    def snapeda(self):
        """
        Gets the snapeda of this FootprintData.

        :return: The snapeda of this FootprintData.
        :rtype: str
        """
        return self._snapeda

    @snapeda.setter
    def snapeda(self, snapeda):
        """
        Sets the snapeda of this FootprintData.

        :param snapeda: The snapeda of this FootprintData.
        :type: str
        """

        self._snapeda = snapeda

    @property
    def snapeda_uid(self):
        """
        Gets the snapeda_uid of this FootprintData.

        :return: The snapeda_uid of this FootprintData.
        :rtype: str
        """
        return self._snapeda_uid

    @snapeda_uid.setter
    def snapeda_uid(self, snapeda_uid):
        """
        Sets the snapeda_uid of this FootprintData.

        :param snapeda_uid: The snapeda_uid of this FootprintData.
        :type: str
        """

        self._snapeda_uid = snapeda_uid

    @property
    def updated(self):
        """
        Gets the updated of this FootprintData.

        :return: The updated of this FootprintData.
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this FootprintData.

        :param updated: The updated of this FootprintData.
        :type: datetime
        """

        self._updated = updated

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
        if not isinstance(other, FootprintData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
