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
    page = 1

    while True:
        query_url = build_query_url(query, page)
        query_soup = query_stack_overflow(query_url)

        if not query_soup:
            break

        post_summaries = get_post_summaries(query_soup)

        if not post_summaries:
            break

        for post_summary in post_summaries:
            soup = post_soup(post_summary)

            if soup:
                yield soup

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
    except:
        return None

    return BeautifulSoup(response.text, 'lxml')


def get_post_summaries(query_soup):
    '''
    TODO: Write docstring.
    '''

    return query_soup.find_all(
        attrs={
            'class': 'question-summary'
        }
    )


def post_soup(post_summary):
    '''
    TODO: Write docstring.
    '''

    if has_accepted_answer(post_summary):
        post_url = get_post_url(post_summary)

        try:
            response = requests.get(BASE_URL + post_href)
        except:
            return None
        
        post_soup = BeautifulSoup(response.text, 'lxml')

        return post_soup
    
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
    except:
        return None


def print_accepted_post(post):
    '''
    Prints a Stack Overflow post with an accepted answer.

    Parameter {BeautifulSoup} post: The 'soup' of the post
    to print.
    '''

    question = None
    try:
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
    except AttributeError:
        return
    finally:
        if not question:
            return

    accepted_answer = None
    try:
        accepted_answer = post.find(
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
    except AttributeError:
        return
    finally:
        if not accepted_answer:
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
    return


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

    for element in post_text:
        if (
            element.name == 'h1' or
            element.name == 'h2' or
            element.name == 'h3'
        ):  # Headers.
            print(
                colored(element.text, 'white', attrs=['bold'])
            )
        elif element.name == 'p':  # Text.
            print(
                colored(element.text, 'white')
            )
        elif element.name == 'blockquote':  # Quotes.
            print(
                colored('    ' + element.text, 'yellow')
            )
        elif element.name == 'ul':  # Lists.
            for item in element.find_all('li'):
                print(
                    colored('    - ' + item.text, 'green', attrs=['bold'])
                )
        elif element.name == 'pre':  # Code.
            print_code_block(element.find('code'))


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

    print('')

    # Store the code's text.
    code = ''

    # Loop through code spans.
    for token in code_block:
        # Catch when spans are wrapped with other tags.
        try:
            code += token
        except TypeError:
            for nestedToken in token.contents:
                code += nestedToken

    # Loop over code, and highlight.
    for token, content in pygments.lex(code, PythonLexer()):
        if str(token) == 'Token.Keyword':
            print(
                colored(content, 'blue'),
                end=''
            )
        elif str(token) == 'Token.Name.Builtin.Pseudo':
            print(
                colored(content, 'blue'),
                end=''
            )
        elif str(token) == 'Token.Literal.Number.Integer':
            print(
                colored(content, 'green'),
                end=''
            )
        elif str(token) == 'Token.Literal.Number.Float':
            print(
                colored(content, 'green'),
                end=''
            )
        elif str(token) == 'Token.Literal.String.Single':
            print(
                colored(content, 'yellow'),
                end=''
            )
        elif str(token) == 'Token.Literal.String.Double':
            print(
                colored(content, 'yellow'),
                end=''
            )
        elif str(token) == 'Token.Literal.String.Doc':
            print(
                colored(content, 'yellow'),
                end=''
            )
        elif str(token) == 'Token.Comment.Single':
            print(
                colored(content, 'green'),
                end=''
            )
        elif str(token) == 'Token.Comment.Hashbang':
            print(
                colored(content, 'green'),
                end=''
            )
        else:
            print(
                content,
                end=''
            )

    print('')
