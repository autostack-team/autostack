# pylint: disable=duplicate-code,too-many-lines
'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/12/2019
Overview: Tests for the config package.
'''

import json
import os
import shutil

from autostack.config import (
    get_config_path,
    eval_string,
    create_config,
    reset_config,
    print_config,
    get_config,
    get_config_hierarchically,
    set_config,
    create_config_object,
    populate_config_object,
    validate_config_key_value
)
from autostack.config.constants import (
    CONFIG_DIR_NAME,
    CONFIG_FILE_NAME,
    DEFAULT_CONFIG,
    GLOBAL_CONFIG_PATH
)

LOCAL_CONFIG_PATH = os.path.join(os.getcwd(), CONFIG_FILE_NAME)


def delete_config_file(global_):
    '''
    Deletes a global or local configuration file.
    '''

    try:
        if global_:
            os.remove(GLOBAL_CONFIG_PATH)
        else:
            os.remove(os.path.join(os.getcwd(), CONFIG_FILE_NAME))
    except FileNotFoundError:
        pass


def test_get_config_path_local():
    '''
    Ensures that get_config_path returns the correct
    local path.
    '''

    # 1. Given.

    # 2. When.
    path = get_config_path(False)

    # 3. Then.
    assert path == os.path.join(os.getcwd(), CONFIG_FILE_NAME)


def test_get_config_path_global():
    '''
    Ensures that get_config_path returns the correct
    global path.
    '''

    # 1. Given.

    # 2. When.
    path = get_config_path(True)

    # 3. Then.
    assert path == GLOBAL_CONFIG_PATH


def test_eval_string_string():
    '''
    Ensures that eval_string returns the appropriate
    type.
    '''

    # 1. Given.
    str_ = 'This is a string!'

    # 2. When.
    eval_result = eval_string(str_)

    # 3. Then.
    assert isinstance(eval_result, str)
    assert eval_result == str_


def test_eval_string_int():
    '''
    Ensures that eval_string returns the appropriate
    type.
    '''

    # 1. Given.
    str_ = '7'

    # 2. When.
    eval_result = eval_string(str_)

    # 3. Then.
    assert isinstance(eval_result, int)
    assert eval_result == int(str_)


def test_eval_string_float():
    '''
    Ensures that eval_string returns the appropriate
    type.
    '''

    # 1. Given.
    str_ = '7.87'

    # 2. When.
    eval_result = eval_string(str_)

    # 3. Then.
    assert isinstance(eval_result, float)
    assert eval_result == float(str_)


def test_eval_string_dict():
    '''
    Ensures that eval_string returns the appropriate
    type.
    '''

    # 1. Given.
    str_ = '{"name": "autostack"}'

    # 2. When.
    eval_result = eval_string(str_)

    # 3. Then.
    assert isinstance(eval_result, dict)
    assert eval_result == json.loads(str_)


def test_create_config_mkdirs():
    '''
    Ensures that create_config creates the global configuration
    file path, if needed.
    '''

    # Before.
    shutil.rmtree(
        os.path.join(os.getenv('HOME'), CONFIG_DIR_NAME),
        ignore_errors=True
    )

    # 1. Given.

    # 2. When.
    create_config(True)

    # 3. Then.
    assert os.path.exists(GLOBAL_CONFIG_PATH)
    assert json.loads(open(GLOBAL_CONFIG_PATH).read()) == DEFAULT_CONFIG


def test_create_config_default_local():
    '''
    Ensures that create_config creates the local, default
    configuration file.
    '''

    # 1. Given.

    # 2. When.
    create_config(False)

    # 3. Then.
    assert os.path.exists(LOCAL_CONFIG_PATH)
    assert json.loads(open(LOCAL_CONFIG_PATH).read()) == DEFAULT_CONFIG

    # After.
    delete_config_file(False)


def test_create_config_default_global():
    '''
    Ensures that create_config creates the global, default
    configuration file.
    '''

    # 1. Given.

    # 2. When.
    create_config(True)

    # 3. Then.
    assert os.path.exists(GLOBAL_CONFIG_PATH)
    assert json.loads(open(GLOBAL_CONFIG_PATH).read()) == DEFAULT_CONFIG


def test_create_config_nondefault_local():
    '''
    Ensures that create_config creates the local, nondefault
    configuration file.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}

    # 2. When.
    create_config(False, config)

    # 3. Then.
    assert os.path.exists(LOCAL_CONFIG_PATH)
    assert json.loads(open(LOCAL_CONFIG_PATH).read()) == config

    # After.
    delete_config_file(False)


