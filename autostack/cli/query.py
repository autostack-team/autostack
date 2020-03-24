'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: Command to query Stack Overflow, and dislay posts for the given
query string.
'''

import click

from autostack.error import (
    handle_error
)


@click.command()
@click.argument('string')
def query(string):
    '''
    Query Stack Overflow, and dislay posts for the given query string.
    '''

    handle_error(string)
