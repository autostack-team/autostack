'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: Click command to capture all error messages outputed in the terminal
for configured languages.
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
    Captures all output in the terminal, and pipes it to /tmp/monitorPipe.
    '''

    create_pipe(PIPE_PATH)

    try:
        if sys.platform.startswith('darwin'):  # Mac
            subprocess.run(['script', '-q', '-F', PIPE_PATH], check=True)
        else:  # Linux
            subprocess.run(['script', '-q', '-f', PIPE_PATH], check=True)
    except subprocess.CalledProcessError:
        # The display terminal was exited with ctrl-c.
        pass
