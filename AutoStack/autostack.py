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
    cmd = ["sudo", "dtrace", "-q", "-s", "stdout.d"]

    # Listen for stdout.
    stdout_listener = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    # Listen for new stdout.
    while True:
        try:
            output = stdout_listener.stdout.readline().decode("utf-8")
            print(output.split()[0][:-1])
            if output.split()[0][:-1] in exceptions:
                searchSoup = WebScraper.scrape_so(output.split())
                postUrl = WebScraper.get_post_url(searchSoup)
                
                if postUrl is None:
                    print("No questions found.")
                else:
                    answerSoup = WebScraper.scrape_question(postUrl)
                    answer_text_soup = WebScraper.get_answer(answerSoup)
                    if answer_text_soup is None:
                        print("No answers found.")
                    else:
                        WebScraper.loop_and_print(answer_text_soup)
        except UnicodeDecodeError:
            pass