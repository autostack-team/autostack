'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 03/17/2019
Overview: Contains the StackOverflowScraper class which is used to
scrape Stack Overflow for posts with accepted answers for a given query.
'''

from __future__ import print_function
from bs4 import BeautifulSoup
import pygments
from pygments.lexers import PythonLexer  # pylint: disable=no-name-in-module
import requests
from termcolor import colored

BASE_URL = 'https://stackoverflow.com'


def accepted_posts(query):
    '''
    TODO: Write docstring.
    '''

    for result_set in get_post_summaries(query):
        for post_summary in result_set:
            post = post_soup(post_summary)

            if post:
                yield post


def get_post_summaries(query):
    '''
    TODO: Write docstring.
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
    TODO: Write docstring.
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
    TODO: Write docstring.
    '''

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return None

    return BeautifulSoup(response.text, 'lxml')


def post_soup(post_summary):
    '''
    TODO: Write docstring.
    '''

    if has_accepted_answer(post_summary):
        post_url = get_post_url(post_summary)

        try:
            response = requests.get(BASE_URL + post_url)
        except requests.exceptions.HTTPError:
            return None

        return BeautifulSoup(response.text, 'lxml')

    return None


def has_accepted_answer(post_summary):
    '''
    TODO: Write docstring.
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
    TODO: Write docstring.
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

    Parameter {BeautifulSoup} post: The 'soup' of the post
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
    TODO: Write docstring.
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
    Lists: Green.
    Code: Syntax Highlighted in print_code_block().

    Parameter {BeautifulSoup} post_text: 'soup' of a HTML
    'div' element from a Stack Overflow post with class of
    'post-text.'
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
    TODO: Write docstring.
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

    To highlight the syntax, Pygments PythonLexer is used on the
    code that was grabbed from the 'span' elements inside of the
    'code' element.

    Parameter {BeautifulSoup} code_block: 'soup' of a HTML
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
    TODO: Write docstring.
    '''

    code = ''

    # Loop through code spans.
    for token in code_block:
        # Catch when spans are wrapped with other tags.
        try:
            code += token
        except TypeError:
            code += get_nested_src_code(token)

    return code


def get_nested_src_code(token):
    '''
    TODO: Write docstring.
    '''

    return ''.join(token.contents)
