'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: TODO: Write overview.
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
def capture():
    '''
    Capture all error messages outputed in the terminal for configured
    languages.
    '''

    create_pipe(PIPE_PATH)

    if sys.platform.startswith('darwin'):  # Mac
        subprocess.run(['script', '-q', '-F', '/tmp/monitorPipe'], check=True)
    else:
        subprocess.run(['script', '-q', '-f', '/tmp/monitorPipe'], check=True)
