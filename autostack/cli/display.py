'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: TODO: Write overview.
'''
import os

import click

from autostack.cli.constants import (
    PIPE_PATH
)
from autostack.error import (
    listen_for_errors
)


@click.command()
def display():
    '''
    Display posts for all error messages captured with the 'capture' command.
    '''

    if not os.path.exists(PIPE_PATH):
        print('Execute "autostack capture" in another terminal window first.')
        return

    with open(PIPE_PATH) as pipe:
        listen_for_errors(pipe)
