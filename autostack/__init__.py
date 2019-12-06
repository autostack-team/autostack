'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 03/17/2019
Overview: The autostack package includes a cli and packages for error
parsing, querying Stack Exchange, etc.
'''

name = "autostack"  # pylint: disable=invalid-name

import click
import regex
from PyInquirer import (
    prompt,
    Validator,
    ValidationError
)

from autostack.error import (
    listen_for_errors
)
from autostack.pipe import (
    create_pipe
)

PIPE_PATH = '/tmp/monitorPipe'


def print_logo():
    '''
    Prints the autostack logo, in color.
    '''

    print(u'        \u001b[38;5;179m_____________        ')
    print(u'       \u001b[38;5;179m/    \u001b[38;5;226m___      \u001b[38;5;179m\       \u001b[0m')
    print(u'      \u001b[38;5;179m||    \u001b[38;5;226m\__\\\u001b[0m     \u001b[38;5;179m||\u001b[38;5;208m                   _            _             _    ')
    print(u'      \u001b[38;5;179m||      \u001b[38;5;94m_\u001b[38;5;179m      ||\u001b[38;5;208m                  | |          | |           | |   ')
    print(u'      \u001b[38;5;179m|\     \u001b[38;5;94m/ \\\u001b[38;5;179m     /|\u001b[38;5;208m        __ _ _   _| |_ ___  ___| |_ __ _  ___| | __')
    print(u'      \u001b[38;5;179m\ \___\u001b[38;5;94m/ ^ \\\u001b[38;5;179m___/ /\u001b[38;5;208m       / _` | | | | __/ _ \/ __| __/ _` |/ __| |/ /')
    print(u'      \u001b[38;5;179m\\\\____\u001b[38;5;94m/_^_\\\u001b[38;5;179m____//\u001b[38;5;94m_\u001b[38;5;208m     | (_| | |_| | || (_) \__ \ || (_| | (__|   < ')
    print(u'    \u001b[38;5;94m__\u001b[38;5;179m\\\\____\u001b[38;5;94m/_^_\\\u001b[38;5;179m____// \u001b[38;5;94m\\\u001b[38;5;208m     \__,_|\__,_|\__\___/|___/\__\__,_|\___|_|\_\\')
    print(u'   \u001b[38;5;94m/   \u001b[38;5;179m\____\u001b[38;5;94m/_^_\\\u001b[38;5;179m____/ \u001b[38;5;224m\ \u001b[38;5;94m\\\u001b[0m     \033[1mAUTOMATING THE INEVITABLE...')
    print(u'  \u001b[38;5;94m/\u001b[38;5;224m/\u001b[38;5;94m                   \u001b[38;5;224m, \u001b[38;5;94m/   ')
    print(u'  \u001b[38;5;94m\\\u001b[38;5;224m\\\u001b[38;5;94m___________   \u001b[38;5;224m____  \u001b[38;5;94m/  ')
    print(u'               \u001b[38;5;94m\_______/\u001b[0m     \n')


@click.group()
def cli():
    pass


@cli.command()
def init():
    '''
    Initialize a project with a .autostackrc configuration file.
    '''

    QUESTIONS = [
        {
            'type': 'checkbox',
            'name': 'languages',
            'message': 'What languages do you want autostack to capture errors for?',
            'choices': [
                {
                    'name': 'Python',
                    'checked': True,
                },
            ]
        },
        {
            'type': 'checkbox',
            'name': 'communities',
            'message': 'Which Stack Exchange communities do you want to query?',
            'choices': [
                {
                    'name': 'Stack Overflow',
                    'checked': True,
                },
            ]
        },
        {
            'type': 'list',
            'name': 'communities',
            'message': 'How do you want to order posts?',
            'choices': [
                'Relevance',
                'Newest',
                'Active',
                'Votes',
            ]
        },
        {
            'type': 'confirm',
            'name': 'verified_only',
            'message': 'Do you want to only display posts with verified answers?',
        },
        {
            'type': 'confirm',
            'name': 'display_comments',
            'message': 'Do you want to display comments with questions and answers?',
        },
    ]

    class MaxCommentsValidator(Validator):
        def validate(self, document):
            valid = regex.match('^\d+$', document.text)
            if not valid:
                raise ValidationError(
                    message='Please enter a valid integer',
                    cursor_position=len(document.text))

    MAX_COMMENTS_QUESTION = [
        {
            'type': 'input',
            'name': 'max_comments',
            'message': 'What\'s the max number of comments to display per question or answer?',
            'validate': MaxCommentsValidator,
        }
    ]

    print_logo()
    answers = prompt(QUESTIONS)
    if answers['display_comments']:
        answers['max_comments'] = prompt(MAX_COMMENTS_QUESTION)['max_comments']


@cli.command()
@click.option('--key', required=True, help='The configuration option to change.')
def config():
    '''
    Set global autostack configuration options.
    '''

    pass


@cli.command()
def display():
    '''
    Display posts for all error messages captured with the 'capture' command.
    '''

    with open(PIPE_PATH) as pipe:
        listen_for_errors(pipe)


@cli.command()
def capture():
    '''
    Capture all error messages outputed in the terminal, for configured languages.
    '''

    create_pipe(PIPE_PATH)


@cli.command()
@click.argument('message')
def error():
    '''
    Query for a given error message, and dislay posts for that query.
    '''

    pass
