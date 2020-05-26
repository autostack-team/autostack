'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/25/2019
Overview: Tests for the config package.
'''


from autostack.config.error_messages import (
    print_file_not_found_error,
    print_key_error,
    print_file_load_error,
    print_invalid_key_value
)


def test_print_file_not_found_error(capsys):
    '''
    Ensure that print_file_not_found prints the proper
    output.
    '''

    # 1. Given.
    path = '/path'

    # 2. When.
    print_file_not_found_error(path)

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == (
        'No autostack configuration file found in {}!\n'
        .format(path)
    )


def test_print_key_error(capsys):
    '''
    Ensure that print_key_error prints the proper
    output.
    '''

    # 1. Given.
    key = 'language'
    path = '/path'

    # 2. When.
    print_key_error(key, path)

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == (
        'The key {} doesn\'t exist in the configuration file {}.\n'
        .format(key, path)
    )


def test_print_file_load_error(capsys):
    '''
    Ensure that print_file_load_error prints the proper
    output.
    '''

    # 1. Given.
    path = '/path'

    # 2. When.
    print_file_load_error(path)

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == (
        'Failed to load the configuration file {}.\n'
        .format(path)
    )


def test_print_invalid_key_value(capsys):
    '''
    Ensure that print_invalid_key_value prints the proper
    output.
    '''

    # 1. Given.
    key = 'language'
    value = 'R'
    path = '/path'

    # 2. When.
    print_invalid_key_value(key, value, path)

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == (
        '{}\'s value {} is not valid in the configuration file {}.\n'
        .format(key, value, path)
    )
