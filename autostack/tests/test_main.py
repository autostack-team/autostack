'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 07/23/2019
Overview: Tests for the main functionality.
'''

import os
from unittest import mock

import pytest

from autostack.main import main


# ======================================================================
# Mock input
# ======================================================================


# ======================================================================
# Tests for main
# ======================================================================


def test_main_pipe_dir_doesnt_exist():
    '''
    Test to ensure that the pipe is created even if the
    pipe dir doesn't exist.
    '''

    # 1. Given.
    try:
        os.system('rm -rf /tmp/')
    except:
        assert True

    # 2. When.
    with open('/tmp/monitorPipe', 'w') as monitorPipe:

        main()

    # 3. Then.

    pass


def test_main_pipe_doesnt_exist():
    '''
    Test to ensure that the pipe is created if the pipe
    doesn't exist.
    '''

    # 1. Given.

    # 2. When.

    # 3. Then.

    pass


def test_main_input_y():
    '''
    Test to ensure that, when an error is detected, inputting
    'Y' exits the post query loop.
    '''

    # 1. Given.

    # 2. When.

    # 3. Then.

    pass


def test_main_input_n():
    '''
    Test to ensure that, when an error is detected, inputting
    'n' continues the post query loop.
    '''

    # 1. Given.

    # 2. When.

    # 3. Then.

    pass
