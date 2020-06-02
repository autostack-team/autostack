'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/31/2020
Overview: Tests for the so_web_scraper scrape module.
'''

import requests

from autostack.so_web_scraper.scrape import (
    get_post_summaries,
    build_query_url,
    query_stack_overflow
)


class MockResponse:
    # pylint: disable=too-few-public-methods
    '''
    A mock requests Response object.
    '''

    def __init__(self, status):
        '''
        Inits a mock response object.
        '''

        self.text = '<html></html>'
        self.status = status

    def raise_for_status(self):
        '''
        Mock raise_for_status method.
        '''

        if self.status < 200 or self.status > 399:
            raise requests.exceptions.HTTPError


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


class MockSoup():
    # pylint: disable=too-few-public-methods
    '''
    Mocks bs4 soup.
    '''

    def __init__(self, return_object=None):
        '''
        Inits a mock bs4 soup object.
        '''

        self.return_object = return_object

    def find_all(self, *args, **kwargs):
        # pylint: disable=unused-argument
        '''
        Mocks the find_all method of bs4 soup.
        '''

        return self.return_object


def test_get_post_summaries_http_error(monkeypatch):
    '''
    Ensures that get_post_summaries handles no soup
    being returned from the query, i.e. an http error.
    '''

    # 1. Given.
    post_count = 0

    def mock_build_query_url(*args):
        # pylint: disable=unused-argument
        '''
        Mocks build_query_url method.
        '''

        return 'url'

    def mock_query_stack_overflow(*args):
        # pylint: disable=unused-argument
        '''
        Mocks query_stack_overflow method.
        '''

        return None

    monkeypatch.setattr(
        'autostack.so_web_scraper.scrape.build_query_url',
        mock_build_query_url
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.scrape.query_stack_overflow',
        mock_query_stack_overflow
    )

    # 2. When.
    # pylint: disable=unused-variable
    for post in get_post_summaries('', {}):
        post_count += 1

    # 3. Then.
    assert not post_count


def test_get_post_summaries_no_post_summaries(monkeypatch):
    '''
    Ensures that get_post_summaries handles no post summaries
    being found in the query soup.
    '''

    # 1. Given.
    post_count = 0

    def mock_build_query_url(*args):
        # pylint: disable=unused-argument
        '''
        Mocks build_query_url method.
        '''

        return 'url'

    def mock_query_stack_overflow(*args):
        # pylint: disable=unused-argument
        '''
        Mocks query_stack_overflow method.
        '''

        return MockSoup()

    monkeypatch.setattr(
        'autostack.so_web_scraper.scrape.build_query_url',
        mock_build_query_url
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.scrape.query_stack_overflow',
        mock_query_stack_overflow
    )

    # 2. When.
    # pylint: disable=unused-variable
    for post in get_post_summaries('', {}):
        post_count += 1

    # 3. Then.
    assert not post_count


def test_get_post_summaries_with_post_summaries(monkeypatch):
    '''
    Ensures that get_post_summaries returns the correct number
    of posts summaries.
    '''

    # 1. Given.
    post_count = 0

    def mock_build_query_url(*args):
        # pylint: disable=unused-argument
        '''
        Mocks build_query_url method.
        '''

        return 'url'

    def mock_query_stack_overflow_wrapper():
        '''
        Wrapper for mock_query_stack_overflow method.
        '''

        call_count = 0

        def mock_query_stack_overflow(*args):
            # pylint: disable=unused-argument
            '''
            Mocks query_stack_overflow method.
            '''

            nonlocal call_count
            call_count += 1

            if call_count in (1, 2):
                return MockSoup([1, 2, 3, 4, 5])

            return None

        return mock_query_stack_overflow

    monkeypatch.setattr(
        'autostack.so_web_scraper.scrape.build_query_url',
        mock_build_query_url
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.scrape.query_stack_overflow',
        mock_query_stack_overflow_wrapper()
    )

    # 2. When.
    # pylint: disable=unused-variable
    for posts in get_post_summaries('', {}):
        for post in posts:
            post_count += 1

    # 3. Then.
    assert post_count == 10


def test_build_query_url():
    '''
    Ensures that build_query_url builds a valid url.
    '''

    # 1. Given.
    config = {
        'language': 'python',
        'order_by': 'Relevance'
    }
    page = 1
    query = 'Test Query'

    # 2. When.
    url = build_query_url(query, page, config)

    # 3. Then.
    assert url == (
        'https://stackoverflow.com/search?page=1&tab=Relevance'
        '&q=%5Bpython%5D+Test+Query'
    )


def test_query_stack_overflow_http_error(monkeypatch):
    '''
    Ensures that query_stack_overflow handles http errors.
    '''

    # 1. Given.
    def mock_get(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get method in the request module.
        '''

        return MockResponse(400)

    monkeypatch.setattr(
        'autostack.so_web_scraper.scrape.requests.get',
        mock_get
    )

    # 2. When.
    result = query_stack_overflow('')

    # 3. Then.
    assert not result


def test_query_stack_overflow_no_http_error(monkeypatch):
    '''
    Ensures that query_stack_overflow returns bs4 soup.
    '''

    # 1. Given.
    def mock_get(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get method in the request module.
        '''

        return MockResponse(200)

    monkeypatch.setattr(
        'autostack.so_web_scraper.scrape.requests.get',
        mock_get
    )

    # 2. When.
    result = query_stack_overflow('')

    # 3. Then.
    assert result
