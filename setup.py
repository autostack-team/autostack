import setuptools
from os import path

# Long Description.
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()
    
setuptools.setup(
    # General setup information.
    name='autostack',
    version='0.0.7',
    packages=setuptools.find_packages(exclude=['tests']),
    scripts=[
        'autostack/autostack-terminal'
    ],
    entry_points={
        'console_scripts': [
            'autostack=autostack.__main__:main'
        ]
    },
    install_requires=[
        'Pygments>=2.3.1',
        'requests>=2.21.0',
        'termcolor>=1.1.0',
        'lxml>=4.3.2',
        'beautifulsoup4>=4.7.1',
    ],

    # Meta data.
    author='Elijah Sawyers, Benjamin Sanders, Caleb Werth',
    author_email='elijahsawyers@gmail.com, ben.sanders97@gmail.com, cwerth@crimson.ua.edu',
    description='Automatically detect python errors and search Stack Overflow.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # TODO: URL.
    # TODO: Keywords.
    url='https://github.com/elijahsawyers/AutoStack',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Debuggers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
    ],
)