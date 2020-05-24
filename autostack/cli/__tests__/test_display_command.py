'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/12/2019
Overview: Tests for the config package.
'''

import os

from click.testing import CliRunner

from autostack.cli.constants import PIPE_PATH
from autostack.cli.display import display_command
from autostack.config.constants import DEFAULT_CONFIG

TEST_PIPE_PATH = PIPE_PATH + '.txt'


def mock_do_nothing(*args):
    # pylint: disable=unused-argument
    '''
    Mock method that doesn't do anything.
    '''

    return


def mock_create_config_object(*args, valid=True):
    # pylint: disable=unused-argument
    '''
    Mock create_config_object method.
    '''

    return DEFAULT_CONFIG


def mock_create_invalid_config_object(*args, valid=True):
    # pylint: disable=unused-argument
    '''
    Mock create_config_object method.
    '''

    return None


def delete_pipe():
    '''
    Deletes the pipe used to capture output.
    '''

    try:
        os.remove(TEST_PIPE_PATH)
    except FileNotFoundError:
        pass


def make_pipe():
    '''
    Makes the "pipe" used to capture output, which is just a txt
    file in this case; otherwise, the test would hang listening
    for input.
    '''

    open(TEST_PIPE_PATH, 'w').close()


def test_display_command_no_arguments(monkeypatch):
    '''
    Ensure that the display command functions properly when
    no arguments are passed in.
    '''

    # Before.
    make_pipe()

    # 1. Given.
    runner = CliRunner()

    monkeypatch.setattr(
        'autostack.cli.display.PIPE_PATH',
        TEST_PIPE_PATH
    )
    monkeypatch.setattr(
        'autostack.cli.display.create_config_object',
        mock_create_config_object
    )
    monkeypatch.setattr(
        'autostack.cli.display.listen_for_errors',
        mock_do_nothing
    )

    # 2. When.
    result = runner.invoke(display_command)

    # 3. Then.
    assert result.exit_code == 0

    # After.
    delete_pipe()


def test_display_command_invalid_config_object(monkeypatch):
    '''
    Ensure that the display command exits when a valid config
    object couldn't be created.
    '''

    # Before.
    make_pipe()

    # 1. Given.
    runner = CliRunner()

    monkeypatch.setattr(
        'autostack.cli.display.PIPE_PATH',
        TEST_PIPE_PATH
    )
    monkeypatch.setattr(
        'autostack.cli.display.create_config_object',
        mock_create_invalid_config_object
    )
    monkeypatch.setattr(
        'autostack.cli.display.listen_for_errors',
        mock_do_nothing
    )

    # 2. When.
    result = runner.invoke(display_command)

    # 3. Then.
    assert result.exit_code == 0

    # After.
    delete_pipe()


def test_display_command_no_pipe(monkeypatch):
    '''
    Ensure that the display command exits when there's
    no pipe to listen to.
    '''

    # Before.
    delete_pipe()

    # 1. Given.
    runner = CliRunner()

    monkeypatch.setattr(
        'autostack.cli.display.PIPE_PATH',
        TEST_PIPE_PATH
    )
    monkeypatch.setattr(
        'autostack.cli.display.create_config_object',
        mock_create_config_object
    )
    monkeypatch.setattr(
        'autostack.cli.display.listen_for_errors',
        mock_do_nothing
    )

    # 2. When.
    result = runner.invoke(display_command)

    # 3. Then.
    assert result.exit_code == 0


def test_display_command_custom_query(monkeypatch):
    '''
    Ensure that the display command functions properly when
    a custom query is passed in.
    '''

    # Before.
    make_pipe()

    # 1. Given.
    runner = CliRunner()
    custom_query = 'ERROR'
    given_query = None

    def mock_handle_error(query, *args):
        # pylint: disable=unused-argument
        '''
        Mocks the handle_error method.
        '''

        nonlocal given_query
        given_query = query

    monkeypatch.setattr(
        'autostack.cli.display.PIPE_PATH',
        TEST_PIPE_PATH
    )
    monkeypatch.setattr(
        'autostack.cli.display.create_config_object',
        mock_create_config_object
    )
    monkeypatch.setattr(
        'autostack.cli.display.listen_for_errors',
        mock_do_nothing
    )
    monkeypatch.setattr(
        'autostack.cli.display.handle_error',
        mock_handle_error
    )

    # 2. When.
    result = runner.invoke(display_command, custom_query)

    # 3. Then.
    assert result.exit_code == 0
    assert given_query == custom_query

    # After.
    delete_pipe()


# ======================================================================
#
# VALIDATORS TESTS
#
# ======================================================================


def test_display_command_invalid_language():
    '''
    Ensure that the display command only accepts supported
    languages.
    '''

    # 1. Given.
    runner = CliRunner()

    # 2. When.
    result = runner.invoke(display_command, ['--language', 'C++'])

    # 3. Then.
    assert result.exit_code == 2
    assert 'Error:' in result.output


def test_display_command_invalid_order_by():
    '''
    Ensure that the display command only accepts supported
    order_by.
    '''

    # 1. Given.
    runner = CliRunner()

    # 2. When.
    result = runner.invoke(display_command, ['--order-by', 'Longest'])

    # 3. Then.
    assert result.exit_code == 2
    assert 'Error:' in result.output


def test_display_command_invalid_max_comments_string():
    '''
    Ensure that the display command only accepts supported
    range of max-comments.
    '''

    # 1. Given.
    runner = CliRunner()

    # 2. When.
    result = runner.invoke(display_command, ['--max-comments', 'String'])

    # 3. Then.
    assert result.exit_code == 2
    assert 'Error:' in result.output


def test_display_command_invalid_max_comments_negative_number():
    '''
    Ensure that the display command only accepts supported
    range of max-comments.
    '''

    # 1. Given.
    runner = CliRunner()

    # 2. When.
    result = runner.invoke(display_command, ['--max-comments', -7])

    # 3. Then.
    assert result.exit_code == 2
    assert 'Error:' in result.output
