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

from autostack import (
    print_logo
)
from autostack.config import (
    get_config
)
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

    print_logo()
    print_listening_for_errors()

    while True:
        output = pipe.readline()

        # Pipe closed.
        if output == '':
            break
        
        detect_and_handle_error(pipe, output, config)


def detect_and_handle_error(pipe, output, config):
    '''
    Loops over the configured languages and parses for an error for
    each language. If an error is detected for a language, it is handled.

    Parameter {string} language: the language to parse for an outputted error.
    Parameter {string} output: the current line of output captured with the
    "capture" cli command.
    Parameter {dictionary} config: configuration object passed in from
    the "display" cli command.
    '''

    error_handled = False

    for language in get_configured_languages(config):
        error = get_error(language, output, pipe)

        if error:
            handle_error(error)
            error_handled = True

    if error_handled:
        print_listening_for_errors()


def get_error(language, output, pipe):
    '''
    With the given configured language, import the appropriate parser
    to retrieve an (potential) error in the terminal. This function will
    return None if there are no errors detected with the given output and
    the configured language.

    Parameter {string} language: the language to parse for an outputted error.
    Parameter {string} output: the current line of output captured with the
    "capture" cli command.
    Parameter {file} pipe: the pipe being used to capture terminal output.
    Returns {string|None}: the error, or None, if there isn't one detected.
    '''

    try:
        error_lib = importlib.import_module(
            'autostack.error.{}'.format(language.lower())
        )

        return error_lib.parse_output_for_error(output, pipe)
    except ImportError:
        print('The language {} is not yet supported.'.format(language))


def get_configured_languages(config):
    '''
    Gets the configured languages to display errors for. The order
    of retrieval is as follows:

    1. "diplay" command configuration.
    2. Local .autostack.json configuration.
    3. Global .autostack.json configuration.

    Returns {list}: the list of configured languages.
    '''

    # Configs set by the "display" cli command.
    try:
        return config.languages
    except:
        # Local configurations.
        if get_config(False, 'languages'):
            return get_config(False, 'languages')
        # Global configurations.
        elif get_config(True, 'languages'):
            return get_config(True, 'languages')

    return []


def handle_error(query):
    '''
    When passed a query, this function loops over each accepted
    Stack Overflow post, and displays them, until the user inputs
    'Y'.

    Parameter {str} query: the query to display posts for.
    '''

    for post in accepted_posts(query):
        # Display Stack Overflow posts for the error.
        clear_terminal()
        print_accepted_post(post)

        user_input = handle_user_input()

        # Custom query.
        if user_input not in (True, False):
            handle_error(user_input)
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
