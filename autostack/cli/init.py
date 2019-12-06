'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 12/05/2019
Overview: TODO: Write overview.
'''

import json

import click
import regex
from PyInquirer import (
    prompt,
    Validator,
    ValidationError
)

from autostack import (
    print_logo
)


@click.command()
def init():
    '''
    Initialize a project with a .autostack.json configuration file.
    '''

    class MaxCommentsValidator(Validator):
        # pylint: disable=too-few-public-methods
        '''
        Validator for the max_comments prompt.
        '''

        def validate(self, document):
            '''
            Ensures that the max_comments input contains a positive integer.
            '''

            valid = regex.match(r'^\d+$', document.text)
            if not valid:
                raise ValidationError(
                    message='Please enter a valid integer',
                    cursor_position=len(document.text))

    questions = [
        {
            'type': 'checkbox',
            'name': 'languages',
            'message':
                'What languages do you want autostack \
                to capture errors for?',
            'choices': [
                {
                    'name': 'Python',
                    'checked': True,
                },
            ]
        },
        {
            'type': 'checkbox',
            'name': 'communities',
            'message':
                'Which Stack Exchange communities do you want to \
                query?',
            'choices': [
                {
                    'name': 'Stack Overflow',
                    'checked': True,
                },
            ]
        },
        {
            'type': 'list',
            'name': 'order_by',
            'message': 'How do you want to order posts?',
            'choices': [
                'Relevance',
                'Newest',
                'Active',
                'Votes',
            ]
        },
        {
            'type': 'confirm',
            'name': 'verified_only',
            'message':
                'Do you want to only display posts with verified \
                answers?',
        },
        {
            'type': 'confirm',
            'name': 'display_comments',
            'message':
                'Do you want to display comments with questions and \
                answers?',
        },
    ]

    max_comments_questions = [
        {
            'type': 'input',
            'name': 'max_comments',
            'message':
                'What\'s the max number of comments to display per \
                question or answer?',
            'validate': MaxCommentsValidator,
        }
    ]

    print_logo()
    answers = prompt(questions)
    if answers['display_comments']:
        answers['max_comments'] = prompt(
            max_comments_questions
        )['max_comments']

    with open('./.autostack.json', 'w') as autostack_json:
        json.dump(answers, autostack_json, indent=4)
