'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 03/23/2020
Overview: Contains methods to print out common configuration errors.
'''


def print_file_not_found_error(path):
    '''
    Prints that the configuration file doesn't exist in the path.

    Parameter {string} path: the path to the non-existant configuration file.
    '''

    print('No autostack configuration file found in {}!'.format(path))


def print_key_error(key, path):
    '''
    Prints that the key doesn't exist in the configuration file.

    Parameter {string} key: the key that doesn't exist.
    Parameter {string} path: the path to the configuration file.
    '''

    print(
        'The key {} doesn\'t exist in the configuration file {}.'
        .format(key, path)
    )


def print_file_load_error(path):
    '''
    Prints that the configuration file at the specified path failed to load.

    Parameter {string} path: the path to the configuration file.
    '''

    print(
        'Failed to load the configuration file {}.'
        .format(path)
    )


def print_invalid_key_value(key, value, path):
    '''
    Prints that the key-value pair in the configuration file at the specified
    path is invalid.

    Parameter {string} key: the key.
    Parameter {any} key: the invalid value.
    Parameter {string} path: the path to the configuration file with the
    key-value pair.
    '''

    print(
        '{}\'s value {} is not valid in the configuration file {}.'
        .format(key, value, path)
    )
