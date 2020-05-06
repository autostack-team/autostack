# pylint: disable=invalid-name, line-too-long, anomalous-backslash-in-string
'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 03/17/2019
Overview: The autostack package includes packages for a cli, error
parsing, querying Stack Overflow, and more!
'''

from __future__ import (
    absolute_import,
    division,
    print_function
)

name = 'autostack'


def clear_terminal():
    '''
    Clears the terminal window.
    '''

    print(u'\033c')


def print_logo():
    '''
    Prints the autostack logo, in color.
    '''

    print(u'        \u001b[38;5;179m_____________        ')  # nopep8
    print(u'       \u001b[38;5;179m/    \u001b[38;5;226m___      \u001b[38;5;179m\       \u001b[0m')  # nopep8
    print(u'      \u001b[38;5;179m||    \u001b[38;5;226m\__\\\u001b[0m     \u001b[38;5;179m||\u001b[38;5;208m                   _            _             _    ')  # nopep8
    print(u'      \u001b[38;5;179m||      \u001b[38;5;94m_\u001b[38;5;179m      ||\u001b[38;5;208m                  | |          | |           | |   ')  # nopep8
    print(u'      \u001b[38;5;179m|\     \u001b[38;5;94m/ \\\u001b[38;5;179m     /|\u001b[38;5;208m        __ _ _   _| |_ ___  ___| |_ __ _  ___| | __')  # nopep8
    print(u'      \u001b[38;5;179m\ \___\u001b[38;5;94m/ ^ \\\u001b[38;5;179m___/ /\u001b[38;5;208m       / _` | | | | __/ _ \/ __| __/ _` |/ __| |/ /')  # nopep8
    print(u'      \u001b[38;5;179m\\\\____\u001b[38;5;94m/_^_\\\u001b[38;5;179m____//\u001b[38;5;94m_\u001b[38;5;208m     | (_| | |_| | || (_) \__ \ || (_| | (__|   < ')  # nopep8
    print(u'    \u001b[38;5;94m__\u001b[38;5;179m\\\\____\u001b[38;5;94m/_^_\\\u001b[38;5;179m____// \u001b[38;5;94m\\\u001b[38;5;208m     \__,_|\__,_|\__\___/|___/\__\__,_|\___|_|\_\\')  # nopep8
    print(u'   \u001b[38;5;94m/   \u001b[38;5;179m\____\u001b[38;5;94m/_^_\\\u001b[38;5;179m____/ \u001b[38;5;224m\ \u001b[38;5;94m\\\u001b[0m     \033[1mAUTOMATING THE INEVITABLE...')  # nopep8
    print(u'  \u001b[38;5;94m/\u001b[38;5;224m/\u001b[38;5;94m                   \u001b[38;5;224m, \u001b[38;5;94m/   ')  # nopep8
    print(u'  \u001b[38;5;94m\\\u001b[38;5;224m\\\u001b[38;5;94m___________   \u001b[38;5;224m____  \u001b[38;5;94m/  ')  # nopep8
    print(u'               \u001b[38;5;94m\_______/\u001b[0m     \n')  # nopep8


def print_welcome_message():
    '''
    Prints a welcome message after setup.
    '''

    clear_terminal()
    print_logo()
    print(
        'Welcome to autostack! The command-line debugging tool that automatically displays Stack Overflow answers for thrown errors.'
    )
    print('Setup your global configuration file below...')
