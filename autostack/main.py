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

BUILT_IN_EXCEPTIONS = [
    'Exception',
    'StopIteration',
    'StopAsyncIteration',
    'ArithmeticError',
    'FloatingPointError',
    'OverflowError',
    'ZeroDivisionError',
    'AssertionError',
    'AttributeError',
    'BufferError',
    'EOFError',
    'ImportError',
    'ModuleNotFoundError',
    'LookupError',
    'IndexError',
    'KeyError',
    'MemoryError',
    'NameError',
    'UnboundLocalError',
    'OSError',
    'BlockingIOError',
    'ChildProcessError',
    'ConnectionError',
    'BrokenPipeError',
    'ConnectionAbortedError',
    'ConnectionRefusedError',
    'ConnectionResetError',
    'FileExistsError',
    'FileNotFoundError',
    'InterruptedError',
    'IsADirectoryError',
    'NotADirectoryError',
    'PermissionError',
    'ProcessLookupError',
    'TimeoutError',
    'ReferenceError',
    'RuntimeError',
    'NotImplementedError',
    'RecursionError',
    'SyntaxError',
    'IndentationError',
    'TabError',
    'SystemError',
    'TypeError',
    'ValueError',
    'UnicodeError',
    'UnicodeDecodeError',
    'UnicodeEncodeError',
    'UnicodeTranslateError'
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

    # Ensure that the pipe exists; if not, create it.
    if not os.path.exists('/tmp'):
        os.mkdir('/tmp')
        os.mkfifo('/tmp/monitorPipe')
    elif not os.path.exists('/tmp/monitorPipe'):
        os.mkfifo('/tmp/monitorPipe')

    # Open the pipe.
    pipe = open('/tmp/monitorPipe', 'r')
    print('Development terminal[s] open - ')
    print(u'\U0001F95E Listening for Python errors...')

    # Listen for new stdout.
    while True:
        # Read a line from the pipe.
        output = pipe.readline()

        # Pipe closed.
        if output == '':
            break

        # Variable to count number of "no"s.
        no_counter = 0

        # If the current line of output is a built-in exception,
        # query Stack Overflow.
        try:
            if output.split()[0][:-1] in BUILT_IN_EXCEPTIONS:
                for post in accepted_posts(output.split()[0][:-1]):
                    # Display Stack Overflow posts for the error.
                    print_accepted_post(post)

                    # If the user's question has been answered,
                    # don't keep looping over posts.
                    while True:
                        print('Did this answer your question? (Y/n): ', end='')
                        question_answered = input()
                        if question_answered in ('Y', 'n'):
                            break
                    if question_answered == 'Y':
                        print(u'\U0001F95E Listening for Python errors...')
                        break
                    elif question_answered == 'n':
                        continue

            # If the current line of output indicates an exception,
            # ignore the traceback and query Stack Overflow for the
            # exception.
            elif 'Traceback' in output.split():
                output = pipe.readline()

                while (
                    output.split()[0][-1] != ':'
                ):
                    output = pipe.readline()
                
                for post in accepted_posts(output.split()[0][:-1]):
                    # Display Stack Overflow posts for the error.
                    print_accepted_post(post)

                    # If the user's question has been answered,
                    # don't keep looping over posts.
                    while True:
                        print('Did this answer your question? (Y/n): ', end='')
                        question_answered = input()
                        if question_answered in ('Y', 'n'):
                            break
                    if question_answered == 'Y':
                        print(u'\U0001F95E Listening for Python errors...')
                        break
                    elif question_answered == 'n':
                        continue
        except:
            continue
