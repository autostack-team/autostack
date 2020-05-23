'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/12/2019
Overview: Tests for the config package.
'''

from click.testing import CliRunner

from autostack.cli.config import config_command


def test_autostack_config_with_no_command():
    '''
    When the autostack config command is executed with no command,
    ensure that the usage message is printed.
    '''

    # 1. Given.
    runner = CliRunner()

    # 2. When.
    result = runner.invoke(config_command)

    # 3. Then.
    assert result.exit_code == 0
    assert 'Usage:' in result.output


def test_autostack_config_reset_local(monkeypatch):
    '''
    Ensure that the reset_config method is called with
    a local context.
    '''

    # 1. Given.
    runner = CliRunner()
    reset_config_call_count = 0
    ctx = None

    def mock_reset_config(global_):
        '''
        Mocks the reset_config method.
        '''

        nonlocal reset_config_call_count
        nonlocal ctx

        reset_config_call_count += 1

        if global_:
            ctx = 'Global'
        else:
            ctx = 'Local'

    monkeypatch.setattr(
        'autostack.cli.config.reset_config',
        mock_reset_config
    )

    # 2. When.
    result = runner.invoke(config_command, ['reset'])

    # 3. Then.
    assert result.exit_code == 0
    assert reset_config_call_count == 1
    assert ctx == 'Local'


def test_autostack_config_reset_global(monkeypatch):
    '''
    Ensure that the reset_config method is called with
    a global context.
    '''

    # 1. Given.
    runner = CliRunner()
    reset_config_call_count = 0
    ctx = None

    def mock_reset_config(global_):
        '''
        Mocks the reset_config method.
        '''

        nonlocal reset_config_call_count
        nonlocal ctx

        reset_config_call_count += 1

        if global_:
            ctx = 'Global'
        else:
            ctx = 'Local'

    monkeypatch.setattr(
        'autostack.cli.config.reset_config',
        mock_reset_config
    )

    # 2. When.
    result = runner.invoke(config_command, ['-g', 'reset'])

    # 3. Then.
    assert result.exit_code == 0
    assert reset_config_call_count == 1
    assert ctx == 'Global'


def test_autostack_config_set_no_key_or_value():
    '''
    Ensure that the set command errors out when no key or
    value is passed in.
    '''

    # 1. Given.
    runner = CliRunner()

    # 2. When.
    result = runner.invoke(config_command, ['set'])

    # 3. Then.
    assert result.exit_code == 2


def test_autostack_config_set_no_value():
    '''
    Ensure that the set command errors out when no value is
    passed in.
    '''

    # 1. Given.
    runner = CliRunner()

    # 2. When.
    result = runner.invoke(config_command, ['set', 'language'])

    # 3. Then.
    assert result.exit_code == 2


def test_autostack_config_set_local(monkeypatch):
    '''
    Ensure that the set_config method is called with
    a local context.
    '''

    # 1. Given.
    runner = CliRunner()
    key_to_pass = 'language'
    value_to_pass = 'python'
    set_config_call_count = 0
    given_key = None
    given_value = None
    ctx = None

    def mock_set_config(global_, key, value):
        '''
        Mocks the set_config method.
        '''

        nonlocal set_config_call_count
        nonlocal given_key
        nonlocal given_value
        nonlocal ctx

        set_config_call_count += 1
        given_key = key
        given_value = value

        if global_:
            ctx = 'Global'
        else:
            ctx = 'Local'

    monkeypatch.setattr(
        'autostack.cli.config.set_config',
        mock_set_config
    )

    # 2. When.
    result = runner.invoke(config_command, ['set', key_to_pass, value_to_pass])

    # 3. Then.
    assert result.exit_code == 0
    assert set_config_call_count == 1
    assert given_key == key_to_pass
    assert given_value == value_to_pass
    assert ctx == 'Local'


def test_autostack_config_set_global(monkeypatch):
    '''
    Ensure that the set_config method is called with
    a global context.
    '''

    # 1. Given.
    runner = CliRunner()
    key_to_pass = 'language'
    value_to_pass = 'python'
    set_config_call_count = 0
    given_key = None
    given_value = None
    ctx = None

    def mock_set_config(global_, key, value):
        '''
        Mocks the set_config method.
        '''

        nonlocal set_config_call_count
        nonlocal given_key
        nonlocal given_value
        nonlocal ctx

        set_config_call_count += 1
        given_key = key
        given_value = value

        if global_:
            ctx = 'Global'
        else:
            ctx = 'Local'

    monkeypatch.setattr(
        'autostack.cli.config.set_config',
        mock_set_config
    )

    # 2. When.
    result = runner.invoke(
        config_command,
        ['-g', 'set', key_to_pass, value_to_pass]
    )

    # 3. Then.
    assert result.exit_code == 0
    assert set_config_call_count == 1
    assert given_key == key_to_pass
    assert given_value == value_to_pass
    assert ctx == 'Global'


def test_autostack_config_get_no_key():
    '''
    Ensure that the get command errors out when no key is
    passed in.
    '''

    # 1. Given.
    runner = CliRunner()

    # 2. When.
    result = runner.invoke(config_command, ['get'])

    # 3. Then.
    assert result.exit_code == 2


def test_autostack_config_get_local(monkeypatch):
    '''
    Ensure that the print_config method is called with
    a local context.
    '''

    # 1. Given.
    runner = CliRunner()
    key_to_pass = 'language'
    print_config_call_count = 0
    given_key = None
    ctx = None

    def mock_print_config(global_, key):
        '''
        Mocks the print_config method.
        '''

        nonlocal print_config_call_count
        nonlocal given_key
        nonlocal ctx

        print_config_call_count += 1
        given_key = key

        if global_:
            ctx = 'Global'
        else:
            ctx = 'Local'

    monkeypatch.setattr(
        'autostack.cli.config.print_config',
        mock_print_config
    )

    # 2. When.
    result = runner.invoke(config_command, ['get', key_to_pass])

    # 3. Then.
    assert result.exit_code == 0
    assert print_config_call_count == 1
    assert given_key == key_to_pass
    assert ctx == 'Local'


def test_autostack_config_get_global(monkeypatch):
    '''
    Ensure that the print_config method is called with
    a global context.
    '''

    # 1. Given.
    runner = CliRunner()
    key_to_pass = 'language'
    print_config_call_count = 0
    given_key = None
    ctx = None

    def mock_print_config(global_, key):
        '''
        Mocks the print_config method.
        '''

        nonlocal print_config_call_count
        nonlocal given_key
        nonlocal ctx

        print_config_call_count += 1
        given_key = key

        if global_:
            ctx = 'Global'
        else:
            ctx = 'Local'

    monkeypatch.setattr(
        'autostack.cli.config.print_config',
        mock_print_config
    )

    # 2. When.
    result = runner.invoke(config_command, ['-g', 'get', key_to_pass])

    # 3. Then.
    assert result.exit_code == 0
    assert print_config_call_count == 1
    assert given_key == key_to_pass
    assert ctx == 'Global'


def test_autostack_config_list_local(monkeypatch):
    '''
    Ensure that the print_config method is called with
    a local context.
    '''

    # 1. Given.
    runner = CliRunner()
    print_config_call_count = 0
    ctx = None

    def mock_print_config(global_):
        '''
        Mocks the print_config method.
        '''

        nonlocal print_config_call_count
        nonlocal ctx

        print_config_call_count += 1

        if global_:
            ctx = 'Global'
        else:
            ctx = 'Local'

    monkeypatch.setattr(
        'autostack.cli.config.print_config',
        mock_print_config
    )

    # 2. When.
    result = runner.invoke(config_command, ['list'])

    # 3. Then.
    assert result.exit_code == 0
    assert print_config_call_count == 1
    assert ctx == 'Local'


def test_autostack_config_list_global(monkeypatch):
    '''
    Ensure that the print_config method is called with
    a global context.
    '''

    # 1. Given.
    runner = CliRunner()
    print_config_call_count = 0
    ctx = None

    def mock_print_config(global_):
        '''
        Mocks the print_config method.
        '''

        nonlocal print_config_call_count
        nonlocal ctx

        print_config_call_count += 1

        if global_:
            ctx = 'Global'
        else:
            ctx = 'Local'

    monkeypatch.setattr(
        'autostack.cli.config.print_config',
        mock_print_config
    )

    # 2. When.
    result = runner.invoke(config_command, ['-g', 'list'])

    # 3. Then.
    assert result.exit_code == 0
    assert print_config_call_count == 1
    assert ctx == 'Global'
