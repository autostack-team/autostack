'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: TODO: Write overview.
'''

import click

from autostack.error import (
    handle_exception
)


@click.command()
@click.argument('string')
def query(string):
    '''
    Query Stack Exchange with STRING, and dislay posts for that query string.
    '''

    handle_exception(string)
