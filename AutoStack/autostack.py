#!/usr/bin/env python3
import subprocess
from SOQuery import WebScraper

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
    # Command to run the .d stdout script.
    cmd = ["sudo", "dtrace", "-q", "-s", "/usr/bin/AutoStack/stdout.d"]

    # Listen for stdout.
    stdout_listener = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    # Inform the user that the script is listening for errors.
    print("Listening for Python errors...")

    # Listen for new stdout.
    while True:
        try:
            # Grab the output from the .d script.
            output = stdout_listener.stdout.readline().decode("utf-8")

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