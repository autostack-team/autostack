'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/09/2019
Overview: TODO: Write overview.
'''

from __future__ import print_function
from builtins import input

from autostack.so_web_scraper import (
    accepted_posts,
    print_accepted_post
)

SYNTAX_ERRORS = [
    'SyntaxError',
    'IndentationError',
    'TabError',
]


def listen_for_errors(pipe):
    '''
    TODO: Write docstring.
    '''

    print_listening_for_errors()

    # Listen for new stdout.
    while True:
        # Read a line from the pipe.
        output = pipe.readline()

        # Pipe closed.
        if output == '':
            break

        parse_output_for_error(output, pipe)


def parse_output_for_error(output, pipe):
    '''
    TODO: Write docstring.
    '''

    try:
        # Syntax errors - no traceback.
        if output.split()[0][:-1] in SYNTAX_ERRORS:
            error = output.split()[0]
            handle_exception(error)
        # Runtime error - has traceback.
        elif 'Traceback' in output.split():
            error = get_error_from_traceback(pipe)
            handle_exception(error)
    except IndexError:
        pass


def get_error_from_traceback(pipe):
    '''
    TODO: Write docstring.
    '''

    output = pipe.readline()

    while (
            output.split()[0][-1] != ':'
    ):
        output = pipe.readline()

    return output.split()[0]


def handle_exception(exception):
    '''
    TODO: Write docstring.
    '''

    for post in accepted_posts(exception[:-1]):
        # Display Stack Overflow posts for the error.
        print_accepted_post(post)

        error_is_solved = error_solved()

        if error_is_solved:
            print_listening_for_errors()
            break


def error_solved():
    '''
    TODO: Write docstring.
    '''

    is_error_solved = False

    while True:
        print('Did this solve your error? (Y/n): ', end='')
        is_error_solved = input()

        if is_error_solved not in ('Y', 'n'):
            print(
                '{} is not valid input! Please try again.'.format(
                    is_error_solved
                )
            )
        else:
            break

    if is_error_solved == 'n':
        return False

    return True


def print_listening_for_errors():
    '''
    Prints "🥞 Listening for Python errors..."
    '''

    print(u'\U0001F95E Listening for Python errors...')
