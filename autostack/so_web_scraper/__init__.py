'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 03/17/2019
Overview: Used to scrape Stack Overflow for posts with a given query.
'''

from autostack.so_web_scraper.scrape import (
    get_post_summaries,
    post_soup
)


def posts(query, config):
    '''
    A generator that queries Stack Overflow and yields posts, with consideration
    to the configuration object.

    Parameter {string} query: the string to query Stack Overflow with.
    Parameter {dictionary} config: configuration object.
    Yields {bs4.BeautifulSoup}: a post html document (i.e. soup).
    '''

    for result_set in get_post_summaries(query, config):
        for post_summary in result_set:
            post = post_soup(post_summary, config)

            if post:
                yield post
