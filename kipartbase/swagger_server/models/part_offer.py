# coding: utf-8

from __future__ import absolute_import
from swagger_server.models.part_offer_data import PartOfferData
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class PartOffer(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, packaging_unit=None, quantity=None, min_order_quantity=None, unit_price=None, available_stock=None, packaging=None, currency=None, sku=None, updated=None, id=None):
        """
        PartOffer - a model defined in Swagger

        :param packaging_unit: The packaging_unit of this PartOffer.
        :type packaging_unit: int
        :param quantity: The quantity of this PartOffer.
        :type quantity: int
        :param min_order_quantity: The min_order_quantity of this PartOffer.
        :type min_order_quantity: int
        :param unit_price: The unit_price of this PartOffer.
        :type unit_price: float
        :param available_stock: The available_stock of this PartOffer.
        :type available_stock: int
        :param packaging: The packaging of this PartOffer.
        :type packaging: str
        :param currency: The currency of this PartOffer.
        :type currency: str
        :param sku: The sku of this PartOffer.
        :type sku: str
        :param updated: The updated of this PartOffer.
        :type updated: str
        :param id: The id of this PartOffer.
        :type id: int
        """
        self.swagger_types = {
            'packaging_unit': int,
            'quantity': int,
            'min_order_quantity': int,
            'unit_price': float,
            'available_stock': int,
            'packaging': str,
            'currency': str,
            'sku': str,
            'updated': str,
            'id': int
        }

        self.attribute_map = {
            'packaging_unit': 'packaging_unit',
            'quantity': 'quantity',
            'min_order_quantity': 'min_order_quantity',
            'unit_price': 'unit_price',
            'available_stock': 'available_stock',
            'packaging': 'packaging',
            'currency': 'currency',
            'sku': 'sku',
            'updated': 'updated',
            'id': 'id'
        }

        self._packaging_unit = packaging_unit
        self._quantity = quantity
        self._min_order_quantity = min_order_quantity
        self._unit_price = unit_price
        self._available_stock = available_stock
        self._packaging = packaging
        self._currency = currency
        self._sku = sku
        self._updated = updated
        self._id = id

    @classmethod
    def from_dict(cls, dikt):
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PartOffer of this PartOffer.
        :rtype: PartOffer
        """
        return deserialize_model(dikt, cls)

    @property
    def packaging_unit(self):
        """
        Gets the packaging_unit of this PartOffer.

        :return: The packaging_unit of this PartOffer.
        :rtype: int
        """
        return self._packaging_unit

    @packaging_unit.setter
    def packaging_unit(self, packaging_unit):
        """
        Sets the packaging_unit of this PartOffer.

        :param packaging_unit: The packaging_unit of this PartOffer.
        :type packaging_unit: int
        """

        self._packaging_unit = packaging_unit

    @property
    def quantity(self):
        """
        Gets the quantity of this PartOffer.

        :return: The quantity of this PartOffer.
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """
        Sets the quantity of this PartOffer.

        :param quantity: The quantity of this PartOffer.
        :type quantity: int
        """

        self._quantity = quantity

    @property
    def min_order_quantity(self):
        """
        Gets the min_order_quantity of this PartOffer.

        :return: The min_order_quantity of this PartOffer.
        :rtype: int
        """
        return self._min_order_quantity

    @min_order_quantity.setter
    def min_order_quantity(self, min_order_quantity):
        """
        Sets the min_order_quantity of this PartOffer.

        :param min_order_quantity: The min_order_quantity of this PartOffer.
        :type min_order_quantity: int
        """

        self._min_order_quantity = min_order_quantity

    @property
    def unit_price(self):
        """
        Gets the unit_price of this PartOffer.

        :return: The unit_price of this PartOffer.
        :rtype: float
        """
        return self._unit_price

    @unit_price.setter
    def unit_price(self, unit_price):
        """
        Sets the unit_price of this PartOffer.

        :param unit_price: The unit_price of this PartOffer.
        :type unit_price: float
        """

        self._unit_price = unit_price

    @property
    def available_stock(self):
        """
        Gets the available_stock of this PartOffer.

        :return: The available_stock of this PartOffer.
        :rtype: int
        """
        return self._available_stock

    @available_stock.setter
    def available_stock(self, available_stock):
        """
        Sets the available_stock of this PartOffer.

        :param available_stock: The available_stock of this PartOffer.
        :type available_stock: int
        """

        self._available_stock = available_stock

    @property
    def packaging(self):
        """
        Gets the packaging of this PartOffer.

        :return: The packaging of this PartOffer.
        :rtype: str
        """
        return self._packaging

    @packaging.setter
    def packaging(self, packaging):
        """
        Sets the packaging of this PartOffer.

        :param packaging: The packaging of this PartOffer.
        :type packaging: str
        """

        self._packaging = packaging

    @property
    def currency(self):
        """
        Gets the currency of this PartOffer.

        :return: The currency of this PartOffer.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """
        Sets the currency of this PartOffer.

        :param currency: The currency of this PartOffer.
        :type currency: str
        """

        self._currency = currency

    @property
    def sku(self):
        """
        Gets the sku of this PartOffer.

        :return: The sku of this PartOffer.
        :rtype: str
        """
        return self._sku

    @sku.setter
    def sku(self, sku):
        """
        Sets the sku of this PartOffer.

        :param sku: The sku of this PartOffer.
        :type sku: str
        """

        self._sku = sku

    @property
    def updated(self):
        """
        Gets the updated of this PartOffer.

        :return: The updated of this PartOffer.
        :rtype: str
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this PartOffer.

        :param updated: The updated of this PartOffer.
        :type updated: str
        """

        self._updated = updated

    @property
    def id(self):
        """
        Gets the id of this PartOffer.

        :return: The id of this PartOffer.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this PartOffer.

        :param id: The id of this PartOffer.
        :type id: int
        """

        self._id = id

