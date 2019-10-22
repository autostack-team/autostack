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
    # error_solved,
    print_listening_for_errors,
)


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
