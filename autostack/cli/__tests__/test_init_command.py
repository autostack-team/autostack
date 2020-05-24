'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/12/2019
Overview: Tests for the config package.
'''

import json
import os

from click.testing import CliRunner
from PyInquirer import (
    ValidationError
)

from autostack.cli.init import (
    init_command,
    MaxCommentsValidator,
)

from autostack.config.constants import (
    CONFIG_FILE_NAME,
    DEFAULT_CONFIG,
    GLOBAL_CONFIG_PATH
)

LOCAL_CONFIG_PATH = os.path.join(os.getcwd(), CONFIG_FILE_NAME)


def delete_config_file(global_):
    '''
    Deletes a local or global configuration file.
    '''

    try:
        if global_:
            os.remove(GLOBAL_CONFIG_PATH)
        else:
            os.remove(LOCAL_CONFIG_PATH)
    except FileNotFoundError:
        pass


def test_init_command_default_local():
    '''
    Ensures that the default configuration file
    is written locally.
    '''

    # Before.
    delete_config_file(False)

    # 1. Given.
    runner = CliRunner()

    # 2. When.
    result = runner.invoke(init_command, '-d')

    # 3. Then.
    assert result.exit_code == 0
    assert os.path.exists(LOCAL_CONFIG_PATH)
    assert json.loads(open(LOCAL_CONFIG_PATH).read()) == DEFAULT_CONFIG

    # After.
    delete_config_file(False)


def test_init_command_default_global():
    '''
    Ensures that the default configuration file
    is written globally.
    '''

    # Before.
    delete_config_file(True)

    # 1. Given.
    runner = CliRunner()

    # 2. When.
    result = runner.invoke(init_command, ['-g', '-d'])

    # 3. Then.
    assert result.exit_code == 0
    assert os.path.exists(GLOBAL_CONFIG_PATH)
    assert json.loads(open(GLOBAL_CONFIG_PATH).read()) == DEFAULT_CONFIG

    # After.
    delete_config_file(True)


def test_init_command_no_comments_locally(monkeypatch):
    '''
    Ensures that the configuration file is written properly,
    locally if display_comments is False.
    '''

    # Before.
    delete_config_file(False)

    # 1. Given.
    runner = CliRunner()

    def mock_prompt(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the prompt method.
        '''

        return {
            'language': 'Python',
            'order_by': 'Relevance',
            'verified_only': True,
            'display_comments': False,
        }

    monkeypatch.setattr(
        'autostack.cli.init.prompt',
        mock_prompt
    )

    # 2. When.
    result = runner.invoke(init_command)

    # 3. Then.
    assert result.exit_code == 0
    assert os.path.exists(LOCAL_CONFIG_PATH)
    assert json.loads(open(LOCAL_CONFIG_PATH).read()) == DEFAULT_CONFIG

    # After.
    delete_config_file(False)


