'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/06/2020
Overview: Used to print Stack Overflow posts.
'''

from __future__ import (
    absolute_import,
    division,
    print_function
)

import pygments
from pygments.lexers import PythonLexer  # pylint: disable=no-name-in-module
from termcolor import colored

from autostack.so_web_scraper.scrape import (
    get_post_comments,
    get_post_text,
    get_src_code
)


def print_post(post, config):
    '''
    Prints a Stack Overflow post with an answer.

    Parameter {bs4.BeautifulSoup} post: The 'soup' of the post
    to print.
    Parameter {dictionary} config: configuration object.
    '''

    question = None
    question_comments = None
    answer = None
    answer_comments = None

    # Grab the question and answer.
    question = get_post_text(post, 'question')
    answer = get_post_text(post, 'answer')

    # Grab the comments, if applicable.
    if config['display_comments']:
        question_comments = get_post_comments(post, 'question', config['max_comments'])
        answer_comments = get_post_comments(post, 'answer', config['max_comments'])

    # If the question or answer could not be grabbed, return.
    if question is None or answer is None:
        return

    print(colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red'))
    print(colored('Question:', 'red'))

    # Print the question.
    print_post_text(question)

    # Print the question comments, if applicable.
    if question_comments:
        print(colored('\nComments:', 'red'))
        print_post_comments(question_comments)

    print(colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red'))
    print(colored('Answer:', 'red'))

    # Print the answer.
    print_post_text(answer)

    # Print the answer comments, if applicable.
    if answer_comments:
        print(colored('\nComments:', 'red'))
        print_post_comments(answer_comments)

    print(colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red'))


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

    
def print_post_comments(comments):
    '''
    TODO
    '''

    for comment in comments:
        try:
            text = comment.find(
                attrs={
                    'class': 'comment-copy'
                }
            ).get_text()
            print(text)
        except AttributeError:
            pass


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
