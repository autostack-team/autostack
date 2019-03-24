from bs4 import BeautifulSoup
import requests
from termcolor import colored
import pygments
from pygments.lexers import PythonLexer

# Functions to take an error message, search StackOverflow for an answer, and print the answer to the terminal.
class WebScraper:
    # Returns the parsed html of a search page.
    def scrape_so(self, searchStrings):
        # Url string to get html from.
        url = "https://stackoverflow.com/search?q="

        # Build url to search.
        url = url + searchStrings[0]
        for i in searchStrings[1:]:
            url = url + "+" + i

        # Request page.
        r = requests.get(url)

        # Get html from page.
        html_doc = r.text

        # Convert html to BeautfulSoup object.
        soup = BeautifulSoup(html_doc, 'lxml')

        # Return soup object.
        return soup

    # Scrapes html from question.
    def scrape_question(self, url):
        # Builds url to question.
        url = "https://stackoverflow.com/" + url
        print(colored("Getting post from: " + url, 'yellow'))

        # Request page.
        r = requests.get(url)

        # Get html from page.
        html_doc = r.text

        # Convert html to soup object.
        soup = BeautifulSoup(html_doc, 'lxml')

        # Return soup object.
        return soup

    # Gets the url of a post to scrape.
    def get_post_url(self, soup, data_position = "1"):
        # Find first question.
        theDiv = soup.find("div", {"data-position": data_position})

        # If no questions are found.
        if theDiv == None:
            return None
        
        # Find link to page of first question.
        theLink = theDiv.find("a", {"class": "question-hyperlink"})

        # Get link from a tag.
        theRef = theLink.get("href")
        
        # Return link to post.
        return theRef

    # Finds accepted answer, if it exists, and returns a BeautifulSoup object of the html.
    def get_answer(self, soup):
        # Get accepted answer.
        theDiv = soup.find("div", {"itemprop": "acceptedAnswer"})

        # If no accepted answer is found.
        if theDiv is None:
            return None

        # Get text of post.
        theText = theDiv.find("div", {"class": "post-text"})

        # Return post text.
        return theText

    # Traverses through a BeautifulSoup object of the answer's text and prints the text.
    def loop_and_print(self, soup):
        # Formatting in terminal.
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'red'))
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'red'))
        
        # Loop through soup objects.
        for i in soup:
            # If the object is a paragraph.
            if i.name == "p":
                print(colored(i.text, 'white'))

            # If the object is a quote.
            elif i.name == "blockquote":
                print(colored("    " + i.text, 'green'))

            # If the object is in a pre tag.
            elif i.name == "pre":
                # Formatting.
                print("\n")

                # Find the code block.
                code = i.find("code")

                # Store the code.
                code_to_be_colored = ''

                # Loop through code spans.
                for j in code:
                    code_to_be_colored += j

                # Loop over code, and highlight.
                for token, content in pygments.lex(code_to_be_colored, PythonLexer()):
                    if str(token) == "Token.Keyword":
                        print(colored(content, 'blue'), end='')
                    elif str(token) == "Token.Name.Builtin.Pseudo":
                        print(colored(content, 'blue'), end='')
                    elif str(token) == "Token.Literal.Number.Integer":
                        print(colored(content, 'green'), end='')
                    elif str(token) == "Token.Literal.Number.Float":
                        print(colored(content, 'green'), end='')
                    elif str(token) == "Token.Literal.String.Single":
                        print(colored(content, 'yellow'), end='')
                    elif str(token) == "Token.Literal.String.Double":
                        print(colored(content, 'yellow'), end='')
                    elif str(token) == "Token.Literal.String.Doc":
                        print(colored(content, 'yellow'), end='')
                    elif str(token) == "Token.Comment.Single":
                        print(colored(content, 'green'), end='')
                    elif str(token) == "Token.Comment.Hashbang":
                        print(colored(content, 'green'), end='')
                    else:
                        print(content, end='')
                print('')

            # If the object is an unordered list.
            elif i.name == "ul":
                # Loop through list items.
                for li in i.find_all("li"):
                    print(colored("    - " + li.text, 'yellow', attrs=['bold']))
                    # If a link is present.
                    if li.find("a") is not None:
                        # Get link text.
                        link = li.find("a").get("href")
                        print(colored("        link to: " + link, 'yellow', attrs=['bold']))
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'red'))
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'red'))
        return