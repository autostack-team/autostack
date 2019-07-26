'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 07/23/2019
Overview: Tests for the Stack Overflow web scraper.
'''

import pytest
import requests
from autostack.web_scraper.stack_overflow_scraper import (
    accepted_posts,
    print_accepted_post,
    print_post_text,
    print_code_block,
)
from unittest import mock

# ======================================================================
# Mock requests
# ======================================================================


def mock_get_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

    if 'page=2' in args[0]:
        # When the scraper goes to page 2, return query HTML with no posts.
        with open(
            'autostack/web_scraper/tests/data/query_no_posts.html',
            'r'
        ) as html:
            return MockResponse(html.read(), 200)
    elif 'questions' in args[0]:
        # Returns post HTML.
        with open(
            'autostack/web_scraper/tests/data/post.html',
            'r'
        ) as html:
            return MockResponse(html.read(), 200)
    elif 'q=+NoAcceptedPosts' in args[0]:
        # Returns query HTML with no accepted posts.
        with open(
            'autostack/web_scraper/tests/data/query_no_accepted_posts.html',
            'r'
        ) as html:
            return MockResponse(html.read(), 200)
    elif 'q=+OneAcceptedPost' in args[0]:
        # Returns query HTML with one accepted post.
        with open(
            'autostack/web_scraper/tests/data/query_one_accepted_post.html',
            'r'
        ) as html:
            return MockResponse(html.read(), 200)
    elif 'q=+MultipleAcceptedPosts' in args[0]:
        # Returns query HTML with multiple accepted posts.
        with open(
            'autostack/web_scraper/tests/data/query_seven_accepted_posts.html',
            'r'
        ) as html:
            return MockResponse(html.read(), 200)

requests.get = mock_get_request

# ======================================================================
# Tests for accepted_posts
# ======================================================================


def test_accepted_posts_no_accepted_posts_on_query_page():
    '''
    This test ensures that no posts are returned on a query
    page with no accepted posts.
    '''

    # 1. Given.
    post_count = 0

    # 2. When.
    for post in accepted_posts('NoAcceptedPosts'):
        post_count += 1

    # 3. Then.
    assert post_count == 0


def test_accepted_posts_one_accepted_post_on_query_page():
    '''
    This test ensures that one post is returned on a query
    page with only one accepted post.
    '''

    # 1. Given.
    post_count = 0

    # 2. When.
    for post in accepted_posts('OneAcceptedPost'):
        post_count += 1

    # 3. Then.
    assert post_count == 1


def test_accepted_posts_multiple_accepted_posts_on_query_page():
    '''
    This test ensures that all posts are returned on a query
    page with multiple accepted posts.

    Note: the test data for multiple accepted posts has
    seven accepted posts.
    '''

    # 1. Given.
    post_count = 0

    # 2. When.
    for post in accepted_posts('MultipleAcceptedPosts'):
        post_count += 1

    # 3. Then.
    assert post_count == 7

# ======================================================================
# Tests for print_accepted_posts
# ======================================================================


def test_print_accepted_posts_placeholder():
    assert True

# ======================================================================
# Tests for print_post_text
# ======================================================================


def test_print_post_text_placeholder():
    assert True

# ======================================================================
# Tests for print_code_block
# ======================================================================


def test_print_code_block_placeholder():
    assert True
