'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 03/17/2019
Overview: This opens the named pipe '/tmp/monitorPipe' and listens for data
passed to the pipe. If the data is detected to be a python error, it queries
Stack Overflow for the error and displays posts with accepted answers.
'''

from autostack.error import (
    listen_for_errors
)
from autostack.pipe import (
    create_pipe
)

PIPE_PATH = './blah/blah2/monitorPipe'


def main():
    '''
    Opens a fifo and starts listening for python errors inputed to the pipe.
    '''

    with create_pipe(PIPE_PATH) as pipe:
        listen_for_errors(pipe)
