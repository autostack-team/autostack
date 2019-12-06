'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: TODO: Write overview.
'''

import click

from autostack.error import (
    listen_for_errors
)

PIPE_PATH = '/tmp/monitorPipe'


@click.command()
def display():
    '''
    Display posts for all error messages captured with the 'capture' command.
    '''

    with open(PIPE_PATH) as pipe:
        listen_for_errors(pipe)
