'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/05/2020
Overview: Validates command-line input from the user.
'''

import click

from autostack.config.constants import (
    SUPPORTED_LANGUAGES,
    SUPPORTED_ORDER_BY_FILTERS
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