def test_create_config_nondefault_global():
    '''
    Ensures that create_config creates the global, nondefault
    configuration file.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}

    # 2. When.
    create_config(True, config)

    # 3. Then.
    assert os.path.exists(GLOBAL_CONFIG_PATH)
    assert json.loads(open(GLOBAL_CONFIG_PATH).read()) == config

    # After.
    create_config(True)


def test_reset_config_local():
    '''
    Ensures the reset_config method properly resets the local configuration
    file.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}
    create_config(False, config)

    # 2. When.
    reset_config(False)

    # 3. Then.
    assert os.path.exists(LOCAL_CONFIG_PATH)
    assert json.loads(open(LOCAL_CONFIG_PATH).read()) == DEFAULT_CONFIG

    # After.
    delete_config_file(False)


def test_reset_config_global():
    '''
    Ensures the reset_config method properly resets the global configuration
    file.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}
    create_config(True, config)

    # 2. When.
    reset_config(True)

    # 3. Then.
    assert os.path.exists(GLOBAL_CONFIG_PATH)
    assert json.loads(open(GLOBAL_CONFIG_PATH).read()) == DEFAULT_CONFIG


def test_reset_config_file_not_found(capsys):
    '''
    Ensures the reset_config method handles file not found.
    '''

    # 1. Given.

    # 2. When.
    reset_config(False)

    # 3. Then.
    assert not os.path.exists(LOCAL_CONFIG_PATH)
    captured = capsys.readouterr()
    assert captured.out


def test_print_config_file_not_found(capsys):
    '''
    Ensures the print_config method handles file not found.
    '''

    # 1. Given.

    # 2. When.
    print_config(False)

    # 3. Then.
    assert not os.path.exists(LOCAL_CONFIG_PATH)
    captured = capsys.readouterr()
    assert captured.out


def test_print_config_local(capsys):
    '''
    Ensures the print_config properly prints locally.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}
    create_config(False, config)

    # 2. When.
    print_config(False)

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == (
        '\nCONFIGURATIONS:\n'
        '  language: GoLang\n'
        '\n'
    )

    # After.
    delete_config_file(False)


def test_print_config_global(capsys):
    '''
    Ensures the print_config properly prints globally.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}
    create_config(True, config)

    # 2. When.
    print_config(True)

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == (
        '\nCONFIGURATIONS:\n'
        '  language: GoLang\n'
        '\n'
    )

    # After.
    reset_config(True)


def test_print_config_key(capsys):
    '''
    Ensures the print_config properly prints key.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}
    create_config(False, config)

    # 2. When.
    print_config(False, 'language')

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == (
        '\nlanguage: GoLang\n\n'
    )

    # After.
    delete_config_file(False)


