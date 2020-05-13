'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: Click Group and Command setup.
'''

import click

from autostack.cli.capture import capture
from autostack.cli.config import config
from autostack.cli.display import display
from autostack.cli.init import init


@click.group()
def cli():
    '''
    A command-line debugging tool.
    '''

    return


cli.add_command(capture)
cli.add_command(config)
cli.add_command(display)
cli.add_command(init)
