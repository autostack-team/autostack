'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 03/23/2020
Overview: Contains 
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
    Prints that the file at the specified path failed to load.

    Parameter {string} path: the path to the configuration file.
    '''

    print(
        'Failed to load the configuration file {}.'
        .format(path)
    )
