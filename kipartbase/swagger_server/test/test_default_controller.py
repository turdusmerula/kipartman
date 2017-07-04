# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.inline_response200 import InlineResponse200
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestDefaultController(BaseTestCase):
    """ DefaultController integration test stubs """

    def test_persons_get(self):
        """
        Test case for persons_get

        Gets some persons
        """
        response = self.client.open('/openapi101/persons',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
