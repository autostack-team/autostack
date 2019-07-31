'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 07/23/2019
Overview: Tests for the Stack Overflow web scraper.
'''

from contextlib import contextmanager
from io import StringIO
import re
import sys
from unittest import mock

import pytest
import requests
from bs4 import BeautifulSoup

from autostack.web_scraper.stack_overflow_scraper import (
    accepted_posts,
    print_accepted_post,
    print_post_text,
    print_code_block,
)


# ======================================================================
# Mock requests
# ======================================================================


def mock_get_request(*args, **kwargs):
    '''
    Mocks request.get function.

    Unit tests are supposed to be self-contained, so unit
    tests should not have to rely on actual HTTP requests.
    '''

    class MockResponse:
        '''
        Mocks the response object from a request.get() method
        call.
        '''

        def __init__(self, text, status_code):
            '''
            Initializes the MockResponse with text and a
            status code.

            Parameter {str} text: The HTML of the response.
            Parameter {int} status_code: The HTTP response
            status code (e.g. 200, 400).
            '''
            self.text = text
            self.status_code = status_code

    data_path = 'autostack/web_scraper/tests/data'

    if 'page=2' in args[0]:
        # When the scraper goes to page 2, return query HTML with no posts.
        with open(
            '{}/query_no_posts.html'.format(data_path),
            'r'
        ) as html:
            return MockResponse(html.read(), 200)
    elif 'questions' in args[0]:
        # Returns post HTML.
        with open(
            '{}/post_accepted_answer.html'.format(data_path),
            'r'
        ) as html:
            return MockResponse(html.read(), 200)
    elif 'q=+NoAcceptedPosts' in args[0]:
        # Returns query HTML with no accepted posts.
        with open(
            '{}/query_no_accepted_posts.html'.format(data_path),
            'r'
        ) as html:
            return MockResponse(html.read(), 200)
    elif 'q=+OneAcceptedPost' in args[0]:
        # Returns query HTML with one accepted post.
        with open(
            '{}/query_one_accepted_post.html'.format(data_path),
            'r'
        ) as html:
            return MockResponse(html.read(), 200)
    elif 'q=+MultipleAcceptedPosts' in args[0]:
        # Returns query HTML with multiple accepted posts.
        with open(
            '{}/query_seven_accepted_posts.html'.format(data_path),
            'r'
        ) as html:
            return MockResponse(html.read(), 200)

requests.get = mock_get_request

# ======================================================================
# Capture stdout and stderr
# ======================================================================


@contextmanager
def captured_output():
    '''
    Captures stdout and stderr by temporarily replacing sys.stdout.
    '''

    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

# ======================================================================
# Remove ANSI characters in output.
# ======================================================================


ANSI_ESCAPE = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')


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


def test_print_accepted_post_no_question():
    '''
    This test ensures that the function returns and doesn't
    print anything, if non-post 'soup' is given as input.
    '''

    # 1. Given.
    with open(
        'autostack/web_scraper/tests/data/query_no_accepted_posts.html',
        'r'
    ) as html:
        soup = BeautifulSoup(html.read(), 'lxml')

        # 2. When.
        with captured_output() as (stdout, stderr):
            print_accepted_post(soup)

        # 3. Then.
        assert not stdout.getvalue().strip()


def test_print_accepted_post_no_answer():
    '''
    This test ensures that the function returns, and doesn't
    print anything, if the post doesn't have an answer.
    '''

    # 1. Given.
    with open(
        'autostack/web_scraper/tests/data/post_no_answer.html',
        'r'
    ) as html:
        soup = BeautifulSoup(html.read(), 'lxml')

        # 2. When.
        with captured_output() as (stdout, stderr):
            print_accepted_post(soup)

        # 3. Then.
        assert not stdout.getvalue().strip()


def test_print_accepted_post_no_accepted_answer():
    '''
    This test ensures that the function returns, and doesn't
    print anything, if the post doesn't have an accepted answer.
    '''

    # 1. Given.
    with open(
        'autostack/web_scraper/tests/data/post_no_accepted_answer.html',
        'r'
    ) as html:
        soup = BeautifulSoup(html.read(), 'lxml')

        # 2. When.
        with captured_output() as (stdout, stderr):
            print_accepted_post(soup)

        # 3. Then.
        assert not stdout.getvalue().strip()


def test_print_accepted_post_accepted_answer():
    '''
    This test ensures that print_accepted_post properly prints a
    post with an accepted answer.
    '''

    # 1. Given.
    with open(
        'autostack/web_scraper/tests/data/post_accepted_answer.html',
        'r'
    ) as html:
        soup = BeautifulSoup(html.read(), 'lxml')

        # 2. When.
        with captured_output() as (stdout, stderr):
            print_accepted_post(soup)

        # 3. Then.
        output = ANSI_ESCAPE.sub('', stdout.getvalue().strip())
        assert 'I am trying to write some Python example\
             code with a line commented out:' in output
        assert 'user_by_email = session.query(User)\\' in output
        assert '.filter(Address.email==\'one\')\\' in output
        assert '#.options(joinedload(User.addresses))\\' in output
        assert '.first()' in output
        assert 'I also tried:' in output
        assert 'user_by_email = session.query(User)\\' in output
        assert '.filter(Address.email==\'one\')\\' in output
        assert '#    .options(joinedload(User.addresses))\\' in output
        assert '.first()' in output
        assert 'But I get IndentationError: unexpected indent.' in output
        assert 'If I remove the commented out line, the code works.' in output
        assert 'I am decently sure that I use only\
             spaces (Notepad++ screenshot):' in output
        assert 'Enclose the statement in paranthesis' in output
        assert 'user_by_email = (session.query(User)' in output
        assert '.filter(Address.email==\'one\')' in output
        assert '#.options(joinedload(User.addresses))' in output
        assert '.first())' in output


# ======================================================================
# Tests for print_post_text
# ======================================================================


def test_print_post_text():
    '''
    This test ensures that print_post_text properly prints a
    post's text.
    '''

    # 1. Given.
    with open(
        'autostack/web_scraper/tests/data/post_accepted_answer.html',
        'r'
    ) as html:
        post = BeautifulSoup(html.read(), 'lxml')

        question = post.find(
            attrs={
                'class',
                'question'
            }
        ).find(
            attrs={
                'class',
                'post-text'
            }
        )

        answer = post.find(
            attrs={
                'class',
                'accepted-answer'
            }
        ).find(
            attrs={
                'class',
                'post-text'
            }
        )

        # 2. When.
        with captured_output() as (stdout, stderr):
            print_post_text(question)
            print_post_text(answer)

        output = ANSI_ESCAPE.sub('', stdout.getvalue().strip())
        assert 'I am trying to write some Python example\
             code with a line commented out:' in output
        assert 'user_by_email = session.query(User)\\' in output
        assert '.filter(Address.email==\'one\')\\' in output
        assert '#.options(joinedload(User.addresses))\\' in output
        assert '.first()' in output
        assert 'I also tried:' in output
        assert 'user_by_email = session.query(User)\\' in output
        assert '.filter(Address.email==\'one\')\\' in output
        assert '#    .options(joinedload(User.addresses))\\' in output
        assert '.first()' in output
        assert 'But I get IndentationError: unexpected indent.' in output
        assert 'If I remove the commented out line, the code works.' in output
        assert 'I am decently sure that I use only\
             spaces (Notepad++ screenshot):' in output
        assert 'Enclose the statement in paranthesis' in output
        assert 'user_by_email = (session.query(User)' in output
        assert '.filter(Address.email==\'one\')' in output
        assert '#.options(joinedload(User.addresses))' in output
        assert '.first())' in output


# ======================================================================
# Tests for print_code_block
# ======================================================================


def test_print_code_block():
    '''
    This test ensures that print_code_block properly prints a
    code block.
    '''

    # 1. Given.
    with open(
        'autostack/web_scraper/tests/data/post_accepted_answer.html',
        'r'
    ) as html:
        code_block = BeautifulSoup(html.read(), 'lxml').find('code')

        # 2. When.
        with captured_output() as (stdout, stderr):
            print_code_block(code_block)

        output = ANSI_ESCAPE.sub('', stdout.getvalue().strip())
        assert 'user_by_email = session.query(User)\\' in output
        assert '.filter(Address.email==\'one\')\\' in output
        assert '#.options(joinedload(User.addresses))\\' in output
        assert '.first()' in output
