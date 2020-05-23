'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: Command to captures all output in the terminal, which is to be
used with the 'display' command in another terminal.
'''

import subprocess
import sys

import click

from autostack.cli.constants import (
    PIPE_PATH
)
from autostack.pipe import (
    create_pipe
)


@click.command()
def capture_command():
    '''
    Captures all output in the terminal, which is to be used with the
    'display' command in another terminal.
    '''

    create_pipe(PIPE_PATH)

    # Depending on the platform (Mac or Linux), the -f, or -F, flag changes.
    try:
        if sys.platform.startswith('darwin'):  # Mac
            subprocess.run(['script', '-q', '-F', PIPE_PATH], check=True)
        else:  # Linux
            subprocess.run(['script', '-q', '-f', PIPE_PATH], check=True)
    except subprocess.CalledProcessError:
        # The display terminal was exited with ctrl-c.
        pass
