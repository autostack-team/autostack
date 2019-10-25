'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/25/2019
Overview: Mocks the request package.
'''

import requests


class MockResponse:
    '''
    A mock requests Response object.
    '''

    def __init__(self, path_to_html, status):
        '''
        Initializes a mock response with html text and a
        HTTP status.
        '''

        self.text = open(path_to_html).read()
        self.status = status

    def raise_for_status(self):
        '''
        Raises an requests.exceptions.HTTPError if the HTTP
        status is not within 200-399.
        '''

        if self.status < 200 or self.status > 399:
            raise requests.exceptions.HTTPError

    def get_text(self):
        '''
        Getter for text.
        '''

        return self.text

    def get_status(self):
        '''
        Getter for status.
        '''

        return self.status


def build_mock_get(mock_response):
    '''
    Builds a mock requests get method.
    '''

    def mock_get(*args):
        # pylint: disable=unused-argument
        '''
        Mocks requests get method.

        Returns {MockResponse}: a mock response.
        '''

        nonlocal mock_response
        return mock_response

    return mock_get
