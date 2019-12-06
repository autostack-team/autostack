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
@click.argument('message')
def error(message):
    '''
    Query for a given error message, and dislay posts for that query.
    '''

    handle_exception(message)
