'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 03/17/2019
Overview: Contains the StackOverflowScraper class which is used to
scrape Stack Overflow for posts with accepted answers for a given query.
'''

from __future__ import absolute_import, division, print_function
from bs4 import BeautifulSoup
import pygments
from pygments.lexers import PythonLexer  # pylint: disable=no-name-in-module
import requests
from termcolor import colored

BASE_URL = 'https://stackoverflow.com'


def accepted_posts(query):
    '''
    A generator that queries Stack Overflow and yields posts with
    accepted answers.

    Parameter {str} query: the string to query Stack Overflow with.
    Yields {bs4.BeautifulSoup}: accepted posts html documents.
    '''

    for result_set in get_post_summaries(query):
        for post_summary in result_set:
            post = post_soup(post_summary)

            if post:
                yield post


def get_post_summaries(query):
    '''
    A generator that queries Stack Overflow and yields a ResultSet
    of post summaries.

    Parameter {str} query: the string to query Stack Overflow with.
    Yields {bs4.element.ResultSet}: ResultSet of post summaries.
    '''

    page = 1

    while True:
        query_url = build_query_url(query, page)
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


def build_query_url(query, page):
    '''
    Builds a URL to query Stack Overflow with.

    e.g. query == 'Test Query' and page == 1 then the url will be:
    https://stackoverflow.com/search?page=1&tab=Relevance&q=%5Bpython%5D+Test+Query

    Parameter {str} query: the string to query Stack Overflow with.
    Parameter {int} page: the page to select in the query.
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

    Parameter {str} url: the url to request.
    Returns {bs4.BeautifulSoup}: the BeautifulSoup of the request.
    '''

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return None

    return BeautifulSoup(response.text, 'lxml')


def post_soup(post_summary):
    '''
    Given a post summary, query Stack Overflow, and return the
    BeautifulSoup of the post, if it has an accepted answer.

    Parameter {bs4.Tag} post_summary: the bs4.Tag post summary.
    Parameter {bs4.BeautifulSoup}: the BeautifulSoup of the post,
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
    Returns {Boolean}: True if the post has an accepted answer;
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
    Returns {str:None}: post url, or None, if the post url couldn't
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


def print_accepted_post(post):
    '''
    Prints a Stack Overflow post with an accepted answer.

    Parameter {bs4.BeautifulSoup} post: The 'soup' of the post
    to print.
    '''

    question = get_post_text(post, 'question')
    accepted_answer = get_post_text(post, 'accepted-answer')

    if question is None or accepted_answer is None:
        return

    print(colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red'))
    print(colored('Question:', 'red'))

    # Print the question.
    print_post_text(question)

    print(colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red'))
    print(colored('Answer:', 'red'))

    # Print the answer.
    print_post_text(accepted_answer)

    print(colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red'))


def get_post_text(post, html_class):
    '''
    Given a post, and a html class, this function returns a
    bs4.Tag with the post-text.
    Typically, you'd only pass 'question' or 'accepted-answer' as
    the html class.

    Parameter {bs4.BeautifulSoup} post: the post to get post-text from.
    Parameter {str} html_class: the html class of the elementto get
    post-text from.
    Returns {bs4.Tag}: the post-text.
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


def print_post_text(post_text):
    '''
    Prints post-text from Stack Overflow.

    On Stack Overflow, a div with a class of 'post-text'
    indicates that the div is either a question or an answer.

    Different elements of the post-text are printed in different
    colors.

    Headers: White.
    Text: White.
    Quotes: Yellow.
    Lists: Syntax Highlighted in print_ul.
    Code: Syntax Highlighted in print_code_block.

    Parameter {bs4.Tag} post_text: HTML 'div' element from a Stack Overflow
    post with class of 'post-text.'
    '''

    element_colors = {
        'h1': 'white',
        'h2': 'white',
        'h3': 'white',
        'p': 'white',
        'blockquote': 'yellow',
    }

    for element in post_text:
        if element.name in element_colors.keys():
            print(
                colored(element.text, element_colors[element.name])
            )
        elif element.name == 'ul':  # Lists.
            print_ul(element)
        elif element.name == 'pre':  # Code.
            print_code_block(element.find('code'))


def print_ul(ul_element):
    '''
    Prints an unordered list.

    Parameter {bs4.Tag} ul_element: the unordered list to print.
    '''

    for item in ul_element.find_all('li'):
        print(
            colored('    - ' + item.text, 'green', attrs=['bold'])
        )


def print_code_block(code_block):
    '''
    Prints a code block from Stack Overflow with syntax highlighting.

    On Stack Overflow, the code in a HTML 'code' element contains
    a 'span' element for each token. Because of this, it's necessary
    to grab each of the 'code' element's 'span' elements' values to get
    the actual code.

    Parameter {bs4.Tag} code_block: 'soup' of a HTML
    'code' element from a Stack Overflow post.
    '''

    token_colors = {
        'Token.Keyword': 'blue',
        'Token.Name.Builtin.Pseudo': 'blue',
        'Token.Literal.Number.Integer': 'green',
        'Token.Literal.Number.Float': 'green',
        'Token.Comment.Single': 'green',
        'Token.Comment.Hashbang': 'green',
        'Token.Literal.String.Single': 'yellow',
        'Token.Literal.String.Double': 'yellow',
        'Token.Literal.String.Doc': 'yellow'
    }

    print('')

    # Store the code's text.
    code = get_src_code(code_block)

    # Loop over code, and highlight.
    for token, content in pygments.lex(code, PythonLexer()):
        try:
            print(
                colored(content, token_colors[str(token)]),
                end=''
            )
        except KeyError:
            print(
                content,
                end=''
            )

    print('')


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