def test_print_config_invalid_key(capsys):
    '''
    Ensures the print_config handles invalid key.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}
    create_config(False, config)

    # 2. When.
    print_config(False, 'invalid_key')

    # 3. Then.
    captured = capsys.readouterr()
    assert 'doesn\'t exist' in captured.out

    # After.
    delete_config_file(False)


def test_print_config_invalid_file_contents(capsys):
    '''
    Ensures the print_config handles invalid file contents.
    '''

    # 1. Given.
    with open(LOCAL_CONFIG_PATH, 'w') as config_file:
        config_file.write('Invalid file!')

    # 2. When.
    print_config(False, 'invalid_key')

    # 3. Then.
    captured = capsys.readouterr()
    assert 'Failed to load the configuration file' in captured.out

    # After.
    delete_config_file(False)


def test_get_config_file_not_found(capsys):
    '''
    Ensures the get_config handles file not found.
    '''

    # 1. Given.

    # 2. When.
    get_config(False, 'language')

    # 3. Then.
    captured = capsys.readouterr()
    assert 'No autostack configuration file found' in captured.out


def test_get_config_file_not_found_no_errors(capsys):
    '''
    Ensures the get_config handles file not found with no errors to print.
    '''

    # 1. Given.

    # 2. When.
    get_config(False, 'language', False)

    # 3. Then.
    captured = capsys.readouterr()
    assert not captured.out


def test_get_config_invalid_file_contents(capsys):
    '''
    Ensures the get_config handles invalid file contents.
    '''

    # 1. Given.
    with open(LOCAL_CONFIG_PATH, 'w') as config_file:
        config_file.write('Invalid file!')

    # 2. When.
    get_config(False, 'language')

    # 3. Then.
    captured = capsys.readouterr()
    assert 'Failed to load the configuration file' in captured.out

    # After.
    delete_config_file(False)


def test_get_config_invalid_key(capsys):
    '''
    Ensures the get_config handles invalid keys.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}
    create_config(False, config)

    # 2. When.
    get_config(False, 'invalid_key')

    # 3. Then.
    captured = capsys.readouterr()
    assert 'doesn\'t exist' in captured.out

    # After.
    delete_config_file(False)


def test_get_config_valid_key_local():
    '''
    Ensures the get_config returns the appropriate key locally.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}
    create_config(False, config)

    # 2. When.
    key_value = get_config(False, 'language')

    # 3. Then.
    assert key_value == 'GoLang'

    # After.
    delete_config_file(False)


def test_get_config_valid_key_global():
    '''
    Ensures the get_config returns the appropriate key globally.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}
    create_config(True, config)

    # 2. When.
    key_value = get_config(True, 'language')

    # 3. Then.
    assert key_value == 'GoLang'

    # After.
    reset_config(True)


def test_get_config_hierarchically_valid_key_locally():
    '''
    Ensures the get_config_hierarchically returns the appropriate key
    locally.
    '''

    # 1. Given.
    config = {'language': 'GoLang'}
    create_config(False, config)

    # 2. When.
    key_value, global_ = get_config_hierarchically('language')

    # 3. Then.
    assert key_value == 'GoLang'
    assert not global_

    # After.
    delete_config_file(False)


def test_get_config_hierarchically_valid_key_globally():
    '''
    Ensures the get_config_hierarchically returns the appropriate key
    globally.
    '''

    # 1. Given.
    create_config(True)

    # 2. When.
    key_value, global_ = get_config_hierarchically('language')

    # 3. Then.
    assert key_value == DEFAULT_CONFIG['language']
    assert global_


def test_get_config_hierarchically_invalid_key():
    '''
    Ensures the get_config_hierarchically returns None for key not
    found.
    '''

    # 1. Given.

    # 2. When.
    result = get_config_hierarchically('invalid_key')

    # 3. Then.
    assert result is None


def test_set_config_file_not_found(capsys):
    '''
    Ensures the set_config handles file not found.
    '''

    # 1. Given.
    key = 'language'
    value = 'python'

    # 2. When.
    set_config(False, key, value)

    # 3. Then.
    captured = capsys.readouterr()
    assert 'No autostack configuration file found' in captured.out


def test_set_config_invalid_file_contents(capsys):
    '''
    Ensures the set_config handles invalid file contents.
    '''

    # 1. Given.
    key = 'language'
    value = 'python'
    with open(LOCAL_CONFIG_PATH, 'w') as config_file:
        config_file.write('Invalid file!')

    # 2. When.
    set_config(False, key, value)

    # 3. Then.
    captured = capsys.readouterr()
    assert 'Failed to load the configuration file' in captured.out

    # After.
    delete_config_file(False)


