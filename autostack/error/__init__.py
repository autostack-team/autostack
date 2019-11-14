'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/09/2019
Overview: TODO: Write overview.
'''

from __future__ import absolute_import, division, print_function

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
    Reads output from a pipe until EOF, indicated by empty string. The
    output is parsed for errors.

    Parameter {File}: the pipe to read output from.
    '''

    print_listening_for_errors()

    while True:
        output = pipe.readline()

        # Pipe closed.
        if output == '':
            break

        parse_output_for_error(output, pipe)


def parse_output_for_error(output, pipe):
    '''
    Parses a line of output, and determines whether or not it is
    an error message. There are two types of errors, syntax errors
    and runtime errors. Syntax errors do not have a traceback but
    runtime errors do.

    e.g. without traceback:
        IndentationError: unexpected indent
    e.g. with traceback:
        Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
        NameError: name 'xyz' is not defined

    Parameter {str} output: line of output from a pipe.
    Parameter {File} pipe: pipe to read output from, in case of traceback.
    '''

    try:
        # Syntax errors - no traceback.
        if output.split()[0][:-1] in SYNTAX_ERRORS:
            error = output.split()[0][:-1]
            handle_exception(error)
        # Runtime error - has traceback.
        elif 'Traceback' in output.split():
            error = get_error_from_traceback(pipe)
            handle_exception(error)
    except IndexError:
        pass


def get_error_from_traceback(pipe):
    '''
    Gets the error description from a traceback.

    e.g.:
        Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
        NameError: name 'xyz' is not defined
    would return 'NameError'.

    Parameter {File} pipe: the pipe to read the traceback from.
    Returns {str}: the error description.
    '''

    output = pipe.readline()

    while (
            output.split()[0][-1] != ':'
    ):
        output = pipe.readline()

    return output.split()[0][:-1]


def handle_exception(query):
    '''
    When passed a query, this function loops over each accepted
    Stack Overflow post, and displays them, until the user inputs
    'Y'.

    Parameter {str} query: the query to display posts for.
    '''

    for post in accepted_posts(query):
        # Display Stack Overflow posts for the error.
        print_accepted_post(post)

        user_input = handle_user_input()

        # Custom query.
        if user_input not in (True, False):
            handle_exception(user_input)
            return

        # Error solved, break out of the loop.
        if user_input is True:
            print_listening_for_errors()
            return

        # Otherwise, the question wasn't answered, keep looping.


def handle_user_input():
    '''
    Prompts the user to input whether or not his/her error was solved.
    Valid inputs are 'Y' and 'n'. 'Y' meaning the error was solved and
    'f' meaning it wasn't solved. Otherwise, whatever the user entered
    is used for a custom query.

    Returns: True if 'Y' or False if 'f' was inputed; otherwise, returns
    the raw user input (custom query).
    '''

    user_input = input('Did this solve your error? (Y/n or custom query): ')

    if user_input not in ('Y', 'n'):
        return user_input

    if user_input == 'Y':
        return True

    return False


def print_listening_for_errors():
    '''
    Prints "🥞 Listening for Python errors..."
    '''

    print(u'\U0001F95E Listening for Python errors...')
