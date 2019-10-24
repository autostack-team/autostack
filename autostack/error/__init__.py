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


def handle_exception(error_description):
    '''
    When passed an error description, this function loops over each
    accepted Stack Overflow post, and displays them, until the user
    inputs 'Y'.

    Parameter {str} error_description: the error description to
    display posts for.
    '''

    for post in accepted_posts(error_description):
        # Display Stack Overflow posts for the error.
        print_accepted_post(post)

        error_is_solved = error_solved()

        if error_is_solved:
            print_listening_for_errors()
            break


def error_solved():
    '''
    Prompts the user to input whether or not his/her error was solved.
    The only two valid inputs are 'Y' and 'n'. 'Y' meaning the error
    was solved and 'f' meaning it wasn't solved.

    Returns: True if 'Y' was inputed and False if 'f' was inputed.
    '''

    is_error_solved = False

    while True:
        is_error_solved = input('Did this solve your error? (Y/n): ')

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