def test_set_config_local():
    '''
    Ensures the set_config properly sets key locally.
    '''

    # 1. Given.
    key = 'language'
    value = 'GoLang'
    create_config(False)

    # 2. When.
    set_config(False, key, value)

    # 3. Then.
    assert json.load(open(LOCAL_CONFIG_PATH))[key] == value

    # After.
    delete_config_file(False)


def test_set_config_global():
    '''
    Ensures the set_config properly sets key globally.
    '''

    # 1. Given.
    key = 'language'
    value = 'GoLang'
    create_config(True)

    # 2. When.
    set_config(True, key, value)

    # 3. Then.
    assert json.load(open(GLOBAL_CONFIG_PATH))[key] == value

    # After.
    reset_config(True)


def test_create_config_object_no_max_comments(monkeypatch):
    '''
    Ensures that create_config_object produces the correct
    configuration object with -1 supplied for max_comments.
    '''

    # 1. Given.
    language = 'python'
    order_by = 'Relevance'
    verified_only = False
    max_comments = -1

    def mock_populate_config_object(config):
        '''
        Mocks the populate_config_object method.
        '''

        return config

    monkeypatch.setattr(
        'autostack.config.populate_config_object',
        mock_populate_config_object
    )

    # 2. When.
    config_object = create_config_object(
        language,
        order_by,
        verified_only,
        max_comments
    )

    # 3. Then.
    assert config_object == {
        'language': language,
        'order_by': order_by,
        'verified_only': verified_only,
        'display_comments': None,
        'max_comments': None
    }


def test_create_config_object_max_comments(monkeypatch):
    '''
    Ensures that create_config_object produces the correct
    configuration object with a positive integer supplied for
    max_comments.
    '''

    # 1. Given.
    language = 'python'
    order_by = 'Relevance'
    verified_only = False
    max_comments = 3

    def mock_populate_config_object(config):
        '''
        Mocks the populate_config_object method.
        '''

        return config

    monkeypatch.setattr(
        'autostack.config.populate_config_object',
        mock_populate_config_object
    )

    # 2. When.
    config_object = create_config_object(
        language,
        order_by,
        verified_only,
        max_comments
    )

    # 3. Then.
    assert config_object == {
        'language': language,
        'order_by': order_by,
        'verified_only': verified_only,
        'display_comments': True,
        'max_comments': 3
    }


