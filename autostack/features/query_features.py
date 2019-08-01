'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 07/29/2019
Overview: Contains extra features for autostack.
'''

from __future__ import print_function
from builtins import input
from autostack.web_scraper.stack_overflow_scraper import (
    accepted_posts,
    print_accepted_post
)


def custom_query():
    '''
    Searches Stack Overflow using a custom search query from the user.

    Called after three "no"s from the user. This function prompts the user
    for a string to serach on Stack Overflow. Using the same for loop as
    main, questions and accepted answers are printed to the terminal for the
    user to view.
    '''

    print('Enter a custom query (\'e\' to exit): ', end='')
    new_query = input()

    # If the user enters e, exit custom_query.
    if new_query == 'e':
        print(u'\U0001F95E Listening for Python errors...')
        return

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
