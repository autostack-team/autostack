import setuptools
from os import path

from autostack import print_welcome_message
from autostack.cli.init import undecorated_init

# Setup autostack.
try:
    setuptools.setup(
        # General setup information.
        name='autostack',
        version='1.2.0',
        packages=setuptools.find_packages(exclude=['tests']),
        entry_points={
            'console_scripts': [
                'autostack=autostack.main:main'
            ]
        },
        install_requires=[
            'Pygments',
            'requests',
            'termcolor',
            'lxml',
            'beautifulsoup4',
            'future',
            'pytest',
            'pytest-cov',
            'click',
            'PyInquirer',
        ],
        extras_require={ 
            'development': [
                'pytest',
                'pytest-pep8',
                'pytest-cov',
                'pytest-pylint',
            ]
        },

        # Meta data.
        url='https://github.com/elijahsawyers/autostack',
        author='Elijah Sawyers, Benjamin Sanders, Caleb Werth',
        author_email='elijahsawyers@gmail.com, ben.sanders97@gmail.com, cwerth@crimson.ua.edu',
        description='Automatically detect python errors and search Stack Overflow.',
        long_description=open('./README.md').read(),
        long_description_content_type='text/markdown',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Debuggers',
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Unix',
        ],
        keywords='command-line debug development tool'
    )

# After setup, initialize the global configuration file.
finally:
    print_welcome_message()
    undecorated_init(False, True)
