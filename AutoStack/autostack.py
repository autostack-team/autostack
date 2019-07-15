#!/usr/bin/env python3
import os
from .SOQuery import WebScraper

exceptions = ['Exception',
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
'NotImplementedError']
   
if __name__ == '__main__':
    # Ensure that the pipe exists; if not, create it.
    if not os.path.exists('./monitorPipe'):
        os.mkfifo('monitorPipe')

    # Open the pipe.
    f = open('monitorPipe', 'r')

    # Inform the user that the script is listening for errors.
    print("Listening for Python errors...")

    # Listen for new stdout.
    while True:
        try:
            # Read a line from the pipe.
            output = f.readline()

            # Pipe closed.
            if output == '':
                break

            # If it's a python error, scrape SO.
            if output.split()[0][:-1] in exceptions:
                # Store user input.
                satisfied = 'no'
                i = 1

                # Find a SO post.
                webscraper = WebScraper()
                searchSoup = webscraper.scrape_so(output.split())

                # Loop over SO post.
                while (satisfied == 'no'):
                    postUrl = webscraper.get_post_url(searchSoup, str(i))
                    
                    if postUrl is None:
                        print("No questions found.")
                    else:
                        answerSoup = webscraper.scrape_question(postUrl)
                        answer_text_soup = webscraper.get_answer(answerSoup)
                        if answer_text_soup is None:
                            print("No answers found.")
                            break
                        else:
                            webscraper.loop_and_print(answer_text_soup)
                    
                    print("Happy with this answer? (yes, no): ")
                    satisfied = input()
                    i += 1

        except UnicodeDecodeError:
            pass