def test_populate_config_object_value_not_found(monkeypatch):
    '''
    Ensures that populate_config_object returns None if
    a valid value couldn't be found for each key.
    '''

    # 1. Given.
    config_object = {
        'language': 'python',
        'order_by': 'Relevance',
        'verified_only': True,
        'display_comments': None,
        'max_comments': None
    }

    def mock_get_config_hierarchically(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_config_hierarchically method.
        '''

        return None

    def mock_validate_config_key_value(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the validate_config_key_value method.
        '''

        return True

    monkeypatch.setattr(
        'autostack.config.get_config_hierarchically',
        mock_get_config_hierarchically
    )

    monkeypatch.setattr(
        'autostack.config.validate_config_key_value',
        mock_validate_config_key_value
    )

    # 2. When.
    result = populate_config_object(config_object)

    # 3. Then.
    assert result is None


def test_populate_config_object_invalid_value(monkeypatch):
    '''
    Ensures that populate_config_object returns None if
    a valid value couldn't be found for each key.
    '''

    # 1. Given.
    config_object = {
        'language': 'python',
        'order_by': 'Relevance',
        'verified_only': True,
        'display_comments': None,
        'max_comments': 3
    }

    def mock_get_config_hierarchically(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_config_hierarchically method.
        '''

        return ('invalid', True)

    def mock_validate_config_key_value(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the validate_config_key_value method.
        '''

        return False

    monkeypatch.setattr(
        'autostack.config.get_config_hierarchically',
        mock_get_config_hierarchically
    )

    monkeypatch.setattr(
        'autostack.config.validate_config_key_value',
        mock_validate_config_key_value
    )

    # 2. When.
    result = populate_config_object(config_object)

    # 3. Then.
    assert result is None


def test_populate_config_object_valid(monkeypatch):
    '''
    Ensures that populate_config_object returns None if
    a valid value couldn't be found for each key.
    '''

    # 1. Given.
    config_object = {
        'language': 'python',
        'order_by': None,
        'verified_only': True,
        'display_comments': True,
        'max_comments': 3
    }

    def mock_get_config_hierarchically(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_config_hierarchically method.
        '''

        return ('Relevance', True)

    def mock_validate_config_key_value(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the validate_config_key_value method.
        '''

        return True

    monkeypatch.setattr(
        'autostack.config.get_config_hierarchically',
        mock_get_config_hierarchically
    )

    monkeypatch.setattr(
        'autostack.config.validate_config_key_value',
        mock_validate_config_key_value
    )

    # 2. When.
    result = populate_config_object(config_object)

    # 3. Then.
    assert result is not None


def test_validate_config_key_value_none(capsys):
    '''
    Ensures that validate_config_key_value handles None
    value.
    '''

    # 1. Given.
    key = 'language'
    value = None
    global_ = True

    # 2. When.
    result = validate_config_key_value(key, value, global_)

    # 3. Then.
    captured = capsys.readouterr()
    assert 'Cannot find a configuration value for the key' in captured.out
    assert not result


def test_validate_config_key_value_display_comments(capsys):
    '''
    Ensures that validate_config_key_value handles invalid
    display_comments.
    '''

    # 1. Given.
    key = 'display_comments'
    value = 'invalid'
    global_ = True

    # 2. When.
    result = validate_config_key_value(key, value, global_)

    # 3. Then.
    captured = capsys.readouterr()
    assert 'is not valid in the configuration file' in captured.out
    assert not result


def test_validate_config_key_value_language(capsys):
    '''
    Ensures that validate_config_key_value handles invalid
    language.
    '''

    # 1. Given.
    key = 'language'
    value = 'GoLang'
    global_ = True

    # 2. When.
    result = validate_config_key_value(key, value, global_)

    # 3. Then.
    captured = capsys.readouterr()
    assert 'is not valid in the configuration file' in captured.out
    assert not result


def test_validate_config_key_max_comments(capsys):
    '''
    Ensures that validate_config_key_value handles invalid
    max_comments.
    '''

    # 1. Given.
    key = 'max_comments'
    value = 'invalid'
    value2 = -2
    global_ = True

    # 2. When.
    result = validate_config_key_value(key, value, global_)
    result2 = validate_config_key_value(key, value2, global_)

    # 3. Then.
    captured = capsys.readouterr()
    assert 'is not valid in the configuration file' in captured.out
    assert not result
    assert not result2


def test_validate_config_key_order_by(capsys):
    '''
    Ensures that validate_config_key_value handles invalid
    order_by.
    '''

    # 1. Given.
    key = 'order_by'
    value = 'invalid'
    global_ = True

    # 2. When.
    result = validate_config_key_value(key, value, global_)

    # 3. Then.
    captured = capsys.readouterr()
    assert 'is not valid in the configuration file' in captured.out
    assert not result


def test_validate_config_key_verified_only(capsys):
    '''
    Ensures that validate_config_key_value handles invalid
    verified_only.
    '''

    # 1. Given.
    key = 'verified_only'
    value = 'invalid'
    global_ = True

    # 2. When.
    result = validate_config_key_value(key, value, global_)

    # 3. Then.
    captured = capsys.readouterr()
    assert 'is not valid in the configuration file' in captured.out
    assert not result


def test_validate_config_key_invalid_key(capsys):
    '''
    Ensures that validate_config_key_value handles invalid
    keys.
    '''

    # 1. Given.
    key = 'invalid_key'
    value = 'invalid'
    global_ = True

    # 2. When.
    result = validate_config_key_value(key, value, global_)

    # 3. Then.
    captured = capsys.readouterr()
    assert 'is not valid.' in captured.out
    assert not result
