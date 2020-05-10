'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 03/17/2019
Overview: Contains methods to scrape Stack Overflow and display posts
in a neat fashion.
'''

from autostack.so_web_scraper.scrape import (
    get_post_summaries,
    post_soup
)


def posts(query, config):
    '''
    A generator that queries Stack Overflow and yields posts for the query,
    with consideration to the configuration.

    Parameter {string} query: the string to query Stack Overflow with.
    Parameter {dictionary} config: configuration object.
    Yields {bs4.BeautifulSoup} a post's html document (i.e. bs4 soup).
    '''

    for post_summaries in get_post_summaries(query, config):
        for post_summary in post_summaries:
            post = post_soup(post_summary, config)

            if post:
                yield post
