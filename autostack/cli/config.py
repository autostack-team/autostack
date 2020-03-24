'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: Commands to interact with autostack configuration files.
'''

import click

from autostack.config import (
    reset_config,
    print_config,
    set_config
)


@click.group()
@click.option(
    '--global',
    '-g',
    'global_',
    is_flag=True,
    help='Interact with the global configuration file.'
)
@click.pass_context
def config(ctx, global_):
    '''
    Interact with autostack configuration files.
    '''

    ctx.obj = {
        'GLOBAL': global_
    }


@config.command()
@click.pass_context
def reset(ctx):
    '''
    Resets the configuration file to default values.
    '''

    reset_config(ctx.obj['GLOBAL'])


@config.command('set')
@click.argument('key')
@click.argument('value')
@click.pass_context
def set_(ctx, key, value):
    '''
    Sets a key's value in the configuration file.

    KEY in the configuration file to be assigned VALUE.
    '''

    set_config(ctx.obj['GLOBAL'], key, value)


@config.command('get')
@click.argument('key')
@click.pass_context
def get_(ctx, key):
    '''
    Gets a key's value in the configuration file.

    KEY in the configuration file to return the value for.
    '''

    print_config(ctx.obj['GLOBAL'], key)


@config.command('list')
@click.pass_context
def list_(ctx):
    '''
    Lists all key-value pairs in the configuration file.
    '''

    print_config(ctx.obj['GLOBAL'])
