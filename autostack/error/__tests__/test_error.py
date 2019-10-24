'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/22/2019
Overview: Tests for the error package.
'''

from autostack.error import (
    listen_for_errors,
    parse_output_for_error,
    get_error_from_traceback,
    handle_exception,
    error_solved,
    print_listening_for_errors,
)
from autostack.error.__tests__.mock_pipe import MockPipe
from autostack.error.__tests__.mock_handle_exception import MockHandleException


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
    mock_handle_exception = MockHandleException()

    monkeypatch.setattr(
        'autostack.error.handle_exception',
        mock_handle_exception.handle_exception
    )

    output = 'Not an error.'

    # 2. When.
    parse_output_for_error(output, None)

    # 3. Then.
    assert not mock_handle_exception.parameter
    assert not mock_handle_exception.was_called


def test_parse_output_for_error_with_error(monkeypatch):
    '''
    Ensures that handle_exception is called when an error
    is passed into parse_output_for_error.
    '''

    # 1. Given.
    mock_handle_exception = MockHandleException()

    monkeypatch.setattr(
        'autostack.error.handle_exception',
        mock_handle_exception.handle_exception
    )

    output = 'IndentationError: unexpected indent'

    # 2. When.
    parse_output_for_error(output, None)

    # 3. Then.
    assert mock_handle_exception.parameter == 'IndentationError'
    assert mock_handle_exception.was_called


def test_parse_output_for_error_traceback(monkeypatch):
    '''
    Ensures that handle_exception is called when a traceback
    is passed into parse_output_for_error.
    '''

    # 1. Given.
    mock_pipe = MockPipe([
        '    File "<stdin>", line 1, in <module>',
        'NameError: name \'xyz\' is not defined'
    ])
    mock_handle_exception = MockHandleException()
    output = 'Traceback (most recent call last):'

    def mock_get_error_from_traceback(pipe):
        # pylint: disable=unused-argument
        '''
        Mocks the get_error_from_traceback function.
        '''

        return 'NameError'

    monkeypatch.setattr(
        'autostack.error.handle_exception',
        mock_handle_exception.handle_exception
    )

    monkeypatch.setattr(
        'autostack.error.get_error_from_traceback',
        mock_get_error_from_traceback
    )

    # 2. When.
    parse_output_for_error(output, mock_pipe)

    # 3. Then.
    assert mock_handle_exception.parameter == 'NameError'
    assert mock_handle_exception.was_called


def test_parse_output_for_error_index_error(monkeypatch):
    '''
    Ensures that parse_output_for_error catches index errors.
    '''

    # 1. Given.
    mock_handle_exception = MockHandleException()

    monkeypatch.setattr(
        'autostack.error.handle_exception',
        mock_handle_exception.handle_exception
    )

    output = ''

    # 2. When.
    parse_output_for_error(output, None)

    # 3. Then.
    assert not mock_handle_exception.parameter
    assert not mock_handle_exception.was_called


def test_get_error_from_traceback():
    '''
    Ensures that the error description is returned from a
    traceback.
    '''

    # 1. Given.
    mock_pipe = MockPipe([
        '    File "<stdin>", line 1, in <module>',
        'NameError: name \'xyz\' is not defined'
    ])

    # 2. When.
    error = get_error_from_traceback(mock_pipe)

    # 3. Then.
    assert error == 'NameError'
    assert mock_pipe.get_readline_call_count() == 2


def test_handle_exception(capsys, monkeypatch):
    '''
    Ensures that posts are printed until the user inputs 'Y'
    to stop.
    '''

    # 1. Given.
    def make_mock_accepted_posts():
        '''
        Mocks the accepted_posts function.
        '''

        iteration = 0

        def mock_accepted_posts(*args):
            # pylint: disable=unused-argument
            '''
            Mocks the accepted_posts function which yields
            string digits instead of actual post bs4 soup.
            '''

            nonlocal iteration
            yield str(iteration)
            iteration += 1

        return mock_accepted_posts

    def mock_print_accepted_post(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the print_accepted_post function.
        '''

        return

    def mock_error_solved():
        '''
        Mocks the error_solved function.
        '''

        return True

    def mock_print_listening_for_errors():
        '''
        Mocks the print_listening_for_errors function.
        '''

        print(u'\U0001F95E Listening for Python errors...')

    monkeypatch.setattr(
        'autostack.error.accepted_posts',
        make_mock_accepted_posts()
    )

    monkeypatch.setattr(
        'autostack.error.print_accepted_post',
        mock_print_accepted_post
    )

    monkeypatch.setattr(
        'autostack.error.error_solved',
        mock_error_solved
    )

    monkeypatch.setattr(
        'autostack.error.print_listening_for_errors',
        mock_print_listening_for_errors
    )

    # 2. When.
    handle_exception('Error')

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == u'\U0001F95E Listening for Python errors...\n'


def test_error_solved_y(monkeypatch):
    '''
    Ensures that when 'Y' is inputted, error_solved returns True.
    '''

    # 1. Given.
    def mock_input(*args):
        # pylint: disable=unused-argument
        '''
        Mocks user input to be 'Y'.
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
        Mocks user input to be 'n'.
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
        Creates the mock function to mock user intput, and the
        input is different based on the call count.
        '''

        call_count = 0

        def mock_input(*args):
            # pylint: disable=unused-argument
            '''
            Mocks user input to be 'a' then 'Y'.
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
