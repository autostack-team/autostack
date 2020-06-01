'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/25/2019
Overview: Tests for the so_web_scraper package.
'''

from autostack.so_web_scraper import (
    posts,
)


def test_posts(monkeypatch):
    '''
    Ensures that posts loops over each post summary.
    '''

    # 1. Given.
    get_post_summaries_call_count = 0
    post_soup_post_call_count = 0
    post_soup_no_post_call_count = 0

    def mock_get_post_summaries(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_summaries method.
        '''

        nonlocal get_post_summaries_call_count
        get_post_summaries_call_count += 1

        return [
            [True, False, True, False, True],
            [True, False, True, False, True],
            [True, False, True, False, True],
            [True, False, True, False, True],
            [True, False, True, False, True],
        ]

    def mock_post_soup(post_summary, config):
        # pylint: disable=unused-argument
        '''
        Mocks the post_soup method.
        '''

        nonlocal post_soup_post_call_count
        nonlocal post_soup_no_post_call_count

        if post_summary:
            post_soup_post_call_count += 1
            return True

        post_soup_no_post_call_count += 1
        return False

    monkeypatch.setattr(
        'autostack.so_web_scraper.get_post_summaries',
        mock_get_post_summaries
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.post_soup',
        mock_post_soup
    )

    # 2. When.
    # pylint: disable=unused-variable
    for post in posts(None, {}):
        pass

    # 3. Then.
    assert get_post_summaries_call_count == 1
    assert post_soup_post_call_count == 15
    assert post_soup_no_post_call_count == 10
