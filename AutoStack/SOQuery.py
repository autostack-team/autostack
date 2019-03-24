from bs4 import BeautifulSoup
import requests
from termcolor import colored
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import NullFormatter

# Functions to take an error message, search StackOverflow for an answer, and print the answer to the terminal.
class WebScraper:
    # Returns the parsed html of a page.
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
        print("Getting post from: " + url)

        # Request page.
        r = requests.get(url)

        # Get html from page.
        html_doc = r.text

        # Convert html to soup object.
        soup = BeautifulSoup(html_doc, 'lxml')

        # Return soup object.
        return soup

    def get_post_url(self, soup):
        # Find first question.
        theDiv = soup.find("div", {"data-position": "1"})

        # If no questions are found.
        if theDiv == None:
            return None
        
        # Find link to page of first question.
        theLink = theDiv.find("a", {"class": "question-hyperlink"})

        # Get link from a tag.
        theRef = theLink.get("href")
        
        # Return link to post.
        return theRef

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

    def loop_and_print(self, soup):
        # Formatting in terminal.
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'yellow'))
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'yellow'))
        
        # Loop through soup objects.
        for i in soup:
            # If the object is a paragraph.
            if i.name == "p":
                print(colored(i.text, 'red'))

            # If the object is a quote.
            elif i.name == "blockquote":
                print(colored("    " + i.text, 'green'))

            # If the object is in a pre tag.
            elif i.name == "pre":
                # Formatting.
                print("\n")

                # Find the code block.
                code = i.find("code")

                # Loop through the elements in the code block.
                # for j in code:
                #     # Print the highlited code.
                #     # if j.get("class") == None:
                #     #     print("IT FINALLY WORKS")
                #     try:
                #         print(j.get("class"))
                #         print(highlight(str(j), PythonLexer(), NullFormatter()))
                #     except NavigableString:
                #         pass

                # Loop through code spans.
                for j in code:
                    print(j)
            # If the object is an unordered list.
            elif i.name == "ul":
                # Loop through list items.
                for li in i.find_all("li"):
                    print("    - " + li.text)
                    # If a link is present.
                    if li.find("a") is not None:
                        # Get link text.
                        link = li.find("a").get("href")
                        print("        link to: " + link)
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'yellow'))
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'yellow'))
        return