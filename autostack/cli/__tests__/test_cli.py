'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/12/2019
Overview: Tests for the cli package.
'''

from click.testing import CliRunner

from autostack.cli import autostack


def test_autostack_with_no_command():
    '''
    When the autostack command is executed with no command,
    ensure that the usage message is printed.
    '''

    # 1. Given.
    runner = CliRunner()

    # 2. When.
    result = runner.invoke(autostack)

    # 3. Then.
    assert result.exit_code == 0
    assert 'Usage:' in result.output
