'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/09/2019
Overview: Contains all methods to detect and handle errors.
'''

import importlib

from autostack import clear_terminal
from autostack.so_web_scraper import (
    posts
)
from autostack.so_web_scraper.print import (
    print_post
)


def listen_for_errors(pipe, config):
    '''
    Reads output from a pipe until EOF, indicated by empty string. The
    output is parsed for errors.

    Parameter {file} pipe: the pipe to read output from.
    Parameter {dictionary} config: configuration object.
    '''

    # Import the appropriate error detection library.
    error_library = importlib.import_module(
        'autostack.error.{}'.format(config['language'].lower())
    )

    print_listening_for_errors()

    # Parse each line of output from the pipe for errors.
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

    Parameter {file} pipe: the pipe to read output from.
    Parameter {string} output: the current line of output read from the pipe.
    Parameter {library} error_library: the library to use for parsing for
    errors.
    Parameter {dictionary} config: configuration object.
    '''

    error = error_library.parse_output_for_error(output, pipe)

    if error:
        handle_error(error, config)
        print_listening_for_errors()


def handle_error(query, config):
    '''
    When passed a query, this function loops over each accepted
    Stack Overflow post, and displays them, until the user inputs
    'Y'.

    Parameter {string} query: the query to display posts for.
    Parameter {dictionary} config: configuration object.
    '''

    for post in posts(query, config):
        clear_terminal()
        print_post(post, config)

        user_input = handle_user_input()

        # Custom query.
        if user_input not in (True, False):
            handle_error(user_input, config)
            return

        # T - Error solved, break out of the loop.
        if user_input is True:
            clear_terminal()
            return

        # f - The question wasn't answered, keep looping.


def handle_user_input():
    '''
    Prompts the user to input whether or not his/her error was solved.
    Valid inputs are 'Y' and 'n'. 'Y' meaning the error was solved and
    'f' meaning it wasn't solved. Otherwise, whatever the user entered
    is used for a custom query.

    Returns {boolean} True if 'Y' or False if 'f' was inputed; otherwise,
    returns the raw user input (custom query).
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
