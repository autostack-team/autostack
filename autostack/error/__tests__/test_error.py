'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/22/2019
Overview: Tests for the error package.
'''

from autostack.error import (
    listen_for_errors,
    parse_output_for_error,
    handle_error,
    handle_user_input,
    print_listening_for_errors
)


class MockPipe:
    '''
    Mocks a pipe.
    '''

    def __init__(self, readline_returns=''):
        '''
        Initializes a mock pipe with readline return values and
        the number of readline calls set to 0.
        '''

        self.readline_returns = readline_returns
        self.readline_call_count = 0

    def readline(self):
        '''
        Returns a value for readline, based on the current call
        count value.
        '''

        readline_val = self.readline_returns[self.readline_call_count]
        self.readline_call_count += 1
        return readline_val

    def get_readline_call_count(self):
        '''
        Returns the readline method call count.
        '''

        return self.readline_call_count


class MockErrorLibrary():
    # pylint: disable=too-few-public-methods
    '''
    Mocks an error_library object.
    '''

    def __init__(self, return_error):
        '''
        Init a error_library object.
        '''

        self.return_error = return_error

    def parse_output_for_error(self, *args):
        # pylint: disable=unused-argument
        '''
        Mocks parse_output_for_error method.
        '''

        if self.return_error:
            return 'Error'

        return None


def mock_do_nothing(*args):
    # pylint: disable=unused-argument
    '''
    Mocks method that does nothing.
    '''

    return


def mock_posts(*args):
    # pylint: disable=unused-argument
    '''
    Mocks the posts generator.
    '''

    count = 1

    while True:
        yield count
        count += 1


def test_listen_for_errors(monkeypatch):
    '''
    Ensures that listen_for_errors reads output from a pipe until
    empty string is returned. In this case, that'd be 3 calls.
    '''

    # 1. Given.
    config = {
        'language': 'language'
    }

    monkeypatch.setattr(
        'autostack.error.importlib.import_module',
        mock_do_nothing
    )

    monkeypatch.setattr(
        'autostack.print_logo',
        mock_do_nothing
    )

    monkeypatch.setattr(
        'autostack.error.print_listening_for_errors',
        mock_do_nothing
    )

    monkeypatch.setattr(
        'autostack.error.parse_output_for_error',
        mock_do_nothing
    )

    mockpipe = MockPipe(['output', 'output', ''])

    # 2. When.
    listen_for_errors(mockpipe, config)

    # 3. Then.
    assert mockpipe.get_readline_call_count() == 3


def test_parse_output_for_error_non_error(monkeypatch):
    '''
    Ensures that handle_error is never called when a non-error
    is passed into parse_output_for_error.
    '''

    # 1. Given.
    call_count = 0

    def mock_handle_error(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the handle_error method.
        '''

        nonlocal call_count
        call_count += 1

    monkeypatch.setattr(
        'autostack.error.print_listening_for_errors',
        mock_do_nothing
    )

    monkeypatch.setattr(
        'autostack.error.handle_error',
        mock_handle_error
    )

    # 2. When.
    parse_output_for_error('Not an error.', None, MockErrorLibrary(False), {})

    # 3. Then.
    assert not call_count


def test_parse_output_for_error_with_error(monkeypatch):
    '''
    Ensures that handle_exception is called when an error
    is passed into parse_output_for_error.
    '''

    # 1. Given.
    call_count = 0

    def mock_handle_error(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the handle_error method.
        '''

        nonlocal call_count
        call_count += 1

    monkeypatch.setattr(
        'autostack.error.print_listening_for_errors',
        mock_do_nothing
    )

    monkeypatch.setattr(
        'autostack.error.handle_error',
        mock_handle_error
    )

    # 2. When.
    parse_output_for_error('Not an error.', None, MockErrorLibrary(True), {})

    # 3. Then.
    assert call_count


def test_handle_error_first_answer_solved(monkeypatch):
    '''
    Ensures that only one post is printed.
    '''

    # 1. Given.
    call_count = 0

    def mock_print_post(*args):
        # pylint: disable=unused-argument
        '''
        Mocks print_post method.
        '''

        nonlocal call_count
        call_count += 1

    def mock_handle_user_input():
        '''
        Mocks handle_user_input method.
        '''

        return True

    monkeypatch.setattr(
        'autostack.error.posts',
        mock_posts
    )

    monkeypatch.setattr(
        'autostack.error.print_post',
        mock_print_post
    )

    monkeypatch.setattr(
        'autostack.error.handle_user_input',
        mock_handle_user_input
    )

    # 2. When.
    handle_error('', {})

    # 3. Then.
    assert call_count == 1


def test_handle_error_first_multiple_posts(monkeypatch):
    '''
    Ensures that multiple posts are printed, until True
    is returned for user input.
    '''

    # 1. Given.
    call_count = 0

    def mock_print_post(*args):
        # pylint: disable=unused-argument
        '''
        Mocks print_post method.
        '''

        nonlocal call_count
        call_count += 1

    def mock_handle_user_input_wrapper():
        '''
        Mock handle_user_input wrapper for input count
        tracking.
        '''

        input_count = 0

        def mock_handle_user_input():
            '''
            Mocks handle_user_input method.
            '''

            nonlocal input_count
            input_count += 1

            if input_count == 3:
                return True

            return False

        return mock_handle_user_input

    monkeypatch.setattr(
        'autostack.error.posts',
        mock_posts
    )

    monkeypatch.setattr(
        'autostack.error.print_post',
        mock_print_post
    )

    monkeypatch.setattr(
        'autostack.error.handle_user_input',
        mock_handle_user_input_wrapper()
    )

    # 2. When.
    handle_error('', {})

    # 3. Then.
    assert call_count == 3


def test_handle_error_first_custom_query(monkeypatch):
    '''
    Ensures that handle_error handles custom queries.
    '''

    # 1. Given.
    call_count = 0

    def mock_print_post(*args):
        # pylint: disable=unused-argument
        '''
        Mocks print_post method.
        '''

        nonlocal call_count
        call_count += 1

    def mock_handle_user_input_wrapper():
        '''
        Mock handle_user_input wrapper for input count
        tracking.
        '''

        input_count = 0

        def mock_handle_user_input():
            '''
            Mocks handle_user_input method.
            '''

            nonlocal input_count
            input_count += 1

            if input_count == 2:
                return True

            return 'Custom query.'

        return mock_handle_user_input

    monkeypatch.setattr(
        'autostack.error.posts',
        mock_posts
    )

    monkeypatch.setattr(
        'autostack.error.print_post',
        mock_print_post
    )

    monkeypatch.setattr(
        'autostack.error.handle_user_input',
        mock_handle_user_input_wrapper()
    )

    # 2. When.
    handle_error('', {})

    # 3. Then.
    assert call_count == 2


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
                return 'custom query'
            return 'Y'
        return mock_input

    monkeypatch.setattr('builtins.input', make_mock_input())

    # 2. When.
    user_input = handle_user_input()

    # 3. Then.
    assert user_input == 'custom query'


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
    assert captured.out == u'\U0001F95E Listening for errors...\n'
