# pylint: disable=bare-except
'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/10/2019
Overview: Used to interact with global and local (project-specific) autostack
configuration files.
'''

import ast
import json
import os

from autostack.config.error_messages import (
    print_file_not_found_error,
    print_key_error,
    print_file_load_error
)

DEFAULT_CONFIG = {
    'languages': [
        'Python'
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


def get_config_path(global_):
    '''
    Returns a configuration file path.

    Parameter {boolean} global_: whether to grab the local or global
    configuration file path.
    Returns {string}: the local or global path.
    '''

    if global_:
        return GLOBAL_CONFIG_PATH

    return os.path.join(os.getcwd(), CONFIG_FILE_NAME)


def eval_string(string):
    '''
    Casts a string into native types: int, float, list, dict, etc.

    Parameter {string} string: the string to evaluate.
    Returns {any}: the evaluated value.
    '''

    try:
        return json.loads(string)
    except:
        pass

    try:
        return ast.literal_eval(string)
    except:
        pass

    return string


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
    Resets a configuration file to the default configuration.

    Parameter {boolean} global_: whether to reset the global configuration file
    or the local configuration file in the current working directory.
    '''

    path = get_config_path(global_)

    # Attempt to open the configuration file.
    try:
        with open(path, 'r+') as config_file:
            config_file.truncate(0)
            json.dump(DEFAULT_CONFIG, config_file, indent=4)
    # The file doesn't exist.
    except FileNotFoundError:
        print_file_not_found_error(path)


def print_config(global_=False, key=None):
    '''
    Prints out the configuration file, or a key-value pair in the
    configuration file. If a key is passed in, only print that key-value
    pair.

    Parameter {boolean} global_: whether to print the global configuration
    file or the location configuration file in the current working directory.
    Parameter {string} key: the key of the key-value pair to print.
    '''

    path = get_config_path(global_)
    jsondata = None

    # Attempt to open the configuration file.
    try:
        with open(path, 'r') as config_file:
            jsondata = json.loads(config_file.read())

            # Try to return the value from the specified key.
            if key:
                try:
                    print('\n{}: {}\n'.format(key, jsondata[key]))
                except KeyError:
                    print_key_error(key, path)
                return

            print('\nCONFIGURATIONS:')
            for key, value in jsondata.items():
                print('  {}: {}'.format(key, value))
            print('')
    # The file doesn't exist.
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
    jsondata = None

    # Attempt to open the configuration file.
    try:
        with open(path, 'r') as config_file:
            try:
                jsondata = json.loads(config_file.read())
            # The file could not be opened.
            except:
                print_file_load_error(path)
                return

            # Try to return the value from the specified key.
            try:
                return jsondata[key]
            except KeyError:
                print_key_error(key, path)
    # The file doesn't exist.
    except FileNotFoundError:
        print_file_not_found_error(path)
        return


def set_config(global_, key, value):
    '''
    Sets the value for a key in a configuration file.

    Parameter {boolean} global_: whether to set in the global configuration
    file or the local configuration file in the current working directory.
    Parameter {string} key: the key to set a value for.
    Parameter {any} value: the value to assign to the key.
    '''

    path = get_config_path(global_)
    jsondata = None

    # Attempt to open the configuration file.
    try:
        with open(path, 'r') as config_file:
            try:
                jsondata = json.loads(config_file.read())
            # The file could not be opened.
            except:
                print_file_load_error(path)
                return
    # The file doesn't exist.
    except FileNotFoundError:
        print_file_not_found_error(path)
        return

    # Write the key-value pair to the configuration file.
    jsondata[key] = eval_string(value)
    with open(path, 'w') as config_file:
        json.dump(jsondata, config_file, indent=4)
