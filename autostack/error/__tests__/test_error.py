'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/22/2019
Overview: Tests for the error package.
'''

from autostack.error import (
    listen_for_errors,
    parse_output_for_error,
    # get_error_from_traceback,
    # handle_exception,
    error_solved,
    print_listening_for_errors,
)
from autostack.error.__tests__.mock_pipe import MockPipe


def test_listen_for_errors(monkeypatch):
    '''
    Ensures that listen_for_errors reads output from a pipe until
    empty string is returned. In this case, that'd be 3 calls.
    '''

    # 1. Given.
    def mock_print_listening_for_errors():
        '''
        Mocks the print_listening_for_errors function.
        '''

        return

    def mock_parse_output_for_error(output, pipe):
        # pylint: disable=unused-argument
        '''
        Mocks the parse_output_for_error function.
        '''

        return

    monkeypatch.setattr(
        'autostack.error.print_listening_for_errors',
        mock_print_listening_for_errors
    )

    monkeypatch.setattr(
        'autostack.error.parse_output_for_error',
        mock_parse_output_for_error
    )

    mockpipe = MockPipe(['output', 'output', ''])

    # 2. When.
    listen_for_errors(mockpipe)

    # 3. Then.
    assert mockpipe.get_readline_call_count() == 3


def test_parse_output_for_error_non_error(monkeypatch):
    '''
    Ensures that handle_exception is never called when a non-error
    is passed into parse_output_for_error.
    '''

    # 1. Given.
    output = 'IndentationError: unexpected indent'
    error_called_with = None
    was_called = False

    def mock_handle_exception(error):
        nonlocal error_called_with
        nonlocal was_called
        was_called = True
        error_called_with = error

    monkeypatch.setattr(
        'autostack.error.handle_exception',
        mock_handle_exception
    )

    # 2. When.
    parse_output_for_error(output, None)

    # 3. Then.
    assert error_called_with == 'IndentationError'
    assert was_called


def test_parse_output_for_error_with_error(monkeypatch):
    '''
    Ensures that handle_exception is called when an error
    is passed into parse_output_for_error.
    '''

    # 1. Given.
    output = 'Not an error.'
    error_called_with = None
    was_called = False

    def mock_handle_exception(error):
        nonlocal error_called_with
        nonlocal was_called
        was_called = True
        error_called_with = error

    monkeypatch.setattr(
        'autostack.error.handle_exception',
        mock_handle_exception
    )

    # 2. When.
    parse_output_for_error(output, None)

    # 3. Then.
    assert not error_called_with
    assert not was_called


def test_parse_output_for_error_traceback(monkeypatch):
    '''
    Ensures that handle_exception is called when a traceback
    is passed into parse_output_for_error.
    '''

    # 1. Given.
    pipe = MockPipe([
        '    File "<stdin>", line 1, in <module>',
        'NameError: name \'xyz\' is not defined'
    ])
    output = 'Traceback (most recent call last):'
    error_called_with = None
    was_called = False

    def mock_handle_exception(error):
        nonlocal error_called_with
        nonlocal was_called
        was_called = True
        error_called_with = error

    def mock_get_error_from_traceback(pipe):
        # pylint: disable=unused-argument
        return 'NameError'

    monkeypatch.setattr(
        'autostack.error.handle_exception',
        mock_handle_exception
    )

    monkeypatch.setattr(
        'autostack.error.get_error_from_traceback',
        mock_get_error_from_traceback
    )

    # 2. When.
    parse_output_for_error(output, pipe)

    # 3. Then.
    assert error_called_with == 'NameError'
    assert was_called


def test_error_solved_y(monkeypatch):
    '''
    Ensures that when 'Y' is inputted, error_solved returns True.
    '''

    # 1. Given.
    def mock_input(*args):
        # pylint: disable=unused-argument
        '''
        '''

        return 'Y'

    monkeypatch.setattr('builtins.input', mock_input)

    # 2. When.
    is_error_solved = error_solved()

    # 3. Then.
    assert is_error_solved


def test_error_solved_n(monkeypatch):
    '''
    Ensures that when 'n' is inputted, error_solved returns False.
    '''

    # 1. Given.
    def mock_input(*args):
        # pylint: disable=unused-argument
        '''
        '''

        return 'n'

    monkeypatch.setattr('builtins.input', mock_input)

    # 2. When.
    is_error_solved = error_solved()

    # 3. Then.
    assert not is_error_solved


def test_error_solved_invalid_input(capsys, monkeypatch):
    '''
    Ensures that when input is invalid, error_solved prompts the user
    to try again.
    '''

    # 1. Given.
    def make_mock_input():
        '''
        '''

        call_count = 0

        def mock_input(*args):
            # pylint: disable=unused-argument
            '''
            '''

            nonlocal call_count
            if call_count == 0:
                call_count += 1
                return 'a'
            return 'Y'
        return mock_input

    monkeypatch.setattr('builtins.input', make_mock_input())

    # 2. When.
    is_error_solved = error_solved()

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == 'a is not valid input! Please try again.\n'
    assert is_error_solved


def test_print_listening_for_errors(capsys):
    '''
    Ensures that print_listening_for_errors prints the proper output.

    "🥞 Listening for Python errors..."
    '''

    # 1. Given.

    # 2. When.
    print_listening_for_errors()

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == u'\U0001F95E Listening for Python errors...\n'
