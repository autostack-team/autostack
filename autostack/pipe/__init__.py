'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/09/2019
Overview:
'''

import os


def create_pipe(path):
    '''
    TODO: Write docstring.

    Parameter {string}: the full path to the fifo.
    Returns: The pipe in read mode.
    '''

    leaf_dir_path = '/'.join(path.split('/')[:-1])

    if not os.path.exists(leaf_dir_path):
        os.makedirs(leaf_dir_path)

    try:
        os.mkfifo(path)
    except (FileExistsError, OSError):
        pass
