'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/25/2019
Overview: Tests for the so_web_scraper package.
'''

from bs4 import BeautifulSoup

from autostack.so_web_scraper import (
    accepted_posts,
    get_post_summaries,
    build_query_url,
    query_stack_overflow,
    post_soup,
    # has_accepted_answer,
    # get_post_url,
    # print_accepted_post,
    # get_post_text,
    # print_post_text,
    # print_ul,
    # print_code_block,
    # get_src_code,
)
from autostack.so_web_scraper.__tests__.mock_response import (
    MockResponse,
    build_mock_get
)


def test_accepted_posts(monkeypatch):
    '''
    Ensures that accepted_posts loops over each post summary.
    '''

    # 1. Given.
    post_soup_call_count = 0

    def mock_get_post_summaries(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_summaries function
        '''

        html = open(
            'autostack/so_web_scraper/__tests__/data/query_post_summaries.html'
        ).read()

        post_summaries = BeautifulSoup(html, 'lxml').find_all(
            attrs={
                'class': 'question-summary'
            }
        )

        return [post_summaries]

    def mock_post_soup(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the post_soup function
        '''
        nonlocal post_soup_call_count
        post_soup_call_count += 1
        return 'SOUP'

    monkeypatch.setattr(
        'autostack.so_web_scraper.get_post_summaries',
        mock_get_post_summaries
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.post_soup',
        mock_post_soup
    )

    # 2. When.
    # pylint: disable=unused-variable
    for post in accepted_posts(None):
        pass

    # 3. Then.
    assert post_soup_call_count == 15


def test_get_post_summaries(monkeypatch):
    '''
    Ensures that the generator yields post summaries until
    there aren't anymore post summaries.
    '''

    # 1. Given.
    query_stack_overflow_call_count = 0

    def mock_build_query_url(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the build_query_url function.
        '''

        return

    def mock_query_stack_overflow(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the query_stack_overflow function.
        '''

        nonlocal query_stack_overflow_call_count
        query_stack_overflow_call_count += 1

        base = 'autostack/so_web_scraper/__tests__/data/'

        if query_stack_overflow_call_count == 3:
            return BeautifulSoup(open(
                base + 'query_no_post_summaries.html'
            ).read(), 'lxml')

        return BeautifulSoup(open(
            base + 'query_post_summaries.html'
        ).read(), 'lxml')

    monkeypatch.setattr(
        'autostack.so_web_scraper.build_query_url',
        mock_build_query_url
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.query_stack_overflow',
        mock_query_stack_overflow
    )

    # 2. When.
    # pylint: disable=unused-variable
    for post_summaries in get_post_summaries(None):
        pass

    # 3. Then.
    assert query_stack_overflow_call_count == 3


def test_get_post_summaries_no_query_soup(monkeypatch):
    '''
    Ensures that the generator yields nothing when there's
    no BeautifulSoup returned from querying Stack Overflow.
    '''

    # 1. Given.
    def mock_build_query_url(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the build_query_url function.
        '''

        return

    def mock_query_stack_overflow(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the query_stack_overflow function.
        '''

        return None

    monkeypatch.setattr(
        'autostack.so_web_scraper.build_query_url',
        mock_build_query_url
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.query_stack_overflow',
        mock_query_stack_overflow
    )

    # 2. When.
    post_count = 0

    # pylint: disable=unused-variable
    for post_summaries in get_post_summaries(None):
        post_count += 1

    # 3. Then.
    assert post_count == 0


def test_build_query_url():
    '''
    Ensures that the proper URL is built with build_query_url.
    '''

    # 1. Given.
    base_url = 'https://stackoverflow.com'
    page = 1
    query = 'Test Query'

    # 2. When.
    url = build_query_url(query, page)

    # 3. Then.
    assert '{}/search?page={}&tab=Relevance&q=%5Bpython%5D+Test+Query'.format(
        base_url,
        page
    ) == url


def test_query_stack_overflow_good_response_status(monkeypatch):
    '''
    Ensures that BeautifulSoup is returned from query_stack_overflow.
    '''

    # 1. Given.
    path = 'autostack/so_web_scraper/__tests__/data/query_post_summaries.html'
    html = open(path).read()
    soup = BeautifulSoup(html, 'lxml')
    mock_response = MockResponse(
        path,
        200
    )
    mock_get = build_mock_get(mock_response)

    monkeypatch.setattr('requests.get', mock_get)

    # 2. When.
    response = query_stack_overflow(None)

    # 3. Then.
    assert response == soup


def test_query_stack_overflow_bad_response_status(monkeypatch):
    '''
    Ensures that BeautifulSoup is returned from query_stack_overflow.
    '''

    # 1. Given.
    mock_response = MockResponse(
        'autostack/so_web_scraper/__tests__/data/query_post_summaries.html',
        400
    )
    mock_get = build_mock_get(mock_response)

    monkeypatch.setattr('requests.get', mock_get)

    # 2. When.
    response = query_stack_overflow(None)

    # 3. Then.
    assert not response


def test_post_soup_no_accepted_answer(monkeypatch):
    '''
    Ensures None is returned when there's no accepted answer.
    '''

    # 1. Given.
    def mock_has_accepted_answer(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the has_accepted_answer function.
        '''

        return False

    monkeypatch.setattr(
        'autostack.so_web_scraper.has_accepted_answer',
        mock_has_accepted_answer
    )

    # 2. When.
    response_soup = post_soup(None)

    # 3. Then.
    assert not response_soup


def test_post_soup_accepted_answer(monkeypatch):
    '''
    Ensures BeautifulSoup is returned when there's an accepted answer.
    '''

    # 1. Given.
    path = 'autostack/so_web_scraper/__tests__/data/post_accepted_answer.html'
    html = open(path).read()
    soup = BeautifulSoup(html, 'lxml')

    def mock_has_accepted_answer(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the has_accepted_answer function.
        '''

        return True

    def mock_get_post_url(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_url function.
        '''

        return ''

    mock_response = MockResponse(
        path,
        200
    )
    mock_get = build_mock_get(mock_response)

    monkeypatch.setattr(
        'autostack.so_web_scraper.has_accepted_answer',
        mock_has_accepted_answer
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.get_post_url',
        mock_get_post_url
    )

    monkeypatch.setattr('requests.get', mock_get)

    # 2. When.
    response_soup = post_soup(None)

    # 3. Then.
    assert response_soup == soup


def test_post_soup_bad_status(monkeypatch):
    '''
    Ensures None is returned when the request status is bad.
    '''

    # 1. Given.
    mock_response = MockResponse(
        'autostack/so_web_scraper/__tests__/data/post_accepted_answer.html',
        400
    )
    mock_get = build_mock_get(mock_response)

    def mock_has_accepted_answer(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the has_accepted_answer function.
        '''

        return True

    def mock_get_post_url(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_url function.
        '''

        return ''

    monkeypatch.setattr(
        'autostack.so_web_scraper.has_accepted_answer',
        mock_has_accepted_answer
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.get_post_url',
        mock_get_post_url
    )

    monkeypatch.setattr('requests.get', mock_get)

    # 2. When.
    response = post_soup(None)

    # 3. Then.
    assert not response
