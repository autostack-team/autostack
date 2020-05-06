'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/09/2019
Overview: Ability to handle errors.
'''

from __future__ import (
    absolute_import,
    division,
    print_function
)

import importlib

from autostack.so_web_scraper import (
    accepted_posts,
    print_accepted_post
)


def listen_for_errors(pipe, config):
    '''
    Reads output from a pipe until EOF, indicated by empty string. The
    output is parsed for errors.

    Parameter {file} pipe: the pipe to read output from.
    Parameter {dictionary} config: configuration object passed in from
    the "display" cli command.
    '''

    error_library = None

    # Import the appropriate error detection library.
    error_library = importlib.import_module(
        'autostack.error.{}'.format(config['language'].lower())
    )

    print_listening_for_errors()

    while True:
        output = pipe.readline()

        # Pipe closed.
        if output == '':
            break
        
        parse_output_for_error(pipe, output, error_library, config)


def parse_output_for_error(pipe, output, error_library, config):
    '''
    Given a line of output read in from the pipe, determine if an error was
    outputted, and if so, display Stack Overflow posts for that error.

    Parameter {file} pipe: the pipe to read output from, if needed.
    Parameter {string} output: the current line of output read from the pipe.
    Parameter {library} error_library: the library to use for parsing for errors.
    Parameter {dictionary} config: configuration object passed in from
    the "display" cli command.
    '''

    error_handled = False
    error = None

    # Parse the current line of output from the pipe for an error.
    error = error_library.parse_output_for_error(output, pipe)

    if error:
        handle_error(error, config)
        error_handled = True

    if error_handled:
        print_listening_for_errors()


def handle_error(query, config):
    '''
    When passed a query, this function loops over each accepted
    Stack Overflow post, and displays them, until the user inputs
    'Y'.

    Parameter {str} query: the query to display posts for.
    Parameter {dictionary} config: configuration object passed in from
    the "display" cli command.
    '''

    for post in accepted_posts(query):
        # Display Stack Overflow posts for the error.
        clear_terminal()
        print_accepted_post(post)

        user_input = handle_user_input()

        # Custom query.
        if user_input not in (True, False):
            handle_error(user_input, config)
            return

        # Error solved, break out of the loop.
        if user_input is True:
            clear_terminal()
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
    user_input = user_input.lower()

    if user_input not in ('y', 'n'):
        return user_input

    if user_input == 'y':
        return True

    return False


def print_listening_for_errors():
    '''
    Prints "🥞 Listening for errors..."
    '''

    print(u'\U0001F95E Listening for errors...')


def clear_terminal():
    '''
    Clears the terminal window.
    '''

    print(u'\033c')
