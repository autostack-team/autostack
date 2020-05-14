'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 10/22/2019
Overview: Tests for the pipe package.
'''

import shutil
import os

from autostack.pipe import create_pipe


def test_create_pipe_dir_doesnt_exist():
    '''
    Ensures that create_pipe creates the directories to the pipe
    recursively.
    '''

    # Before.
    shutil.rmtree('/tmp/test_autostack/', ignore_errors=True)

    # 1. Given.
    path = '/tmp/test_autostack/dir/pipe'

    # 2. When.
    create_pipe(path)

    # 3. Then.
    assert os.path.exists(path)

    # After.
    shutil.rmtree('/tmp/test_autostack/', ignore_errors=True)


def test_create_pipe_file_doesnt_exist():
    '''
    Ensures that create_pipe creates a pipe, if it doesn't exist.
    '''

    # 1. Given.
    path = '/tmp/test_autostack/pipe'

    # 2. When.
    create_pipe(path)

    # 3. Then.
    assert os.path.exists(path)

    # After.
    os.remove(path)


def test_create_pipe_file_already_exists():
    '''
    Ensures that if a file already exists at the specifies path,
    it will not be overwritten.
    '''

    # 1. Given.
    path = '/tmp/test_autostack/pipe'

    # 2. When.
    os.mkfifo(path)
    modified_time = os.path.getmtime(path)
    create_pipe(path)

    # 3. Then.
    assert os.path.getmtime(path) == modified_time
