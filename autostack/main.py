'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 03/17/2019
Overview: This opens the named pipe '/tmp/monitorPipe' and listens for data
passed to the pipe. If the data is detected to be a python error, it queries
Stack Overflow for the error and displays posts with accepted answers.
'''

from __future__ import print_function
from builtins import input
import os

from autostack.web_scraper.stack_overflow_scraper import (
    accepted_posts,
    print_accepted_post
)

from autostack.features.query_features import (
    custom_query
)

PIPE_PATH = '/tmp/monitorPipe'
SYNTAX_ERRORS = [
    'SyntaxError',
    'IndentationError',
    'TabError',
]


def main():
    '''
    Listens for python errors outputed on the '/tmp/monitorPipe'
    named pipe.

    This opens the named pipe '/tmp/monitorPipe' and listens for data
    passed to the pipe. If the data is detected to be a python error,
    it queries Stack Overflow for the error and displays posts with
    accepted answers.
    '''

    try:
        create_pipe(PIPE_PATH)
    except:
        pass

    # Open the pipe.
    pipe = open(PIPE_PATH, 'r')
    print_listening()

    # Listen for new stdout.
    while True:
        # Read a line from the pipe.
        output = pipe.readline()

        # Pipe closed.
        if output == '':
            break

        try:
            if output.split()[0][:-1] in SYNTAX_ERRORS:  # Syntax errors don't have a traceback.
                handle_exception(output)
            elif 'Traceback' in output.split():  # Runtime error.
                output = pipe.readline()

                while (
                    output.split()[0][-1] != ':'
                ):
                    output = pipe.readline()

                handle_exception(output)
        except:
            pass


def handle_exception(exception):
    '''
    '''

    for post in accepted_posts(exception.split()[0][:-1]):
        # Display Stack Overflow posts for the error.
        print_accepted_post(post)

        handle_user_input()


def handle_user_input():
    '''
    '''

    while True:
        print('Did this answer your question? (Y/n): ', end='')
        question_answered = input()
        if question_answered in ('Y', 'n'):
            break

        if question_answered == 'Y':
            print_listening()
            break
        elif question_answered == 'n':
            continue

def create_pipe(path):
    '''
    Creates a named pipe at the specified path. If the fifo already exists,
    the function throws an error. This function will recursively create the
    full file path.

    Parameter {string}: the full path to the fifo.
    '''

    leaf_dir_path = path.split('/')[:-1].join('')

    if (os.path.exists(path)):
        raise Error('The fifo already exists.')
    elif not os.path.exists(leaf_dir_path):
        os.mkdirs(leaf_dir_path)
    else:
        os.mkfifo(path)

def print_listening():
    '''
    Prints "🥞 Listening for Python errors..."
    '''
    print(u'\U0001F95E Listening for Python errors...')