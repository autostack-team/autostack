# pylint: disable=line-too-long, anomalous-backslash-in-string
'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/13/2020
Overview: Tests for the autostack package.
'''

import re

from autostack import (
    clear_terminal,
    print_logo,
    print_welcome_message
)
from autostack.main import main

ANSI_ESCAPE = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')


def test_clear_terminal(capsys):
    '''
    Ensures that clear_terminal clears the terminal.
    '''

    # 1. Given.

    # 2. When.
    clear_terminal()

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == '\x1bc\n'  # Same as u'\033c'


def test_print_logo(capsys):
    '''
    Ensures the the logo prints properly.
    '''

    # 1. Given.

    # 2. When.
    print_logo()

    # 3. Then.
    captured = capsys.readouterr()
    assert ANSI_ESCAPE.sub('', captured.out) == (
        '        _____________        \n'  # nopep8
        '       /    ___      \       \n'  # nopep8
        '      ||    \__\     ||                   _            _             _    \n'  # nopep8
        '      ||      _      ||                  | |          | |           | |   \n'  # nopep8
        '      |\     / \     /|        __ _ _   _| |_ ___  ___| |_ __ _  ___| | __\n'  # nopep8
        '      \ \___/ ^ \___/ /       / _` | | | | __/ _ \/ __| __/ _` |/ __| |/ /\n'  # nopep8
        '      \\\\____/_^_\____//_     | (_| | |_| | || (_) \__ \ || (_| | (__|   < \n'  # nopep8
        '    __\\\\____/_^_\____// \     \__,_|\__,_|\__\___/|___/\__\__,_|\___|_|\_\\\n'  # nopep8
        '   /   \____/_^_\____/ \ \     AUTOMATING THE INEVITABLE...\n'  # nopep8
        '  //                   , /   \n'  # nopep8
        '  \\\\___________   ____  /  \n'  # nopep8
        '               \_______/     \n\n'  # nopep8
    )


def test_print_welcome_message(capsys, monkeypatch):
    '''
    Ensures that the welcome message prints properly.
    '''

    # 1. Given.
    call_count = 0

    def mock():
        '''
        Used to mock the clear_terminal and print_logo functions.
        '''

        nonlocal call_count
        call_count += 1

    monkeypatch.setattr(
        'autostack.clear_terminal',
        mock
    )
    monkeypatch.setattr(
        'autostack.print_logo',
        mock
    )

    # 2. When.
    print_welcome_message()

    # 3. Then.
    captured = capsys.readouterr()
    assert call_count == 2
    assert captured.out == (
        'Welcome to autostack! The command-line debugging tool that '
        'automatically displays Stack Overflow answers for thrown errors.'
        '\nSetup your global configuration file below...\n'
    )


def test_main(monkeypatch):
    '''
    Ensures that main calls the cli() method.
    '''

    # 1. Given.
    call_count = 0

    def mock():
        '''
        Used to mock the cli function.
        '''

        nonlocal call_count
        call_count += 1

    monkeypatch.setattr(
        'autostack.main.autostack',
        mock
    )

    # 2. When.
    main()

    # 3. Then.
    assert call_count == 1
