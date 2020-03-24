'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: Command to display Stack Overflow posts for all error messages
captured in terminals executing the 'capture' command.
'''

import os

import click

from autostack.config.constants import (
    SUPPORTED_LANGUAGES,
    SUPPORTED_ORDER_BY_FILTERS
)
from autostack.cli.constants import (
    PIPE_PATH
)
from autostack.error import (
    listen_for_errors
)


def validate_language(ctx, param, value):
    '''
    Validates the language option.

    Parameter {click.core.Context} ctx: the command's context.
    Parameter {click.core.Option} param: the command's option.
    Parameter {any} param: the value passed to the command's option.
    '''

    if value is not None and value not in SUPPORTED_LANGUAGES:
        raise click.BadParameter(
            '{} is an invalid language. Use one of {}.'
            .format(value, SUPPORTED_LANGUAGES)
        )


def validate_order_by(ctx, param, value):
    '''
    Validates the order_by option.

    Parameter {click.core.Context} ctx: the command's context.
    Parameter {click.core.Option} param: the command's option.
    Parameter {any} param: the value passed to the command's option.
    '''

    if value is not None and value not in SUPPORTED_ORDER_BY_FILTERS:
        raise click.BadParameter(
            '{} is an invalid order-by filter. Use one of {}.'
            .format(value, SUPPORTED_ORDER_BY_FILTERS)
        )


def validate_display_comments(ctx, param, value):
    '''
    Validates the display_comments option.

    Parameter {click.core.Context} ctx: the command's context.
    Parameter {click.core.Option} param: the command's option.
    Parameter {any} param: the value passed to the command's option.
    '''

    if value is not None and value <= 0:
        raise click.BadParameter(
            '{} is invalid. Enter a postitive integer.'
            .format(value)
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

    config = {
        'language': language,
        'order_by': order_by,
        'verified_only': verified_only,
        'display_comments': display_comments
    }

    if not os.path.exists(PIPE_PATH):
        print('Execute "autostack capture" in another terminal window first.')
        return

    with open(PIPE_PATH) as pipe:
        listen_for_errors(pipe, config)
