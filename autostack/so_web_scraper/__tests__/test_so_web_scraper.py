'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 10/25/2019
Overview: Tests for the so_web_scraper package.
'''

import re
from bs4 import BeautifulSoup

from autostack.so_web_scraper import (
    accepted_posts,
    get_post_summaries,
    build_query_url,
    query_stack_overflow,
    post_soup,
    has_accepted_answer,
    get_post_url,
    print_accepted_post,
    get_post_text,
    print_post_text,
    print_ul,
    print_code_block,
    get_src_code,
)
from autostack.so_web_scraper.__tests__.mock_response import (
    MockResponse,
    build_mock_get
)

ANSI_ESCAPE = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')


def test_accepted_posts(monkeypatch):
    '''
    Ensures that accepted_posts loops over each post summary.
    '''

    # 1. Given.
    post_soup_call_count = 0

    def mock_get_post_summaries(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_summaries function
        '''

        html = open(
            'autostack/so_web_scraper/__tests__/data/query_post_summaries.html'
        ).read()

        post_summaries = BeautifulSoup(html, 'lxml').find_all(
            attrs={
                'class': 'question-summary'
            }
        )

        return [post_summaries]

    def mock_post_soup(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the post_soup function
        '''
        nonlocal post_soup_call_count
        post_soup_call_count += 1
        return 'SOUP'

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
    for post in accepted_posts(None):
        pass

    # 3. Then.
    assert post_soup_call_count == 15


def test_get_post_summaries(monkeypatch):
    '''
    Ensures that the generator yields post summaries until
    there aren't anymore post summaries.
    '''

    # 1. Given.
    query_stack_overflow_call_count = 0

    def mock_build_query_url(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the build_query_url function.
        '''

        return

    def mock_query_stack_overflow(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the query_stack_overflow function.
        '''

        nonlocal query_stack_overflow_call_count
        query_stack_overflow_call_count += 1

        base = 'autostack/so_web_scraper/__tests__/data/'

        if query_stack_overflow_call_count == 3:
            return BeautifulSoup(open(
                base + 'query_no_post_summaries.html'
            ).read(), 'lxml')

        return BeautifulSoup(open(
            base + 'query_post_summaries.html'
        ).read(), 'lxml')

    monkeypatch.setattr(
        'autostack.so_web_scraper.build_query_url',
        mock_build_query_url
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.query_stack_overflow',
        mock_query_stack_overflow
    )

    # 2. When.
    # pylint: disable=unused-variable
    for post_summaries in get_post_summaries(None):
        pass

    # 3. Then.
    assert query_stack_overflow_call_count == 3


def test_get_post_summaries_no_query_soup(monkeypatch):
    '''
    Ensures that the generator yields nothing when there's
    no BeautifulSoup returned from querying Stack Overflow.
    '''

    # 1. Given.
    def mock_build_query_url(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the build_query_url function.
        '''

        return

    def mock_query_stack_overflow(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the query_stack_overflow function.
        '''

        return None

    monkeypatch.setattr(
        'autostack.so_web_scraper.build_query_url',
        mock_build_query_url
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.query_stack_overflow',
        mock_query_stack_overflow
    )

    # 2. When.
    post_count = 0

    # pylint: disable=unused-variable
    for post_summaries in get_post_summaries(None):
        post_count += 1

    # 3. Then.
    assert post_count == 0


def test_build_query_url():
    '''
    Ensures that the proper URL is built with build_query_url.
    '''

    # 1. Given.
    base_url = 'https://stackoverflow.com'
    page = 1
    query = 'Test Query'

    # 2. When.
    url = build_query_url(query, page)

    # 3. Then.
    assert '{}/search?page={}&tab=Relevance&q=%5Bpython%5D+Test+Query'.format(
        base_url,
        page
    ) == url


def test_query_stack_overflow_good_response_status(monkeypatch):
    '''
    Ensures that BeautifulSoup is returned from query_stack_overflow.
    '''

    # 1. Given.
    path = 'autostack/so_web_scraper/__tests__/data/query_post_summaries.html'
    html = open(path).read()
    soup = BeautifulSoup(html, 'lxml')
    mock_response = MockResponse(
        path,
        200
    )
    mock_get = build_mock_get(mock_response)

    monkeypatch.setattr('requests.get', mock_get)

    # 2. When.
    response = query_stack_overflow(None)

    # 3. Then.
    assert response == soup


def test_query_stack_overflow_bad_response_status(monkeypatch):
    '''
    Ensures that BeautifulSoup is returned from query_stack_overflow.
    '''

    # 1. Given.
    mock_response = MockResponse(
        'autostack/so_web_scraper/__tests__/data/query_post_summaries.html',
        400
    )
    mock_get = build_mock_get(mock_response)

    monkeypatch.setattr('requests.get', mock_get)

    # 2. When.
    response = query_stack_overflow(None)

    # 3. Then.
    assert not response


def test_post_soup_no_accepted_answer(monkeypatch):
    '''
    Ensures that None is returned when there's no accepted answer.
    '''

    # 1. Given.
    def mock_has_accepted_answer(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the has_accepted_answer function.
        '''

        return False

    monkeypatch.setattr(
        'autostack.so_web_scraper.has_accepted_answer',
        mock_has_accepted_answer
    )

    # 2. When.
    response_soup = post_soup(None)

    # 3. Then.
    assert not response_soup


def test_post_soup_accepted_answer(monkeypatch):
    '''
    Ensures that BeautifulSoup is returned when there's an accepted answer.
    '''

    # 1. Given.
    path = 'autostack/so_web_scraper/__tests__/data/post_accepted_answer.html'
    html = open(path).read()
    soup = BeautifulSoup(html, 'lxml')

    def mock_has_accepted_answer(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the has_accepted_answer function.
        '''

        return True

    def mock_get_post_url(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_url function.
        '''

        return ''

    mock_response = MockResponse(
        path,
        200
    )
    mock_get = build_mock_get(mock_response)

    monkeypatch.setattr(
        'autostack.so_web_scraper.has_accepted_answer',
        mock_has_accepted_answer
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.get_post_url',
        mock_get_post_url
    )

    monkeypatch.setattr('requests.get', mock_get)

    # 2. When.
    response_soup = post_soup(None)

    # 3. Then.
    assert response_soup == soup


def test_post_soup_bad_status(monkeypatch):
    '''
    Ensures that None is returned when the request status is bad.
    '''

    # 1. Given.
    mock_response = MockResponse(
        'autostack/so_web_scraper/__tests__/data/post_accepted_answer.html',
        400
    )
    mock_get = build_mock_get(mock_response)

    def mock_has_accepted_answer(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the has_accepted_answer function.
        '''

        return True

    def mock_get_post_url(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_url function.
        '''

        return ''

    monkeypatch.setattr(
        'autostack.so_web_scraper.has_accepted_answer',
        mock_has_accepted_answer
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.get_post_url',
        mock_get_post_url
    )

    monkeypatch.setattr('requests.get', mock_get)

    # 2. When.
    response = post_soup(None)

    # 3. Then.
    assert not response


def test_has_accepted_answer_false():
    '''
    Ensures that has_accepted_answer returns False when the post
    does not have an accepted answer.
    '''

    # 1. Given.
    html = open(
        'autostack/so_web_scraper/__tests__/data/query_post_summaries.html'
    ).read()

    post_summary = BeautifulSoup(html, 'lxml').find_all(
        attrs={
            'class': 'question-summary'
        }
    )[0]

    # 2. When.
    accepted_answer = has_accepted_answer(post_summary)

    # 3. Then.
    assert not accepted_answer


def test_has_accepted_answer_true():
    '''
    Ensures that has_accepted_answer returns True when the post
    does in fact have an accepted answer.
    '''

    # 1. Given.
    html = open(
        'autostack/so_web_scraper/__tests__/data/query_post_summaries.html'
    ).read()

    post_summary = BeautifulSoup(html, 'lxml').find_all(
        attrs={
            'class': 'question-summary'
        }
    )[4]

    # 2. When.
    accepted_answer = has_accepted_answer(post_summary)

    # 3. Then.
    assert accepted_answer


def test_get_post_url_where_url_exists():
    '''
    Ensures that a url is returned from get_post_url
    when a url exists.
    '''

    # 1. Given.
    html = open(
        'autostack/so_web_scraper/__tests__/data/query_post_summaries.html'
    ).read()

    post_summary = BeautifulSoup(html, 'lxml').find(
        attrs={
            'class': 'question-summary'
        }
    )

    # 2. When.
    url = get_post_url(post_summary)

    # 3. Then.
    # pylint: disable=line-too-long
    assert url == '/questions/930397/getting-the-last-element-of-a-list/930398?r=SearchResults#930398'  # nopep8


def test_get_post_url_where_url_doesnt_exist():
    '''
    Ensures that None is returned from get_post_url
    when a url doesn't exist.
    '''

    # 1. Given.
    # pylint: disable=too-few-public-methods
    class MockPostSummary:
        '''
        Mocks a post summary.
        '''

        def find(self, *args, **kwargs):
            # pylint: disable=unused-argument,no-self-use
            '''
            Returns an empty dictionary, mocking a find call on a
            bs4.Tag.
            '''

            return dict()

    mock_post_summary = MockPostSummary()

    # 2. When.
    url = get_post_url(mock_post_summary)

    # 3. Then.
    assert not url


def test_print_accepted_post_no_question(capsys, monkeypatch):
    '''
    Ensures that nothing is printed when no question is found on a post.
    '''

    # 1. Given.
    def mock_get_post_text(*args):
        '''
        Mocks the get_post_text function.
        '''

        if args[1] == 'question':
            return None
        return True

    monkeypatch.setattr(
        'autostack.so_web_scraper.get_post_text',
        mock_get_post_text
    )

    # 2. When.
    print_accepted_post(None)

    # 3. Then.
    captured = capsys.readouterr()
    assert not captured.out


def test_print_accepted_post_no_answer(capsys, monkeypatch):
    '''
    Ensures that nothing is printed when no answer is found on a post.
    '''

    # 1. Given.
    def mock_get_post_text(*args):
        '''
        Mocks the get_post_text function.
        '''

        if args[1] == 'accepted-answer':
            return None
        return True

    monkeypatch.setattr(
        'autostack.so_web_scraper.get_post_text',
        mock_get_post_text
    )

    # 2. When.
    print_accepted_post(None)

    # 3. Then.
    captured = capsys.readouterr()
    assert not captured.out


def test_print_accepted_post_found_question_and_answer(capsys, monkeypatch):
    '''
    Ensures that proper output when both a question and answer are found.
    '''

    # 1. Given.
    def mock_get_post_text(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_text function.
        '''

        return True

    def mock_print_post_text(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the print_post_text function.
        '''

        return

    monkeypatch.setattr(
        'autostack.so_web_scraper.get_post_text',
        mock_get_post_text
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.print_post_text',
        mock_print_post_text
    )

    # 2. When.
    print_accepted_post(None)

    # 3. Then.
    captured = capsys.readouterr()
    assert ANSI_ESCAPE.sub('', captured.out) == (
        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        'Question:\n' +
        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        'Answer:\n' +
        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
    )


def test_get_post_text_question():
    '''
    Ensures that the question post-text is returned for a post.
    '''

    # 1. Given.
    path = 'autostack/so_web_scraper/__tests__/data/post_accepted_answer.html'
    html = open(path).read()
    post = BeautifulSoup(html, 'lxml')

    # 2. When.
    post_text = get_post_text(post, 'question')

    # 3. Then.
    assert post_text


def test_get_post_text_answer():
    '''
    Ensures the accepted answer post-text is returned for a post.
    '''

    # 1. Given.
    path = 'autostack/so_web_scraper/__tests__/data/post_accepted_answer.html'
    html = open(path).read()
    post = BeautifulSoup(html, 'lxml')

    # 2. When.
    post_text = get_post_text(post, 'accepted-answer')

    # 3. Then.
    assert post_text


def test_get_post_text_invalid_html_class():
    '''
    Ensures that None when an Attribute error occures.
    '''

    # 1. Given.
    # pylint: disable=too-few-public-methods
    class MockPost:
        '''
        Mocks a post.
        '''

        def find(self, *args, **kwargs):
            # pylint: disable=unused-argument,no-self-use
            '''
            Returns None, mocking a find call on a bs4.Tag.
            '''

            return None

    mock_post = MockPost()

    # 2. When.
    post_text = get_post_text(mock_post, 'invalid-class')

    # 3. Then.
    assert not post_text


def test_print_post_text(capsys, monkeypatch):
    '''
    Ensures that proper output when print_post_text is called.
    '''

    # 1. Given.
    path = 'autostack/so_web_scraper/__tests__/data/post_text.html'
    html = open(path).read()
    post_text = BeautifulSoup(html, 'lxml').find(
        attrs={'class', 'post-text'}
    )

    def mock_other_print_functions(*args):
        # pylint: disable=unused-argument
        '''
        Mocks print_ul and print_code_block functions.
        '''

        return

    monkeypatch.setattr(
        'autostack.so_web_scraper.print_ul',
        mock_other_print_functions
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.print_code_block',
        mock_other_print_functions
    )

    # 2. When.
    print_post_text(post_text)

    # 3. Then.
    captured = capsys.readouterr()
    assert ANSI_ESCAPE.sub('', captured.out) == (
        'Test 1\n' +
        'Test 2\n' +
        'Test 3\n' +
        'Test 4\n' +
        'Test 5\n'
    )


def test_print_ul_populated(capsys):
    '''
    Ensures that all list elements are printed.
    '''

    # 1. Given.
    path = (
        'autostack/so_web_scraper/__tests__/data/post_text_ul_populated.html'
    )
    html = open(path).read()
    unordered_list = BeautifulSoup(html, 'lxml').find('ul')

    # 2. When.
    print_ul(unordered_list)

    # 3. Then.
    captured = capsys.readouterr()
    assert ANSI_ESCAPE.sub('', captured.out) == (
        '    - Test 1\n' +
        '    - Test 2\n' +
        '    - Test 3\n'
    )


def test_print_ul_empty(capsys):
    '''
    Ensures that nothing is printed when the unordered list is empty.
    '''

    # 1. Given.
    path = 'autostack/so_web_scraper/__tests__/data/post_text_ul_empty.html'
    html = open(path).read()
    unordered_list = BeautifulSoup(html, 'lxml').find('ul')

    # 2. When.
    print_ul(unordered_list)

    # 3. Then.
    captured = capsys.readouterr()
    assert not captured.out


def test_print_code_block(capsys, monkeypatch):
    '''
    Ensures that all of the source code is printed.
    '''

    # 1. Given.
    line_1 = 'l = [[1, 2, 3], [4, 5, 6], [7], [8, 9]]\n'
    line_2 = 'reduce(lambda x, y: x.extend(y), l)'

    def mock_get_src_code(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_src_code function.
        '''

        return

    def mock_lex(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the pygments.lex function.
        '''

        nonlocal line_1
        nonlocal line_2

        responses = [
            ('Token.Keyword', line_1),
            ('Other', line_2)
        ]

        for i in range(2):
            yield responses[i]

    monkeypatch.setattr(
        'autostack.so_web_scraper.get_src_code',
        mock_get_src_code
    )

    monkeypatch.setattr('pygments.lex', mock_lex)

    # 2. When.
    print_code_block(None)

    # 3. Then.
    captured = capsys.readouterr()
    assert ANSI_ESCAPE.sub('', captured.out) == (
        '\n{}'.format(line_1) +
        '{}\n'.format(line_2)
    )


def test_get_src_code():
    '''
    Ensures that all source code is returned.
    '''

    # 1. Given.
    line_1 = 'l = [[1, 2, 3], [4, 5, 6], [7], [8, 9]]\n'
    line_2 = 'reduce(lambda x, y: x.extend(y), l)'
    path = 'autostack/so_web_scraper/__tests__/data/post_text_code.html'
    html = open(path).read()
    code_block = BeautifulSoup(html, 'lxml').find('div').find('code')

    # 2. When.
    src_code = get_src_code(code_block)

    # 3. Then.
    assert src_code == line_1 + line_2
