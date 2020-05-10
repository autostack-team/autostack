'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/09/2019
Overview: Contains the methods necessary for creating a pipe (FIFO),
which is used to capture all output in a terminal session.
'''

import os


def create_pipe(path):
    '''
    Given a file path, create a FIFO pipe, and return it in read mode.

    Parameter {string} path: the full path to the FIFO.
    Returns {file} The pipe in read mode.
    '''

    leaf_dir_path = '/'.join(path.split('/')[:-1])

    if not os.path.exists(leaf_dir_path):
        os.makedirs(leaf_dir_path)

    try:
        os.mkfifo(path)
    except (FileExistsError, OSError):
        pass
