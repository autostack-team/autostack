'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/22/2019
Overview: Tests for the cli capture.
'''

import subprocess
import sys
from click.testing import CliRunner

from autostack.cli.capture import capture_command


def mock_subprocess_run(*args, **kwargs):
    # pylint: disable=unused-argument
    '''
    Mocks the subprocess.run method.
    '''

    return ' '.join(*args)


def mock_subprocess_run_raise(*args, **kwargs):
    # pylint: disable=unused-argument
    '''
    Mocks the subprocess.run method, raising an error.
    '''

    raise subprocess.CalledProcessError(returncode=-1, cmd=subprocess.run)


def mock_create_pipe(*args):
    # pylint: disable=unused-argument
    '''
    Mocks the create_pipe method.
    '''

    return


def test_capture_mac(monkeypatch):
    '''
    Ensures the proper subprocess is started on Mac.
    '''

    # 1. Given.
    runner = CliRunner()

    monkeypatch.setattr(
        'autostack.pipe.create_pipe',
        mock_create_pipe
    )
    monkeypatch.setattr(
        sys,
        'platform',
        'darwin'
    )
    monkeypatch.setattr(
        subprocess,
        'run',
        mock_subprocess_run
    )

    # 2. When.
    result = runner.invoke(capture_command)

    # 3. Then.
    assert result.exit_code == 0


def test_capture_linux(monkeypatch):
    '''
    Ensures the proper subprocess is started on Mac.
    '''

    # 1. Given.
    runner = CliRunner()

    monkeypatch.setattr(
        'autostack.pipe.create_pipe',
        mock_create_pipe
    )
    monkeypatch.setattr(
        sys,
        'platform',
        'linux'
    )
    monkeypatch.setattr(
        subprocess,
        'run',
        mock_subprocess_run
    )

    # 2. When.
    result = runner.invoke(capture_command)

    # 3. Then.
    assert result.exit_code == 0


def test_capture_error(monkeypatch):
    '''
    Ensures the proper subprocess is started on Mac.
    '''

    # 1. Given.
    runner = CliRunner()

    monkeypatch.setattr(
        'autostack.pipe.create_pipe',
        mock_create_pipe
    )
    monkeypatch.setattr(
        sys,
        'platform',
        'darwin'
    )
    monkeypatch.setattr(
        subprocess,
        'run',
        mock_subprocess_run_raise
    )

    # 2. When.
    result = runner.invoke(capture_command)

    # 3. Then.
    assert result.exit_code == 0
