'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/10/2019
Overview: TODO: Write overview.
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
GLOBAL_CONFIG_PATH = os.path.join(os.getenv('HOME'), CONFIG_DIR_NAME, CONFIG_FILE_NAME)


def create_global_config():
    '''
    TODO
    '''

    if not os.path.exists(os.path.join(os.getenv('HOME'), CONFIG_DIR_NAME)):
        os.makedirs(os.path.join(os.getenv('HOME'), CONFIG_DIR_NAME))

    with open(GLOBAL_CONFIG_PATH, 'w+') as global_config_file:
        json.dump(DEFAULT_CONFIG, global_config_file, indent=4)


def get_global_config(key):
    '''
    TODO
    '''

    config = None

    with open(GLOBAL_CONFIG_PATH, 'r') as global_config_file:
        config = json.loads(global_config_file.read())

    try:
        return config[key]
    except KeyError:
        print('The key {} doesn\'t exist in the global configuration file.'.format(key))


def get_all_global_configs():
    '''
    TODO
    '''

    with open(GLOBAL_CONFIG_PATH, 'r') as global_config_file:
        config = json.loads(global_config_file.read())

        print('GLOBAL CONFIGURATIONS:')
        for key, value in config:
            print('\t{}: {}'.format(key, value))


def set_global_config(key, value):
    '''
    TODO
    '''

    with open(GLOBAL_CONFIG_PATH, 'r+') as global_config_file:
        config = json.loads(global_config_file.read())

        try:
            config[key] = value
            json.dump(config, global_config_file, indent=4)
        except KeyError:
            print('The key {} doesn\'t exist in the global configuration file.'.format(key))
