'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/11/2019
Overview: Constants used by the config package.
'''

import os

CONFIG_DIR_NAME = '.autostack'

CONFIG_FILE_NAME = '.autostack.json'

DEFAULT_CONFIG = {
    'language': 'Python',
    'order_by': 'Relevance',
    'verified_only': True,
    'display_comments': False,
}

GLOBAL_CONFIG_PATH = os.path.join(
    os.getenv('HOME'),
    CONFIG_DIR_NAME,
    CONFIG_FILE_NAME
)

SUPPORTED_CONFIG_KEYS = ['language', 'order_by', 'verified_only', 'display_comments', 'max_comments']

SUPPORTED_LANGUAGES = ['Python']

SUPPORTED_ORDER_BY_FILTERS = ['Relevance', 'Newest', 'Active', 'Votes']
