'''
Authors: Elijah Sawyers, Benjamin Sanders
Emails: elijahsawyers@gmail.com, ben.sanders97@gmail.com
Date: 03/17/2019
Overview: Contains the StackOverflowScraper class which is used to
scrape Stack Overflow for posts with accepted answers for a given query.
'''

from __future__ import print_function
from bs4 import BeautifulSoup
import pygments
from pygments.lexers import PythonLexer
import requests
from termcolor import colored

URL = 'https://stackoverflow.com'

class StackOverflowScraper(object):
    '''
    The StackOverflowScraper class is used to scrape Stack Overflow
    for posts with accepted answers for a given query.
    '''

    def accepted_posts(self, query):
        '''
        Iterates over Stack Overflow posts for a given query.

        The posts that are iterated are sorted by relevancy, and
        the iterable only returns posts that have an accepted
        answer.

        Parameter {String} query: The Stack Overflow query.
        Returns {BeautifulSoup}: An iterable that iterates
        over Stack Overflow posts for the query.
        '''

        page = 1

        while True:
            query_url = '{}/search?page={}&tab=Relevance&q='.format(URL, page)

            # Build the query.
            for query_string in query.split(' '):
                query_url = query_url + '+' + query_string

            # The 'soup' of the query page.
            request = requests.get(query_url)
            query_html = request.text
            query_soup = BeautifulSoup(query_html, 'lxml')

            # Grab all post summaries from the current page.
            post_summaries = query_soup.find_all(
                attrs={
                    "class": "question-summary"
                }
            )

            # No more posts for the given query.
            if not post_summaries:
                page = 1
                break

            for post_summary in post_summaries:
                accepted_answer = post_summary.find(
                    attrs={
                        'class': 'answered-accepted'
                    }
                )

                # Only view posts with accepted answers.
                if not accepted_answer:
                    continue

                post_href = post_summary.find(
                    attrs={
                        'class': 'question-hyperlink'
                    },
                    href=True
                )['href']

                # The 'soup' of the post.
                request = requests.get(URL + post_href)
                post_html = request.text
                post_soup = BeautifulSoup(post_html, 'lxml')

                yield post_soup

            # Go to the next page
            page += 1

    def print_accepted_post(self, post):
        '''
        Prints a Stack Overflow post with an accepted answer.

        Parameter {BeautifulSoup} post: The 'soup' of the post
        to print.
        '''
        print(colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red'))
        print(colored('Question:', 'red'))

        # Print the question.
        question = post.find(
            attrs={
                'class',
                'question'
            }
        ).find(
            attrs={
                'class',
                'post-text'
            }
        )

        if not question:
            return

        self.print_post_text(question)

        print(colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red'))
        print(colored('Answer:', 'red'))

        # Print the answer.
        accepted_answer = post.find(
            attrs={
                'class',
                'accepted-answer'
            }
        ).find(
            attrs={
                'class',
                'post-text'
            }
        )

        if not accepted_answer:
            return

        self.print_post_text(accepted_answer)

        print(colored('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 'red'))
        return

    def print_post_text(self, post_text):
        '''
        Prints post-text from Stack Overflow.

        On Stack Overflow, a div with a class of 'post-text'
        indicates that the div is either a question or an answer.

        Different elements of the post-text are printed in different
        colors.

        Headers: White.
        Text: White.
        Quotes: Yellow.
        Lists: Green.
        Code: Syntax Highlighted in self.print_code_block().

        Parameter {BeautifulSoup} post_text: 'soup' of a HTML
        'div' element from a Stack Overflow post with class of
        'post-text.'
        '''

        for element in post_text:
            if element.name == 'h1' or element.name == 'h2' or element.name == 'h3': # Header.
                print(colored(element.text, 'white', attrs=['bold']))
            elif element.name == 'p': # Text.
                print(colored(element.text, 'white'))
            elif element.name == 'blockquote': # Quotes.
                print(colored('    ' + element.text, 'yellow'))
            elif element.name == 'ul': # Lists.
                for li_element in element.find_all('li'):
                    print(colored('    - ' + li_element.text, 'green', attrs=['bold']))
            elif element.name == 'pre': # Code.
                self.print_code_block(element.find('code'))

    def print_code_block(self, code_block):
        '''
        Prints a code block from Stack Overflow with syntax highlighting.

        On Stack Overflow, the code in a HTML 'code' element contains
        a 'span' element for each token. Because of this, it's necessary
        to grab each of the 'code' element's 'span' elements' values to get
        the actual code.

        To highlight the syntax, Pygments PythonLexer is used on the
        code that was grabbed from the 'span' elements inside of the
        'code' element.

        Parameter {BeautifulSoup} code_block: 'soup' of a HTML
        'code' element from a Stack Overflow post.
        '''
        print('')

        # Store the code's text.
        code = ''

        # Loop through code spans.
        for token in code_block:
            code += token

        # Loop over code, and highlight.
        for token, content in pygments.lex(code, PythonLexer()):
            if str(token) == 'Token.Keyword':
                print(colored(content, 'blue'), end='')
            elif str(token) == 'Token.Name.Builtin.Pseudo':
                print(colored(content, 'blue'), end='')
            elif str(token) == 'Token.Literal.Number.Integer':
                print(colored(content, 'green'), end='')
            elif str(token) == 'Token.Literal.Number.Float':
                print(colored(content, 'green'), end='')
            elif str(token) == 'Token.Literal.String.Single':
                print(colored(content, 'yellow'), end='')
            elif str(token) == 'Token.Literal.String.Double':
                print(colored(content, 'yellow'), end='')
            elif str(token) == 'Token.Literal.String.Doc':
                print(colored(content, 'yellow'), end='')
            elif str(token) == 'Token.Comment.Single':
                print(colored(content, 'green'), end='')
            elif str(token) == 'Token.Comment.Hashbang':
                print(colored(content, 'green'), end='')
            else:
                print(content, end='')

        print('')