def test_init_command_no_comments_globally(monkeypatch):
    '''
    Ensures that the configuration file is written properly,
    globally if display_comments is False.
    '''

    # Before.
    delete_config_file(True)

    # 1. Given.
    runner = CliRunner()

    def mock_prompt(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the prompt method.
        '''

        return {
            'language': 'Python',
            'order_by': 'Relevance',
            'verified_only': True,
            'display_comments': False,
        }

    monkeypatch.setattr(
        'autostack.cli.init.prompt',
        mock_prompt
    )

    # 2. When.
    result = runner.invoke(init_command, '-g')

    # 3. Then.
    assert result.exit_code == 0
    assert os.path.exists(GLOBAL_CONFIG_PATH)
    assert json.loads(open(GLOBAL_CONFIG_PATH).read()) == DEFAULT_CONFIG

    # After.
    delete_config_file(True)


def test_init_command_with_comments_locally(monkeypatch):
    '''
    Ensures that the configuration file is written properly,
    locally if display_comments is True.
    '''

    # Before.
    delete_config_file(False)

    # 1. Given.
    runner = CliRunner()

    def mock_prompt_wrapper():
        '''
        Wrapper for the mock prompt method.
        '''

        call_count = 0

        def mock_prompt(*args):
            # pylint: disable=unused-argument
            '''
            Mocks the prompt method.
            '''

            nonlocal call_count
            call_count += 1

            if call_count == 1:
                return {
                    'language': 'Python',
                    'order_by': 'Relevance',
                    'verified_only': True,
                    'display_comments': True,
                }

            return {
                'language': 'Python',
                'order_by': 'Relevance',
                'verified_only': True,
                'display_comments': True,
                'max_comments': 3
            }

        return mock_prompt

    monkeypatch.setattr(
        'autostack.cli.init.prompt',
        mock_prompt_wrapper()
    )

    # 2. When.
    result = runner.invoke(init_command)

    # 3. Then.
    assert result.exit_code == 0
    assert os.path.exists(LOCAL_CONFIG_PATH)
    config_file = json.loads(open(LOCAL_CONFIG_PATH).read())
    assert config_file['language'] == 'Python'
    assert config_file['order_by'] == 'Relevance'
    assert config_file['verified_only']
    assert config_file['display_comments']
    assert config_file['max_comments'] == 3

    # After.
    delete_config_file(False)


def test_init_command_with_comments_globally(monkeypatch):
    '''
    Ensures that the configuration file is written properly,
    globally if display_comments is True.
    '''

    # Before.
    delete_config_file(True)

    # 1. Given.
    runner = CliRunner()

    def mock_prompt_wrapper():
        '''
        Wrapper for the mock prompt method.
        '''

        call_count = 0

        def mock_prompt(*args):
            # pylint: disable=unused-argument
            '''
            Mocks the prompt method.
            '''

            nonlocal call_count
            call_count += 1

            if call_count == 1:
                return {
                    'language': 'Python',
                    'order_by': 'Relevance',
                    'verified_only': True,
                    'display_comments': True,
                }

            return {
                'language': 'Python',
                'order_by': 'Relevance',
                'verified_only': True,
                'display_comments': True,
                'max_comments': 3
            }

        return mock_prompt

    monkeypatch.setattr(
        'autostack.cli.init.prompt',
        mock_prompt_wrapper()
    )

    # 2. When.
    result = runner.invoke(init_command, '-g')

    # 3. Then.
    assert result.exit_code == 0
    assert os.path.exists(GLOBAL_CONFIG_PATH)
    config_file = json.loads(open(GLOBAL_CONFIG_PATH).read())
    assert config_file['language'] == 'Python'
    assert config_file['order_by'] == 'Relevance'
    assert config_file['verified_only']
    assert config_file['display_comments']
    assert config_file['max_comments'] == 3

    # After.
    delete_config_file(True)


# ======================================================================
#
# VALIDATORS TESTS
#
# ======================================================================


def test_max_comments_validator_invalid_string_input():
    '''
    Ensures that the max validator only accepts positive
    integers.
    '''

    # 1. Given.
    class MockDocument():
        # pylint: disable=too-few-public-methods
        '''
        Mocks a document passed to max comments validator.
        '''

        def __init__(self):
            '''
            Init a mock document.
            '''

            self.text = 'string'

    validator = MaxCommentsValidator()

    # 2. When.
    try:
        validator.validate(MockDocument())
    except ValidationError:
        # 3. Then.
        assert True
        return

    assert False


def test_max_comments_validator_invalid_negative_input():
    '''
    Ensures that the max validator only accepts positive
    integers.
    '''

    # 1. Given.
    class MockDocument():
        # pylint: disable=too-few-public-methods
        '''
        Mocks a document passed to max comments validator.
        '''

        def __init__(self):
            '''
            Init a mock document.
            '''

            self.text = '-5'

    validator = MaxCommentsValidator()

    # 2. When.
    try:
        validator.validate(MockDocument())
    except ValidationError:
        # 3. Then.
        assert True
        return

    assert False


def test_max_comments_validator_valid_input():
    '''
    Ensures that the max validator only accepts positive
    integers.
    '''

    # 1. Given.
    class MockDocument():
        # pylint: disable=too-few-public-methods
        '''
        Mocks a document passed to max comments validator.
        '''

        def __init__(self):
            '''
            Init a mock document.
            '''

            self.text = '5'

    validator = MaxCommentsValidator()

    # 2. When.
    try:
        validator.validate(MockDocument())
    except ValidationError:
        # 3. Then.
        assert False
        return

    assert True
