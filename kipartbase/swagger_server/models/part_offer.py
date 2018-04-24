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
    def __init__(self, packaging_unit=None, quantity=None, unit_price=None, currency=None, sku=None, updated=None):
        """
        PartOffer - a model defined in Swagger

        :param packaging_unit: The packaging_unit of this PartOffer.
        :type packaging_unit: int
        :param quantity: The quantity of this PartOffer.
        :type quantity: int
        :param unit_price: The unit_price of this PartOffer.
        :type unit_price: float
        :param currency: The currency of this PartOffer.
        :type currency: str
        :param sku: The sku of this PartOffer.
        :type sku: str
        :param updated: The updated of this PartOffer.
        :type updated: str
        """
        self.swagger_types = {
            'packaging_unit': int,
            'quantity': int,
            'unit_price': float,
            'currency': str,
            'sku': str,
            'updated': str
        }

        self.attribute_map = {
            'packaging_unit': 'packaging_unit',
            'quantity': 'quantity',
            'unit_price': 'unit_price',
            'currency': 'currency',
            'sku': 'sku',
            'updated': 'updated'
        }

        self._packaging_unit = packaging_unit
        self._quantity = quantity
        self._unit_price = unit_price
        self._currency = currency
        self._sku = sku
        self._updated = updated

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

