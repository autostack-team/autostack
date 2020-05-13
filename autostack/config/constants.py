'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/11/2019
Overview: Constants used by the config package.
'''

import os

# The global configuration directory.
CONFIG_DIR_NAME = '.autostack'

# The configuration file name.
CONFIG_FILE_NAME = '.autostack.json'

# Default configuration key-value pairs.
DEFAULT_CONFIG = {
    'language': 'Python',
    'order_by': 'Relevance',
    'verified_only': True,
    'display_comments': False,
    'max_comments': 0
}

# The default global configuration file path.
GLOBAL_CONFIG_PATH = os.path.join(
    os.getenv('HOME'),
    CONFIG_DIR_NAME,
    CONFIG_FILE_NAME
)

# The supported configuration file keys.
SUPPORTED_CONFIG_KEYS = [
    'language',
    'order_by',
    'verified_only',
    'display_comments',
    'max_comments'
]

# The supported languages for detecting errors.
SUPPORTED_LANGUAGES = ['Python']

# The supported values for the order_by configuration file key.
SUPPORTED_ORDER_BY_FILTERS = [
    'Relevance',
    'Newest',
    'Active',
    'Votes'
]
