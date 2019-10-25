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
    # build_query_url,
    # query_stack_overflow,
    # post_soup,
    # has_accepted_answer,
    # get_post_url,
    # print_accepted_post,
    # get_post_text,
    # print_post_text,
    # print_ul,
    # print_code_block,
    # get_src_code,
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

        post_summaries = BeautifulSoup(html, features='lxml').find_all(
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
    there aren't anymore.
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
            ).read(), features='lxml')

        return BeautifulSoup(open(
            base + 'query_post_summaries.html'
        ).read(), features='lxml')

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
