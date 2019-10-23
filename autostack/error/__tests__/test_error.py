'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/22/2019
Overview: Tests for the error package.
'''

from autostack.error import (
    # listen_for_errors,
    # parse_output_for_error,
    # get_error_from_traceback,
    # handle_exception,
    error_solved,
    print_listening_for_errors,
)


def test_error_solved_y(monkeypatch):
    '''
    Ensures that when 'Y' is inputted, error_solved returns True.
    '''

    # 1. Given.
    def mock_input(*args):
        # pylint: disable=unused-argument
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
        call_count = 0

        def mock_input(*args):
            # pylint: disable=unused-argument
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
