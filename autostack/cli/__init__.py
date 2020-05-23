'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: Click Group and Command setup.
'''

import click

from autostack.cli.capture import capture_command
from autostack.cli.config import config_command
from autostack.cli.display import display_command
from autostack.cli.init import init_command


@click.group()
def autostack():  # pragma: no cover
    '''
    A command-line debugging tool.
    '''

    return


autostack.add_command(capture_command, name='capture')
autostack.add_command(config_command, name='config')
autostack.add_command(display_command, name='display')
autostack.add_command(init_command, name='init')
