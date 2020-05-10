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
    Yields {bs4.element.ResultSet} ResultSet of post summaries.
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

    Given the configuration object orders by relevance and has python as the language,
    and query == 'Test Query' and page == 1 then the url will be:
    https://stackoverflow.com/search?page=1&tab=Relevance&q=%5Bpython%5D+Test+Query

    Parameter {string} query: the string to query Stack Overflow with.
    Parameter {int} page: the page to select in the query.
    Parameter {dictionary} config: configuration object.
    Returns {string} the query URL.
    '''

    query_url = '{}/search?page={}&tab={}&q=%5B{}%5D'.format(
        BASE_URL,
        page,
        config['order_by'],
        config['language']
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
    Given a post summary, query Stack Overflow, and return the BeautifulSoup
    of the post, if it has an answer (or accepted answer).

    Parameter {bs4.Tag} post_summary: the bs4.Tag post summary.
    Parameter {dictionary} config: configuration object.
    Returns {bs4.BeautifulSoup} the BeautifulSoup of the post.
    '''

    if has_answer(post_summary, config['verified_only']):
        post_url = get_post_url(post_summary)

        try:
            response = requests.get(BASE_URL + post_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return None

        return BeautifulSoup(response.text, 'lxml')

    return None


def has_answer(post_summary, accepted):
    '''
    Given a post summary, this function determines whether or not the
    post has an answer (or accepted answer).

    Parameter {bs4.Tag} post_summary: the post summary.
    Parameter {boolean} accepted: whether or not the post should check for
    an accepted answer.
    Returns {boolean} True if the post has an answer, or accepted answer;
    otherwise, False.
    '''

    answer = post_summary.find(
        attrs={
            'class': 'answered-accepted'
        }
    )

    if not answer and not accepted:
        answer = post_summary.find(
            attrs={
                'class': 'answered'
            }
        )

    if not answer:
        return False

    return True


def get_post_url(post_summary):
    '''
    Given a post summary, this function returns the post's url.

    Parameter {bs4.Tag} post_summary: the post summary.
    Returns {str|None} post url, or None, if the post url couldn't
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


def get_post_text(post, class_):
    '''
    Given a post, and a html class, this function returns a
    bs4.Tag with the post-text, question or answer.

    You'd only want to pass 'question', 'answer', or 'accepted-answer'
    as the class_.

    Parameter {bs4.BeautifulSoup} post: the post to get post-text from.
    Parameter {str} class_: the html class of the element to get
    post-text from.
    Returns {bs4.Tag} the post-text.
    '''

    try:
        return post.find(
            attrs={
                'class',
                class_
            }
        ).find(
            attrs={
                'class',
                'post-text'
            }
        )
    except AttributeError:
        return None


def get_post_comments(post, class_, limit):
    '''
    Given a post, and a html class, this function returns a bs4.element.ResultSet
    with bs4.Tag objects with the question or answer's comments.

    You'd only want to pass 'question', 'answer', or 'accepted-answer'
    as the class_.

    Parameter {bs4.BeautifulSoup} post: the post to get comments from.
    Parameter {str} class_: the html class of the element to get
    comments from.
    Parameter {int} limit: max comments to get.
    Returns {bs4.element.ResultSet} a ResultSet of comments.
    '''

    try:
        return post.find(
            attrs={
                'class',
                class_
            }
        ).find_all(
            attrs={
                'class',
                'comment-body'
            },
            limit=limit
        )
    except AttributeError:
        return None


def get_src_code(code_block):
    '''
    Loops over a code block and grabs the 'source code'
    (i.e. text).

    Parameter {bs4.Tag} code_block: the source code.
    Returns {string}: the source code.
    '''

    code = ''

    # Loop through code spans.
    for token in code_block:
        try:  # bs4.NavigableString
            code += token
        except TypeError:  # bs4.Tag
            code += get_src_code(token.contents)

    return code
