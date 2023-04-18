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


class PartOfferData(object):
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
        'packaging_unit': 'int',
        'quantity': 'int',
        'min_order_quantity': 'int',
        'unit_price': 'float',
        'available_stock': 'int',
        'packaging': 'str',
        'currency': 'str',
        'sku': 'str',
        'updated': 'str'
    }

    attribute_map = {
        'packaging_unit': 'packaging_unit',
        'quantity': 'quantity',
        'min_order_quantity': 'min_order_quantity',
        'unit_price': 'unit_price',
        'available_stock': 'available_stock',
        'packaging': 'packaging',
        'currency': 'currency',
        'sku': 'sku',
        'updated': 'updated'
    }

    def __init__(self, packaging_unit=None, quantity=None, min_order_quantity=None, unit_price=None, available_stock=None, packaging=None, currency=None, sku=None, updated=None):
        """
        PartOfferData - a model defined in Swagger
        """

        self._packaging_unit = None
        self._quantity = None
        self._min_order_quantity = None
        self._unit_price = None
        self._available_stock = None
        self._packaging = None
        self._currency = None
        self._sku = None
        self._updated = None

        if packaging_unit is not None:
          self.packaging_unit = packaging_unit
        if quantity is not None:
          self.quantity = quantity
        if min_order_quantity is not None:
          self.min_order_quantity = min_order_quantity
        if unit_price is not None:
          self.unit_price = unit_price
        if available_stock is not None:
          self.available_stock = available_stock
        if packaging is not None:
          self.packaging = packaging
        if currency is not None:
          self.currency = currency
        if sku is not None:
          self.sku = sku
        if updated is not None:
          self.updated = updated

    @property
    def packaging_unit(self):
        """
        Gets the packaging_unit of this PartOfferData.

        :return: The packaging_unit of this PartOfferData.
        :rtype: int
        """
        return self._packaging_unit

    @packaging_unit.setter
    def packaging_unit(self, packaging_unit):
        """
        Sets the packaging_unit of this PartOfferData.

        :param packaging_unit: The packaging_unit of this PartOfferData.
        :type: int
        """

        self._packaging_unit = packaging_unit

    @property
    def quantity(self):
        """
        Gets the quantity of this PartOfferData.

        :return: The quantity of this PartOfferData.
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """
        Sets the quantity of this PartOfferData.

        :param quantity: The quantity of this PartOfferData.
        :type: int
        """

        self._quantity = quantity

    @property
    def min_order_quantity(self):
        """
        Gets the min_order_quantity of this PartOfferData.

        :return: The min_order_quantity of this PartOfferData.
        :rtype: int
        """
        return self._min_order_quantity

    @min_order_quantity.setter
    def min_order_quantity(self, min_order_quantity):
        """
        Sets the min_order_quantity of this PartOfferData.

        :param min_order_quantity: The min_order_quantity of this PartOfferData.
        :type: int
        """

        self._min_order_quantity = min_order_quantity

    @property
    def unit_price(self):
        """
        Gets the unit_price of this PartOfferData.

        :return: The unit_price of this PartOfferData.
        :rtype: float
        """
        return self._unit_price

    @unit_price.setter
    def unit_price(self, unit_price):
        """
        Sets the unit_price of this PartOfferData.

        :param unit_price: The unit_price of this PartOfferData.
        :type: float
        """

        self._unit_price = unit_price

    @property
    def available_stock(self):
        """
        Gets the available_stock of this PartOfferData.

        :return: The available_stock of this PartOfferData.
        :rtype: int
        """
        return self._available_stock

    @available_stock.setter
    def available_stock(self, available_stock):
        """
        Sets the available_stock of this PartOfferData.

        :param available_stock: The available_stock of this PartOfferData.
        :type: int
        """

        self._available_stock = available_stock

    @property
    def packaging(self):
        """
        Gets the packaging of this PartOfferData.

        :return: The packaging of this PartOfferData.
        :rtype: str
        """
        return self._packaging

    @packaging.setter
    def packaging(self, packaging):
        """
        Sets the packaging of this PartOfferData.

        :param packaging: The packaging of this PartOfferData.
        :type: str
        """

        self._packaging = packaging

    @property
    def currency(self):
        """
        Gets the currency of this PartOfferData.

        :return: The currency of this PartOfferData.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """
        Sets the currency of this PartOfferData.

        :param currency: The currency of this PartOfferData.
        :type: str
        """

        self._currency = currency

    @property
    def sku(self):
        """
        Gets the sku of this PartOfferData.

        :return: The sku of this PartOfferData.
        :rtype: str
        """
        return self._sku

    @sku.setter
    def sku(self, sku):
        """
        Sets the sku of this PartOfferData.

        :param sku: The sku of this PartOfferData.
        :type: str
        """

        self._sku = sku

    @property
    def updated(self):
        """
        Gets the updated of this PartOfferData.

        :return: The updated of this PartOfferData.
        :rtype: str
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this PartOfferData.

        :param updated: The updated of this PartOfferData.
        :type: str
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
        if not isinstance(other, PartOfferData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other