'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: Command to query Stack Overflow, and dislay posts for the given
query string.
'''

import click

from autostack.cli.validators import (
    validate_display_comments,
    validate_language,
    validate_order_by
)
from autostack.config import (
    create_config_object
)
from autostack.error import (
    handle_error
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
@click.argument('string')
def query(string, language, order_by, verified_only, display_comments):
    '''
    Query Stack Overflow, and dislay posts for the given query string.
    '''

    config = create_config_object(language, order_by, verified_only, display_comments)

    if not config:
        return

    handle_error(string, config)
