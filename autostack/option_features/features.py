'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 07/29/2019
Overview: Contains extra features for autostack.
'''

from __future__ import print_function
from autostack.web_scraper.stack_overflow_scraper import (
    accepted_posts,
    print_accepted_post
)

def custom_query():
    '''
    Allows the user to submit a custom query to search on Stack Overflow.
    '''

    print('Enter a custom query: ', end='')
    new_query = input()

    for post in accepted_posts(new_query):
        # Display Stack Overflow posts for the error.
        print_accepted_post(post)

        # If the user's question has been answered,
        # don't keep looping over posts.
        while True:
            print('Did this answer your question? (Y/n): ', end='')
            question_answered = input()
            if question_answered == 'Y' or question_answered == 'n':
                break
        if question_answered == 'Y':
            print(u'\U0001F95E Listening for Python errors...')
            break
        elif question_answered == 'n':
            continue