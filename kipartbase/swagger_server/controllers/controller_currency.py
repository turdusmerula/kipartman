import connexion
from swagger_server.models.currency import Currency

from swagger_server.models.error import Error

import api.models


def serialize_Currency(fcurrency, currency=None):
    if currency is None:
        currency = Currency()
    currency.name = fcurrency.name
    currency.symbol = fcurrency.symbol
    currency.base = fcurrency.base
    currency.ratio = fcurrency.ratio
    return currency


def deserialize_Currency(currency, fcurrency=None):
    if fcurrency is None:
        fcurrency = api.models.Currency()
    fcurrency.name = currency.name
    fcurrency.symbol = currency.symbol
    fcurrency.base = currency.base
    fcurrency.ratio = currency.ratio
    return fcurrency

def find_currencies():
    """
    find_currencies
    Get supported currencies

    :rtype: Storage
    """
    currencies = []

    fcurrencies_query = api.models.Currency.objects
        
    for fcurrency in fcurrencies_query.all():
        currencies.append(serialize_Currency(fcurrency))

    return currencies

def update_currencies():
    """
    update_currencies
    Update supperted currencies

    :rtype: Currency
    """
    if connexion.request.is_json:
        currencies = []
        for item in connexion.request.get_json():
            currencies.append(Currency.from_dict(item))
    else:
        return Error(code=1000, message='Missing payload'), 403

    fcurrencies = []
    for currency in currencies:
        fcurrency = deserialize_Currency(currency)
        fcurrencies.append(fcurrency)
        
    api.models.Currency.objects.all().delete()
    api.models.Currency.objects.bulk_create(fcurrencies)
    
    return currencies
