import connexion
from swagger_server.models.currency import Currency

from swagger_server.models.error import Error

import api.models
import datetime


def get_date():
    """
    get_date
    Get server current datetime

    :rtype: datetime
    """
    return datetime.datetime.now()
