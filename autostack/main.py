'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 03/17/2019
Overview: Entry point of autostack.
'''

from autostack.error import (
    listen_for_errors
)
from autostack.pipe import (
    create_pipe
)

PIPE_PATH = '/tmp/monitorPipe'


def main():
    '''
    Entry point of autostack.
    '''

    with create_pipe(PIPE_PATH) as pipe:
        listen_for_errors(pipe)
