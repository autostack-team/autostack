'''
Authors: Elijah Sawyers
Emails: elijahsawyers@gmail.com
Date: 05/31/2020
Overview: Tests for the so_web_scraper print module.
'''

from termcolor import colored

from autostack.so_web_scraper.print import (
    print_post,
    print_post_text,
    print_post_comments,
    print_ul,
    print_code_block
)


def test_placeholder_print_post_no_question(monkeypatch):
    '''
    Ensures that nothing is printed if a question couldn't be found
    on the post.
    '''

    # 1. Given.
    print_post_text_call_count = 0

    def mock_get_post_text(post, class_):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_text method.
        '''

        if class_ == 'question':
            return None

        return 'Post text!'

    def mock_print_post_text(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the print_post_text method.
        '''

        nonlocal print_post_text_call_count
        print_post_text_call_count += 1

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.get_post_text',
        mock_get_post_text
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.print_post_text',
        mock_print_post_text
    )

    # 2. When.
    print_post(None, {'display_comments': False})

    # 3. Then.
    assert not print_post_text_call_count


def test_placeholder_print_post_no_answer(monkeypatch):
    '''
    Ensures that nothing is printed if an answer couldn't be found
    on the post.
    '''

    # 1. Given.
    print_post_text_call_count = 0

    def mock_get_post_text(post, class_):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_text method.
        '''

        if class_ == 'answer':
            return None

        return 'Post text!'

    def mock_print_post_text(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the print_post_text method.
        '''

        nonlocal print_post_text_call_count
        print_post_text_call_count += 1

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.get_post_text',
        mock_get_post_text
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.print_post_text',
        mock_print_post_text
    )

    # 2. When.
    print_post(None, {'display_comments': False})

    # 3. Then.
    assert not print_post_text_call_count


def test_placeholder_print_post_no_comments(capsys, monkeypatch):
    '''
    Ensures that nothing is printed for comments.
    '''

    # 1. Given.
    print_post_text_call_count = 0

    def mock_get_post_text(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_text method.
        '''

        return 'Post text!'

    def mock_print_post_text(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the print_post_text method.
        '''

        nonlocal print_post_text_call_count
        print_post_text_call_count += 1

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.get_post_text',
        mock_get_post_text
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.print_post_text',
        mock_print_post_text
    )

    # 2. When.
    print_post(None, {'display_comments': False})

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == (
        colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red') +
        '\n' +
        colored('Question:', 'red') + '\n' +
        colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red') +
        '\n' +
        colored('Answer:', 'red') + '\n' +
        colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red') +
        '\n'
    )
    assert print_post_text_call_count == 2


