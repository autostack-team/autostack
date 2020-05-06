'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: Command to display Stack Overflow posts for all error messages
captured in terminals executing the 'capture' command.
'''

import os

import click

from autostack import (
    print_logo
)
from autostack.cli.constants import (
    PIPE_PATH
)
from autostack.cli.validators import (
    validate_display_comments,
    validate_language,
    validate_order_by
)
from autostack.config import (
    create_config_object
)
from autostack.error import (
    listen_for_errors
)


@click.command()
@click.option(
    '--language',
    '-l',
    is_flag=False,
    callback=validate_language,
    help='The language to display posts for.'
)
@click.option(
    '--order-by',
    '-o',
    is_flag=False,
    callback=validate_order_by,
    help='The display order of the posts.'
)
@click.option(
    '--verified-only/--unverified',
    '-v/-u',
    default=None,
    help='Whether or not to only display posts with verified answers.'
)
@click.option(
    '--display-comments',
    '-d',
    type=int,
    callback=validate_display_comments,
    help='The max number of comments to display on each question and answer.'
)
def display(language, order_by, verified_only, display_comments):
    '''
    Display Stack Overflow posts for all error messages captured in terminals
    executing the 'capture' command.
    '''

    print_logo()
    
    config = create_config_object(language, order_by, verified_only, display_comments)

    if not config:
        return

    if not os.path.exists(PIPE_PATH):
        print('Execute "autostack capture" in another terminal window first.')
        return

    print('Waiting on "autostack capture" to be executed...')
    with open(PIPE_PATH) as pipe:
        listen_for_errors(pipe, config)
