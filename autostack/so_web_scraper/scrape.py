'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/06/2020
Overview: Used to scrape Stack Overflow posts using bs4.
'''

from bs4 import BeautifulSoup
import requests

from autostack.so_web_scraper.constants import BASE_URL


def get_post_summaries(query, config):
    '''
    A generator that queries Stack Overflow and yields a ResultSet
    of post summaries.

    Parameter {string} query: the string to query Stack Overflow with.
    Parameter {dictionary} config: configuration object.
    Yields {bs4.element.ResultSet}: ResultSet of post summaries.
    '''

    page = 1

    while True:
        query_url = build_query_url(query, page, config)
        query_soup = query_stack_overflow(query_url)

        if not query_soup:
            break

        post_summaries = query_soup.find_all(
            attrs={
                'class': 'question-summary'
            }
        )

        if not post_summaries:
            break

        yield post_summaries

        page += 1


def build_query_url(query, page, config):
    '''
    Builds a URL to query Stack Overflow with.

    e.g. query == 'Test Query' and page == 1 then the url will be:
    https://stackoverflow.com/search?page=1&tab=Relevance&q=%5Bpython%5D+Test+Query

    Parameter {string} query: the string to query Stack Overflow with.
    Parameter {int} page: the page to select in the query.
    Parameter {dictionary} config: configuration object.
    Returns {string} the query URL.
    '''

    query_url = '{}/search?page={}&tab=Relevance&q=%5Bpython%5D'.format(
        BASE_URL,
        page
    )

    for query_string in query.split(' '):
        query_url = '{}+{}'.format(query_url, query_string)

    return query_url


def query_stack_overflow(url):
    '''
    Given a url, this function returns the BeautifulSoup of the
    request.

    Parameter {string} url: the url to request.
    Returns {bs4.BeautifulSoup} the BeautifulSoup of the request.
    '''

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return None

    return BeautifulSoup(response.text, 'lxml')


def post_soup(post_summary, config):
    '''
    Given a post summary, query Stack Overflow, and return the
    BeautifulSoup of the post, if it has an accepted answer.

    Parameter {bs4.Tag} post_summary: the bs4.Tag post summary.
    Parameter {dictionary} config: configuration object.
    Returns {bs4.BeautifulSoup} the BeautifulSoup of the post,
    if it has an accepted answer; otherwise, None.
    '''

    if has_accepted_answer(post_summary):
        post_url = get_post_url(post_summary)

        try:
            response = requests.get(BASE_URL + post_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return None

        return BeautifulSoup(response.text, 'lxml')

    return None


def has_accepted_answer(post_summary):
    '''
    Given a post summary, this function determines whether or not
    the post has an accepted answer.

    Parameter {bs4.Tag} post_summary: the post summary.
    Returns {boolean} True if the post has an accepted answer;
    otherwise, False.
    '''

    accepted_answer = post_summary.find(
        attrs={
            'class': 'answered-accepted'
        }
    )

    if not accepted_answer:
        return False

    return True


def get_post_url(post_summary):
    '''
    Given a post summary, this function returns the post's url.

    Parameter {bs4.Tag} post_summary: the post summary.
    Returns {str:None} post url, or None, if the post url couldn't
    be found.
    '''

    try:
        return post_summary.find(
            attrs={
                'class': 'question-hyperlink'
            },
            href=True
        )['href']
    except KeyError:
        return None


def get_post_text(post, html_class):
    '''
    Given a post, and a html class, this function returns a
    bs4.Tag with the post-text.
    Typically, you'd only pass 'question' or 'accepted-answer' as
    the html class.

    Parameter {bs4.BeautifulSoup} post: the post to get post-text from.
    Parameter {str} html_class: the html class of the elementto get
    post-text from.
    Returns {bs4.Tag} the post-text.
    '''

    try:
        return post.find(
            attrs={
                'class',
                html_class
            }
        ).find(
            attrs={
                'class',
                'post-text'
            }
        )
    except AttributeError:
        return None


def get_src_code(code_block):
    '''
    Loops over a code block and grabs the 'source code'
    (i.e. text).

    Parameter {bs4.Tag} code_block: the source code (or text).
    Returns {str}: the source code (or text).
    '''

    code = ''

    # Loop through code spans.
    for token in code_block:
        try:  # bs4.NavigableString
            code += token
        except TypeError:  # bs4.Tag
            code += get_src_code(token.contents)

    return code
