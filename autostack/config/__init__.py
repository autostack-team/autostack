'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/10/2019
Overview: the config package is used to interact with global and
project-specific configuration files for autostack.
'''

import json
import os

DEFAULT_CONFIG = {
    'languages': [
        'Python'
    ],
    'communities': [
        'Stack Overflow'
    ],
    'order_by': 'Relevance',
    'verified_only': True,
    'display_comments': False,
}
CONFIG_DIR_NAME = '.autostack'
CONFIG_FILE_NAME = '.autostack.json'
GLOBAL_CONFIG_PATH = os.path.join(
    os.getenv('HOME'),
    CONFIG_DIR_NAME,
    CONFIG_FILE_NAME
)


def print_file_not_found_error(path):
    '''
    Prints that the configuration file doesn't exist in the path.

    Parameter {string} path: the path to the non-existant configuration file.
    '''

    print('No autostack configuration file found in {}!'.format(path))


def print_key_error(key):
    '''
    Prints that the key doesn't exist in the global configuration file.

    Parameter {string} key: the key that doesn't exist.
    '''

    print(
        'The key {} doesn\'t exist in the global configuration file.'
        .format(key)
    )


def get_config_path(global_):
    '''
    Returns the local or global configuration path.

    Parameter {boolean} global_: whether to grab the local or global path.
    Returns {string}: the local or global path.
    '''

    if global_:
        return GLOBAL_CONFIG_PATH

    return os.path.join(os.getcwd(), CONFIG_FILE_NAME)


def create_config(global_=False, jsondata=None):
    '''
    Creates a configuration file.

    Parameter {boolean} global_: whether to create a global configuration file
    or a local configuration file in the current working directory.
    Parameter {dictionary} jsondata: the JSON data to write to the
    configuration file; otherwise, the default configuration is written.
    '''

    if (
            global_ and
            not os.path.exists(
                os.path.join(os.getenv('HOME'), CONFIG_DIR_NAME)
            )
    ):
        os.makedirs(os.path.join(os.getenv('HOME'), CONFIG_DIR_NAME))

    path = get_config_path(global_)

    with open(path, 'w') as config_file:
        json.dump(
            jsondata if jsondata else DEFAULT_CONFIG,
            config_file, indent=4
        )


def reset_config(global_=False):
    '''
    Resets a configuration file.

    Parameter {boolean} global_: whether to reset the global configuration file
    or the local configuration file in the current working directory.
    '''

    path = get_config_path(global_)

    try:
        with open(path, 'r+') as config_file:
            json.dump(DEFAULT_CONFIG, config_file, indent=4)
    except FileNotFoundError:
        print_file_not_found_error(path)


def print_config(global_=False):
    '''
    Prints out a configuration file.

    Parameter {boolean} global_: whether to print the global configuration
    file or the configuration file in the current directory.
    '''

    path = get_config_path(global_)

    try:
        with open(path, 'r') as config_file:
            config = json.loads(config_file.read())

            print('\nConfigurations:')
            for key, value in config.items():
                print('  {}: {}'.format(key, value))
            print('')
    except FileNotFoundError:
        print_file_not_found_error(path)


def get_config(global_, key):
    '''
    Returns the value for a key in a configuration file.

    Parameter {boolean} global_: whether to grab from the global configuration
    file or the local configuration file in the current working directory.
    Parameter {string} key: the key to get the value for.
    Returns {any}: the value for the key.
    '''

    path = get_config_path(global_)

    try:
        with open(GLOBAL_CONFIG_PATH, 'r') as global_config_file:
            config = json.loads(global_config_file.read())

            try:
                return config[key]
            except KeyError:
                print_key_error(key)
    except FileNotFoundError:
        print_file_not_found_error(path)


def set_config(global_, key, value):
    '''
    Sets the value for a key in a configuration file.

    Parameter {boolean} global_: whether to set in the global configuration
    file or the local configuration file in the current working directory.
    Parameter {string} key: the key to set a value for.
    Parameter {any} value: the value to assign to the key.
    '''

    path = get_config_path(global_)

    try:
        with open(GLOBAL_CONFIG_PATH, 'r+') as global_config_file:
            config = json.loads(global_config_file.read())

            try:
                config[key] = value
                global_config_file.seek(0)
                json.dump(config, global_config_file, indent=4)
            except KeyError:
                print_key_error(key)
    except FileNotFoundError:
        print_file_not_found_error(path)
