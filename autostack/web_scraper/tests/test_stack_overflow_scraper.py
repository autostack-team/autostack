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

    url = 'https://stackoverflow.com/'

    if args[0] == '{}search?page=1&tab=Relevance&q=+NoAcceptedPosts'.format(url):
        with open('autostack/web_scraper/tests/data/query_one_accepted_post.html', 'r') as html:
            return MockResponse(html.read(), 200)
    elif args[0] == '{}search?page=1&tab=Relevance&q=+OneAcceptedPosts'.format(url):
        with open('autostack/web_scraper/tests/data/query_no_accepted_posts.html', 'r') as html:
            return MockResponse(html.read(), 200)
    elif args[0] == '{}search?page=1&tab=Relevance&q=+MultipleAcceptedPosts'.format(url):
        with open('autostack/web_scraper/tests/data/query_multiple_accepted_posts.html', 'r') as html:
            return MockResponse(html.read(), 200)
    elif 'page=2' in args[0]:
        with open('autostack/web_scraper/tests/data/query_no_posts.html', 'r') as html:
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

# def test_accepted_posts_one_accepted_post_on_query_page():
#     '''
#     This test ensures that one post is returned on a query
#     page with only one accepted post.
#     '''
#     assert True

# def test_accepted_posts_multiple_accepted_posts_on_query_page():
#     '''
#     This test ensures that all posts are returned on a query
#     page with multiple accepted posts.
#     '''
#     assert True

# ======================================================================
# Tests for print_accepted_posts
# ======================================================================

# ======================================================================
# Tests for print_post_text
# ======================================================================

# ======================================================================
# Tests for print_code_block
# ======================================================================