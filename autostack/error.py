'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/09/2019
Overview:
'''

from autostack.web_scraper.stack_overflow_scraper import (
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
    '''

    listening_for_errors()

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
            listening_for_errors()
            break
        elif question_answered == 'n':
            continue


def listening_for_errors():
    '''
    Prints "🥞 Listening for Python errors..."
    '''
    print(u'\U0001F95E Listening for Python errors...')
