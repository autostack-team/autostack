'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/31/2020
Overview: Tests for the error python package.
'''

from autostack.error.python import (
    parse_output_for_error,
    get_error_from_traceback
)


def test_parse_output_for_error_syntax_error():
    '''
    Ensures that parse_output_for_error handles syntax errors.
    '''

    # 1. Given.
    output = 'IndentationError: unexpected indent'

    # 2. When.
    error = parse_output_for_error(output, None)

    # 3. Then.
    assert error == 'IndentationError'


def test_parse_output_for_error_traceback(monkeypatch):
    '''
    Ensures that parse_output_for_error handles tracebacks.
    '''

    # 1. Given.
    output = 'Traceback (most recent call last):'
    call_count = 0

    def mock_get_error_from_traceback(*args):
        # pylint: disable=unused-argument
        '''
        Mock get_error_from_traceback method.
        '''

        nonlocal call_count
        call_count += 1

    monkeypatch.setattr(
        'autostack.error.python.get_error_from_traceback',
        mock_get_error_from_traceback
    )

    # 2. When.
    parse_output_for_error(output, None)

    # 3. Then.
    assert call_count == 1


def test_parse_output_for_error_index_error():
    '''
    Ensures that parse_output_for_error handles index
    errors when parsing output that cannot be split.
    '''

    # 1. Given.
    output = ''

    # 2. When.
    error = parse_output_for_error(output, None)

    # 3. Then.
    assert error is None


def test_parse_output_for_error_no_error():
    '''
    Ensures that parse_output_for_error returns None
    if the output is not an error.
    '''

    # 1. Given.
    output = 'This is not an error.'

    # 2. When.
    error = parse_output_for_error(output, None)

    # 3. Then.
    assert error is None


def test_get_error_from_traceback():
    '''
    Ensures that get_error_from_traceback reads from
    the pipe until it finds the error description.
    '''

    # 1. Given.
    class MockPipe():
        # pylint: disable=too-few-public-methods
        '''
        Mocks a fifo pipe object.
        '''

        def __init__(self):
            '''
            Inits a fifo pipe object.
            '''

            self.call_count = 0

        def readline(self):
            '''
            Mocks the readline method of a pipe.
            '''

            self.call_count += 1

            if self.call_count == 1:
                return 'Not an error.'

            if self.call_count == 2:
                return 'Not an error.'

            return 'ErrorDescription: ...'

    pipe = MockPipe()

    # 2. When.
    error = get_error_from_traceback(pipe)

    # 3. Then.
    assert error == 'ErrorDescription'
    assert pipe.call_count == 3