def test_placeholder_print_post_with_comments(capsys, monkeypatch):
    '''
    Ensures that comments are printed.
    '''

    # 1. Given.
    print_post_text_call_count = 0

    def mock_get_post_text(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_text method.
        '''

        return 'Post text!'

    def mock_print_post_text(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the print_post_text method.
        '''

        nonlocal print_post_text_call_count
        print_post_text_call_count += 1

    def mock_get_post_comments(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the get_post_comments method.
        '''

        return 'Comment!'

    def mock_print_post_comments(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the print_post_comments method.
        '''

        return

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.get_post_text',
        mock_get_post_text
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.print_post_text',
        mock_print_post_text
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.get_post_comments',
        mock_get_post_comments
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.print_post_comments',
        mock_print_post_comments
    )

    # 2. When.
    print_post(None, {'display_comments': True, 'max_comments': 3})

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == (
        colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red') +
        '\n' +
        colored('Question:', 'red') + '\n' +
        colored('\nComments:', 'red') + '\n' +
        colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red') +
        '\n' +
        colored('Answer:', 'red') + '\n' +
        colored('\nComments:', 'red') + '\n' +
        colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red') +
        '\n'
    )
    assert print_post_text_call_count == 2


def test_print_post_text(monkeypatch):
    '''
    Ensures that print_post_text properly prints each type of HTML element.
    '''

    # 1. Given.
    h1_count = 0
    h2_count = 0
    h3_count = 0
    p_count = 0
    blockquote_count = 0
    ul_count = 0
    pre_count = 0

    class MockPostElement():
        # pylint: disable=too-few-public-methods
        '''
        Mocks a post element.
        '''

        def __init__(self, name):
            '''
            Inits a mock post element object.
            '''

            self.name = name
            self.text = name

        def find(self, *args):
            # pylint: disable=unused-argument,no-self-use
            '''
            Mocks the find method.
            '''

            return

    def mock_print_ul(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the print_ul method.
        '''

        nonlocal ul_count
        ul_count += 1

    def mock_print_code_block(*args):
        # pylint: disable=unused-argument
        '''
        Mocks the print_code_block method.
        '''

        nonlocal pre_count
        pre_count += 1

    def mock_colored(*args):
        '''
        Mocks the colored method.
        '''

        nonlocal h1_count
        nonlocal h2_count
        nonlocal h3_count
        nonlocal p_count
        nonlocal blockquote_count

        if args[0] == 'h1':
            h1_count += 1
        if args[0] == 'h2':
            h2_count += 1
        if args[0] == 'h3':
            h3_count += 1
        if args[0] == 'p':
            p_count += 1
        if args[0] == 'blockquote':
            blockquote_count += 1

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.print_ul',
        mock_print_ul
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.print_code_block',
        mock_print_code_block
    )

    monkeypatch.setattr(
        'autostack.so_web_scraper.print.colored',
        mock_colored
    )

    post_elements = [
        MockPostElement('h1'),
        MockPostElement('h2'),
        MockPostElement('h2'),
        MockPostElement('h3'),
        MockPostElement('h3'),
        MockPostElement('h3'),
        MockPostElement('p'),
        MockPostElement('p'),
        MockPostElement('blockquote'),
        MockPostElement('ul'),
        MockPostElement('ul'),
        MockPostElement('pre'),
        MockPostElement('pre'),
        MockPostElement('pre'),
    ]

    # 2. When.
    print_post_text(post_elements)

    # 3. Then.
    assert h1_count == 1
    assert h2_count == 2
    assert h3_count == 3
    assert p_count == 2
    assert blockquote_count == 1
    assert ul_count == 2
    assert pre_count == 3


def test_print_post_comments_attribute_error(capsys):
    '''
    Ensures that attribute errors are handled in the
    print_post_text method.
    '''

    # 1. Given.
    class MockComment():
        # pylint: disable=too-few-public-methods
        '''
        Mocks a comment object.
        '''

        def find(self, *args, **kwargs):
            # pylint: disable=unused-argument,no-self-use
            '''
            Mocks the find method.
            '''

            return None

    comments = [MockComment()]

    # 2. When.
    print_post_comments(comments)

    # 3. Then.
    captured = capsys.readouterr()
    assert not captured.out


def test_print_post_comments(capsys):
    '''
    Ensures that print_post_comments prints correctly.
    '''

    # 1. Given.
    class MockComment():
        # pylint: disable=too-few-public-methods
        '''
        Mocks a comment object.
        '''

        def find(self, *args, **kwargs):
            # pylint: disable=unused-argument,no-self-use
            '''
            Mocks the find method.
            '''

            class MockCommentText():
                # pylint: disable=too-few-public-methods
                '''
                Mocks a comment text object.
                '''

                def get_text(self):
                    # pylint: disable=no-self-use
                    '''
                    Mocks the get_text method.
                    '''

                    return 'Comment!'

            return MockCommentText()

    comments = [MockComment(), MockComment(), MockComment()]

    # 2. When.
    print_post_comments(comments)

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == (
        colored('Comment!', 'white') + '\n' +
        colored('Comment!', 'white') + '\n' +
        colored('Comment!', 'white') + '\n'
    )


def test_print_ul(capsys):
    '''
    Ensures the print_ul properly prints all li in the ul.
    '''

    # 1. Given.
    class MockUl():
        # pylint: disable=too-few-public-methods
        '''
        Mocks a ul object.
        '''

        def find_all(self, *args, **kwargs):
            # pylint: disable=unused-argument,no-self-use
            '''
            Mocks the find method.
            '''

            class MockLi():
                # pylint: disable=too-few-public-methods
                '''
                Mocks a comment text object.
                '''

                def __init__(self):
                    '''
                    Init a mock li object.
                    '''

                    self.text = 'li'

            return [MockLi(), MockLi(), MockLi()]

    # 2. When.
    print_ul(MockUl())

    # 3. Then.
    captured = capsys.readouterr()
    assert captured.out == (
        colored('    - li', 'green', attrs=['bold']) +
        '\n' +
        colored('    - li', 'green', attrs=['bold']) +
        '\n' +
        colored('    - li', 'green', attrs=['bold']) +
        '\n'
    )


def test_print_code_block():
    '''
    Ensures that print_code_block properly highlights syntax.
    '''