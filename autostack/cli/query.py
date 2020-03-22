'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: Click command to query Stack Overflow with STRING, and dislay
posts for that query string.
'''

import click

from autostack.error import (
    handle_error
)


@click.command()
@click.argument('string')
def query(string):
    '''
    Query Stack Overflow with STRING, and dislay posts for that query string.
    '''

    handle_error(string)
