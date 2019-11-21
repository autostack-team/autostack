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
    handle_user_input,
    print_listening_for_errors,
    clear_terminal,
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
    def mock_accepted_posts(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the accepted_posts function which yields
        strings instead of actual post bs4 soup.
        '''

        i = 1

        while i:
            yield str(i)

    def mock_print_accepted_post(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the print_accepted_post function.
        '''

        return

    def make_mock_handle_user_input():
        '''
        Creates the mock function to mock handle_user_input, and the
        input is different based on the call count.
        '''

        call_count = 0

        def mock_handle_user_input():
            '''
            Mocks the handle_user_input function.
            '''

            nonlocal call_count
            call_count += 1

            if call_count == 1:
                return False

            if call_count == 2:
                return 'Custom query'

            return True

        return mock_handle_user_input

    def mock_clear_terminal():
        '''
        Mocks the clear_terminal function.
        '''

        return

    def mock_print_listening_for_errors():
        '''
        Mocks the print_listening_for_errors function.
        '''

        print(u'\U0001F95E Listening for Python errors...')

    monkeypatch.setattr(
        'autostack.error.accepted_posts',
        mock_accepted_posts
    )

    monkeypatch.setattr(
        'autostack.error.print_accepted_post',
        mock_print_accepted_post
    )

    monkeypatch.setattr(
        'autostack.error.handle_user_input',
        make_mock_handle_user_input()
    )

    monkeypatch.setattr(
        'autostack.error.clear_terminal',
        mock_clear_terminal
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


def test_handle_user_input_y(monkeypatch):
    '''
    Ensures that when 'Y' is inputted, handle_user_input returns True.
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
    user_input = handle_user_input()

    # 3. Then.
    assert user_input is True


def test_handle_user_input_n(monkeypatch):
    '''
    Ensures that when 'n' is inputted, handle_user_input returns False.
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
    user_input = handle_user_input()

    # 3. Then.
    assert not user_input


def test_handle_user_input_custom_query(monkeypatch):
    '''
    Ensures that when input isn't Y/n, handle_user_input returns the input.
    '''

    # 1. Given.
    def make_mock_input():
        '''
        Creates the mock function to mock user input, and the
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
                return 'Custom query'
            return 'Y'
        return mock_input

    monkeypatch.setattr('builtins.input', make_mock_input())

    # 2. When.
    user_input = handle_user_input()

    # 3. Then.
    assert user_input == 'Custom query'


def test_print_listening_for_errors(capsys, monkeypatch):
    '''
    Ensures that print_listening_for_errors prints the proper output.

    "🥞 Listening for Python errors..."
    '''

    # 1. Given.
    def mock_clear_terminal():
        '''
        Mocks the clear_terminal function.
        '''

        return

    monkeypatch.setattr(
        'autostack.error.clear_terminal',
        mock_clear_terminal
    )

    # 2. When.
    print_listening_for_errors()

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == u'\U0001F95E Listening for Python errors...\n'


def test_clear_terminal(capsys):
    '''
    Ensures that clear_terminal clears the terminal.
    '''

    # 1. Given.

    # 2. When.
    clear_terminal()

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == '\x1bc\n'  # Same as u'\033c'
