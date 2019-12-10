'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: TODO: Write overview.
'''

import click

from autostack.config import (
    get_all_global_configs,
    set_global_config
)


@click.command()
@click.option(
    '--key',
    '-k',
    help='The configuration option to change.',
)
@click.option(
    '--list',
    '-l',
    'list_',
    help='List all global configurations.',
    flag_value=True,
)
@click.pass_context
def config(ctx, key, list_):
    '''
    View and set global autostack configurations.
    '''

    if not key and not list_:
        click.echo(ctx.get_help())
    elif list_:
        get_all_global_configs()
    # elif key:
    #     set_global_config(key)
