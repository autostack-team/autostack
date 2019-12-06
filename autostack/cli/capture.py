'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: TODO: Write overview.
'''

import click

from autostack.pipe import (
    create_pipe
)


@click.command()
def capture():
    '''
    Capture all error messages outputed in the terminal, for configured languages.
    '''

    create_pipe(PIPE_PATH)
