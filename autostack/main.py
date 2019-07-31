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

EXCEPTIONS = [
    'Exception',
    'StopIteration',
    'SystemExit',
    'StandardError',
    'ArithmeticError',
    'OverflowError',
    'FloatingPointError',
    'ZeroDivisionError',
    'AssertionError',
    'AttributeError',
    'EOFError',
    'ImportError',
    'KeyboardInterrupt',
    'LookupError',
    'IndexError',
    'KeyError',
    'NameError',
    'UnboundLocalError',
    'EnvironmentError',
    'IOError',
    'OSError',
    'SyntaxError',
    'IndentationError',
    'SystemError',
    'SystemExit',
    'TypeError',
    'ValueError',
    'RuntimeError',
    'NotImplementedError'
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
        '''
        If the current line of output is a python error,
        query Stack Overflow.
        '''
        if output.split()[0][:-1] in EXCEPTIONS:
            for post in accepted_posts(output):
                # Display Stack Overflow posts for the error.
                print_accepted_post(post)

                '''
                If the user's question has been answered,
                don't keep looping over posts.
                '''
                while True:
                    print('Did this answer your question? (Y/n): ', end='')
                    question_answered = input()
                    if question_answered == 'Y' or question_answered == 'n':
                        break
                if question_answered == 'Y':
                    print(u'\U0001F95E Listening for Python errors...')
                    break
                elif question_answered == 'n':
                    no_counter += 1
                    '''
                    If three "no"s occur in a row
                    let the user enter a custom query.
                    '''
                    if(no_counter == 3):
                        no_counter = 0
                        custom_query()
                        '''
                        After user finds an answer from their query,
                        break loop to listen for more errors.
                        '''
                        break
                    continue
