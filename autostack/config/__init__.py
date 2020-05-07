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

from autostack.config.constants import (
    CONFIG_DIR_NAME,
    CONFIG_FILE_NAME,
    DEFAULT_CONFIG,
    GLOBAL_CONFIG_PATH,
    SUPPORTED_CONFIG_KEYS,
    SUPPORTED_LANGUAGES,
    SUPPORTED_ORDER_BY_FILTERS
)

from autostack.config.error_messages import (
    print_file_not_found_error,
    print_key_error,
    print_file_load_error,
    print_invalid_key_value
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

    Parameter {string} string: the string to cast into its native type.
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


def get_config(global_, key, display_errors=True):
    '''
    Returns the value for a key in a configuration file.

    Parameter {boolean} global_: whether to grab from the global configuration
    file or the local configuration file in the current working directory.
    Parameter {string} key: the key to get the value for.
    Returns {any}: the value for the key.
    Parameter {boolean} display_errors: whether or not to print out error such as
    file not found, or if the file can't be opened. Defaults to True.
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
                if display_errors:
                    print_file_load_error(path)
                return

            # Try to return the value from the specified key.
            try:
                return jsondata[key]
            except KeyError:
                if display_errors:
                    print_key_error(key, path)
    # The file doesn't exist.
    except FileNotFoundError:
        if display_errors:
            print_file_not_found_error(path)
        return


def get_config_hierarchically(key):
    '''
    Returns the value for a key in a configuration file, hierarchically. If a
    local configuration file exists, it's searched for there. If the key is not
    there, it's searched for in the global configuration file. If not found,
    None is returned.

    Parameter {string} key: the key to get the value for.
    Returns {tuple} the value for the key and whether or not it was global.
    '''

    if get_config(False, key, False) is not None:
        return (get_config(False, key), False)
    elif get_config(True, key, False) is not None:
        return (get_config(True, key), True)
    else:
        return None


def set_config(global_, key, value, display_errors=True):
    '''
    Sets the value for a key in a configuration file.

    Parameter {boolean} global_: whether to set in the global configuration
    file or the local configuration file in the current working directory.
    Parameter {string} key: the key to set a value for.
    Parameter {any} value: the value to assign to the key.
    Parameter {boolean} display_errors: whether or not to print out error such as
    file not found, or if the file can't be opened. Defaults to True.
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
                if display_errors:
                    print_file_load_error(path)
                return
    # The file doesn't exist.
    except FileNotFoundError:
        if display_errors:
            print_file_not_found_error(path)
        return

    # Write the key-value pair to the configuration file.
    jsondata[key] = eval_string(value)
    with open(path, 'w') as config_file:
        json.dump(jsondata, config_file, indent=4)


def create_config_object(language, order_by, verified_only, display_comments, no_comments):
    '''
    Creates a configuration object of the form:

    {
        'language': ...,
        'order_by': ...,
        'verified_only': ...,
        'diplay_comments': ...
    }

    If a valid configuration value cannot be found for a key in a local or the global
    configuration files, None is returned. Otherwise, the config object is returned.

    This function is intended to be used only with the click commands that take
    in configuration objects.

    Parameter {string|None} language: the config language.
    Parameter {string|None} order_by: the config order_by.
    Parameter {boolean|None} verified_only: the config verified_only.
    Parameter {int|None} display_comments: the max comments to display.
    Parameter {boolean|None} no_comments: don't display comments.
    Returns {dictionary|None} the configuration object, or None.
    '''

    config = {
        'language': language,
        'order_by': order_by,
        'verified_only': verified_only,
        'display_comments': None,
        'max_comments': None
    }

    if no_comments:
        config['display_comments'] = False
        del config['max_comments']
    elif display_comments is not None:
        config['display_comments'] = True
        config['max_comments'] = display_comments

    config = populate_config_object(config)

    return config


def populate_config_object(config):
    '''
    Given a configuration object, try to populate a key's value from a
    local or the global configuration file, if its value is None.

    If any of the key's cannot be assigned a valid value, None
    is returned.

    Parameter {dictionary} config: the configuration object to populate.
    Returns {dictionary|None} the populated configuration object, or None.
    '''

    valid = False

    for key, value in config.items():
        if value is None:
            new_value, global_ = get_config_hierarchically(key)
            config[key] = new_value
            valid = validate_config_key_value(key, new_value, global_)

    if valid:
        return config
    else:
        return None


def validate_config_key_value(key, value, global_):
    '''
    Given a key-value pair, and whether it was in a local or the global
    configuration file, determine if the value is valid.

    Parameter {string} key: the key to validate its value.
    Parameter {any} value: the value to verify.
    Parameter {boolean} global_: whether or not the key-value pair was
    grabbed from the global configuration file.
    '''

    valid = True
    path = get_config_path(global_)

    # Validate the value.
    if value is None:
        print('Cannot find a configuration value for the key {}.'.format(key))
        valid = False
    elif key == 'display_comments' and type(value) != bool:
        print_invalid_key_value(key, value, path)
        valid = False
    elif key == 'language' and value not in SUPPORTED_LANGUAGES:
        print_invalid_key_value(key, value, path)
        valid = False
    elif key == 'max_comments' and type(value) is not int and value < 1:
        print_invalid_key_value(key, value, path)
        valid = False
    elif key == 'order_by' and value not in SUPPORTED_ORDER_BY_FILTERS:
        print_invalid_key_value(key, value, path)
        valid = False
    elif key == 'verified_only' and type(value) != bool:
        print(value)
        print_invalid_key_value(key, value, path)
        valid = False

    return valid
