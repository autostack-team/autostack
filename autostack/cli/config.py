'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: TODO: Write overview.
'''

import click


@click.command()
@click.option(
    '--key',
    required=True,
    help='The configuration option to change.'
)
def config():
    '''
    Set global autostack configuration options.
    '''

    return
