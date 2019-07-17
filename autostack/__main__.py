#!/usr/bin/env python3
from __future__ import print_function # Allows use of the python 3 print function.
import os
from WebScraper.StackOverflowScraper import StackOverflowScraper

EXCEPTIONS = [
    'Exception',
    'StopIteration',
    'SystemExit',
    'StandardError',
    'ArithmeticError',
    'OverflowError',
    'FloatingPointError',
    'ZeroDivisionError',
    'AssertionError',
    'AttributeError',
    'EOFError',
    'ImportError',
    'KeyboardInterrupt',
    'LookupError',
    'IndexError',
    'KeyError',
    'NameError',
    'UnboundLocalError',
    'EnvironmentError',
    'IOError',
    'OSError',
    'SyntaxError',
    'IndentationError',
    'SystemError',
    'SystemExit',
    'TypeError',
    'ValueError',
    'RuntimeError',
    'NotImplementedError'
]
   
def main():
    '''
    Listens for python errors outputed in autostack-terminals.
    '''

    # Ensure that the pipe exists; if not, create it.
    if not os.path.exists('/tmp'):
        os.mkdir('/tmp')
        os.mkfifo('/tmp/monitorPipe')
    elif not os.path.exists('/tmp/monitorPipe'):
        os.mkfifo('/tmp/monitorPipe')
        
    # Open the pipe.
    f = open('/tmp/monitorPipe', 'r')
    print("Development terminal opened - listening for Python errors...")

    # Listen for new stdout.
    while True:
        try:
            # Read a line from the pipe.
            output = f.readline()

            # Pipe closed.
            if output == '':
                break

            # If the current line of output is a python error, query Stack Overflow.
            if output.split()[0][:-1] in EXCEPTIONS:
                # Store user input.
                satisfied = 'n'
                i = 1

                # Query Stack Overflow for the error.
                so_scraper = StackOverflowScraper()
                query_soup = so_scraper.query(output.split())

                # Loop over the Stack Overflow posts from the query.
                while (True):
                    if satisfied == 'n':
                        pass
                    elif satisfied == 'Y':
                        break
                    else:
                        print("Invalid input! (Y/n): ")
                        satisfied = input()
                        continue

                    post_url = so_scraper.get_post_url(searchSoup, str(i))
                    
                    if post_url is None:
                        print("No questions found.")
                    else:
                        post_soup = so_scraper.scrape_question(post_url)
                        answer_soup = so_scraper.get_answer(post_soup)
                        
                        if answer_soup is None:
                            print("No answers found.")
                            break
                        else:
                            so_scraper.loop_and_print(answer_soup)
                    
                    print("Happy with this answer? (Y/n): ")
                    satisfied = input()
                    i += 1
        except UnicodeDecodeError:
            pass

if __name__ == '__main__':
    main()