'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: Command to initialize a .autostack.json configuration file,
locally or globally.
'''

import click
import regex
from PyInquirer import (
    prompt,
    Validator,
    ValidationError
)

from autostack import (
    print_logo
)
from autostack.config import (
    create_config
)


class MaxCommentsValidator(Validator):
    # pylint: disable=too-few-public-methods
    '''
    Validator for the max_comments prompt.
    '''

    def validate(self, document):
        '''
        Ensures that the max_comments input contains a positive integer.
        '''

        valid = regex.match(r'^\d+$', document.text)
        if not valid:
            raise ValidationError(
                message='Please enter a valid integer',
                cursor_position=len(document.text))


# Initialization prompts.
PROMPTS = [
    {
        'type': 'list',
        'name': 'language',
        'message':
            'What language do you want autostack'
            ' to capture errors for?',
        'choices': [
            {
                'name': 'Python',
                'checked': True,
            },
        ],
    },
    {
        'type': 'list',
        'name': 'order_by',
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
        'message':
            'Do you want to only display posts with verified'
            ' answers?',
    },
    {
        'type': 'confirm',
        'name': 'display_comments',
        'message':
            'Do you want to display comments with questions and'
            ' answers?',
    },
]

# Max commments prompts.
MAX_COMMENTS_PROMPTS = [
    {
        'type': 'input',
        'name': 'max_comments',
        'message':
            'What\'s the max number of comments to display per'
            ' question and answer?',
        'validate': MaxCommentsValidator,
    }
]


@click.command()
@click.option(
    '--default',
    '-d',
    is_flag=True,
    help='Use default configuration values.'
)
@click.option(
    '--global',
    '-g',
    'global_',
    is_flag=True,
    help='Initialize the global configuration file.'
)
def init(default, global_):
    '''
    Initialize a .autostack.json configuration file in the current working
    directory, or globally.
    '''

    if not default:
        print_logo()

    undecorated_init(default, global_)


def undecorated_init(default, global_):
    '''
    Initialize a .autostack.json configuration file in the current working
    directory, or globally.

    Parameter {boolean} default: whether or not to use the default
    configuration key-value pairs, which can be found in
    autostack.config.constants.
    Parameter {boolean} global_: If True, initialize the global configuration.
    If False, a local configuration will be initialized in the current working
    directory.
    '''

    if default:
        create_config(global_)
        return

    config_options = prompt(PROMPTS)

    try:
        if config_options['display_comments']:
            config_options['max_comments'] = int(
                prompt(
                    MAX_COMMENTS_PROMPTS
                )['max_comments']
            )
        else:
            config_options['max_comments'] = 0

        create_config(global_, config_options)
    except KeyError:
        pass
