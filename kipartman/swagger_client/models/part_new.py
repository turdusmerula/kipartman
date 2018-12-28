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


class PartNew(object):
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
        'value_parameter': 'str',
        'category': 'PartCategoryRef',
        'childs': 'list[PartRef]',
        'footprint': 'VersionedFileRef',
        'symbol': 'VersionedFileRef',
        'parameters': 'list[PartParameter]',
        'distributors': 'list[PartDistributor]',
        'manufacturers': 'list[PartManufacturer]',
        'storages': 'list[PartStorage]',
        'attachements': 'list[PartAttachement]',
        'references': 'list[PartReference]'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'comment': 'comment',
        'value_parameter': 'value_parameter',
        'category': 'category',
        'childs': 'childs',
        'footprint': 'footprint',
        'symbol': 'symbol',
        'parameters': 'parameters',
        'distributors': 'distributors',
        'manufacturers': 'manufacturers',
        'storages': 'storages',
        'attachements': 'attachements',
        'references': 'references'
    }

    def __init__(self, name=None, description=None, comment=None, value_parameter=None, category=None, childs=None, footprint=None, symbol=None, parameters=None, distributors=None, manufacturers=None, storages=None, attachements=None, references=None):
        """
        PartNew - a model defined in Swagger
        """

        self._name = None
        self._description = None
        self._comment = None
        self._value_parameter = None
        self._category = None
        self._childs = None
        self._footprint = None
        self._symbol = None
        self._parameters = None
        self._distributors = None
        self._manufacturers = None
        self._storages = None
        self._attachements = None
        self._references = None

        if name is not None:
          self.name = name
        if description is not None:
          self.description = description
        if comment is not None:
          self.comment = comment
        if value_parameter is not None:
          self.value_parameter = value_parameter
        if category is not None:
          self.category = category
        if childs is not None:
          self.childs = childs
        if footprint is not None:
          self.footprint = footprint
        if symbol is not None:
          self.symbol = symbol
        if parameters is not None:
          self.parameters = parameters
        if distributors is not None:
          self.distributors = distributors
        if manufacturers is not None:
          self.manufacturers = manufacturers
        if storages is not None:
          self.storages = storages
        if attachements is not None:
          self.attachements = attachements
        if references is not None:
          self.references = references

    @property
    def name(self):
        """
        Gets the name of this PartNew.

        :return: The name of this PartNew.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this PartNew.

        :param name: The name of this PartNew.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this PartNew.

        :return: The description of this PartNew.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this PartNew.

        :param description: The description of this PartNew.
        :type: str
        """

        self._description = description

    @property
    def comment(self):
        """
        Gets the comment of this PartNew.

        :return: The comment of this PartNew.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """
        Sets the comment of this PartNew.

        :param comment: The comment of this PartNew.
        :type: str
        """

        self._comment = comment

    @property
    def value_parameter(self):
        """
        Gets the value_parameter of this PartNew.

        :return: The value_parameter of this PartNew.
        :rtype: str
        """
        return self._value_parameter

    @value_parameter.setter
    def value_parameter(self, value_parameter):
        """
        Sets the value_parameter of this PartNew.

        :param value_parameter: The value_parameter of this PartNew.
        :type: str
        """

        self._value_parameter = value_parameter

    @property
    def category(self):
        """
        Gets the category of this PartNew.

        :return: The category of this PartNew.
        :rtype: PartCategoryRef
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Sets the category of this PartNew.

        :param category: The category of this PartNew.
        :type: PartCategoryRef
        """

        self._category = category

    @property
    def childs(self):
        """
        Gets the childs of this PartNew.

        :return: The childs of this PartNew.
        :rtype: list[PartRef]
        """
        return self._childs

    @childs.setter
    def childs(self, childs):
        """
        Sets the childs of this PartNew.

        :param childs: The childs of this PartNew.
        :type: list[PartRef]
        """

        self._childs = childs

    @property
    def footprint(self):
        """
        Gets the footprint of this PartNew.

        :return: The footprint of this PartNew.
        :rtype: VersionedFileRef
        """
        return self._footprint

    @footprint.setter
    def footprint(self, footprint):
        """
        Sets the footprint of this PartNew.

        :param footprint: The footprint of this PartNew.
        :type: VersionedFileRef
        """

        self._footprint = footprint

    @property
    def symbol(self):
        """
        Gets the symbol of this PartNew.

        :return: The symbol of this PartNew.
        :rtype: VersionedFileRef
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """
        Sets the symbol of this PartNew.

        :param symbol: The symbol of this PartNew.
        :type: VersionedFileRef
        """

        self._symbol = symbol

    @property
    def parameters(self):
        """
        Gets the parameters of this PartNew.

        :return: The parameters of this PartNew.
        :rtype: list[PartParameter]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this PartNew.

        :param parameters: The parameters of this PartNew.
        :type: list[PartParameter]
        """

        self._parameters = parameters

    @property
    def distributors(self):
        """
        Gets the distributors of this PartNew.

        :return: The distributors of this PartNew.
        :rtype: list[PartDistributor]
        """
        return self._distributors

    @distributors.setter
    def distributors(self, distributors):
        """
        Sets the distributors of this PartNew.

        :param distributors: The distributors of this PartNew.
        :type: list[PartDistributor]
        """

        self._distributors = distributors

    @property
    def manufacturers(self):
        """
        Gets the manufacturers of this PartNew.

        :return: The manufacturers of this PartNew.
        :rtype: list[PartManufacturer]
        """
        return self._manufacturers

    @manufacturers.setter
    def manufacturers(self, manufacturers):
        """
        Sets the manufacturers of this PartNew.

        :param manufacturers: The manufacturers of this PartNew.
        :type: list[PartManufacturer]
        """

        self._manufacturers = manufacturers

    @property
    def storages(self):
        """
        Gets the storages of this PartNew.

        :return: The storages of this PartNew.
        :rtype: list[PartStorage]
        """
        return self._storages

    @storages.setter
    def storages(self, storages):
        """
        Sets the storages of this PartNew.

        :param storages: The storages of this PartNew.
        :type: list[PartStorage]
        """

        self._storages = storages

    @property
    def attachements(self):
        """
        Gets the attachements of this PartNew.

        :return: The attachements of this PartNew.
        :rtype: list[PartAttachement]
        """
        return self._attachements

    @attachements.setter
    def attachements(self, attachements):
        """
        Sets the attachements of this PartNew.

        :param attachements: The attachements of this PartNew.
        :type: list[PartAttachement]
        """

        self._attachements = attachements

    @property
    def references(self):
        """
        Gets the references of this PartNew.

        :return: The references of this PartNew.
        :rtype: list[PartReference]
        """
        return self._references

    @references.setter
    def references(self, references):
        """
        Sets the references of this PartNew.

        :param references: The references of this PartNew.
        :type: list[PartReference]
        """

        self._references = references

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
        if not isinstance(other, PartNew):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
