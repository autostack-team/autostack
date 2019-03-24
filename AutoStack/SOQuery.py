from bs4 import BeautifulSoup
import requests
from termcolor import colored
#from stackapi import StackAPI
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import NullFormatter
from Error_Parser import parser

# Functions to take an error message, search StackOverflow for an answer, and print the answer to the terminal.
class WebScraper:
    # Returns the parsed html of a page.
    def scrape_so(searchStrings):
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
    def scrape_question(url):
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

    def get_post_url(soup):
        # Find first question.
        theDiv = soup.find("div", {"data-position": "1"})

        # If no questions are found.
        if theDiv == None:
            return None
        
        # Find link to page of first question.
        theLink = theDiv.find("a", {"class": "question-hyperlink"})

        # Get link from a tag.
        theRef = theLink.get("href")
        
        # Get .
        return theRef

    def get_answer(soup):
        # TODO: No accepted Answer exception OR no answers.

        # Get accepted answer.
        theDiv = soup.find("div", {"itemprop": "acceptedAnswer"})

        # If no accepted answer is found.
        if theDiv is None:
            print("looking for another answers")
            # No accepted answers found. Go to top, suggested answer.
            theDiv = soup.find("div", {"itemprop": "suggestedAnswer"})
            # If no answers are present.
            if theDiv is None:
                return None

        # TODO: No results exception.
        # if theDiv is None:
        #     print("Error: no answer")
        #     return

        theText = theDiv.find("div", {"class": "post-text"})

        #print(theText)

        return theText

    def loop_and_print(soup):
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

                #print("")

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

                for j in code:
                    print(j)
            elif i.name == "ul":
                for li in i.find_all("li"):
                    print("    - " + li.text)
                    if li.find("a") is not None:
                        link = li.find("a").get("href")
                        print("        link to: " + link)
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'yellow'))
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'yellow'))
        return

if __name__ == "__main__":
    #stringToSearch = ["bad", "request", "error", "flask"]
    
    #stringToSearch = ["how", "to", "get", "text", "from", "span", "tag", "in", "beautifulsoup"]
    with open('/Users/bensanders/repos/AutoStack/error.txt', 'r') as myfile:
        stuff=myfile.read()
    stringToSearch = parser.get_last_line_as_array(stuff)
    searchSoup = WebScraper.scrape_so(stringToSearch)
    postUrl = WebScraper.get_post_url(searchSoup)
    postUrl = "https://stackoverflow.com/questions/55178365/split-text-into-multiple-lines-based-on-pipe-and-cap-delimiter-oracle-pl-sql-p"
    
    if postUrl is None:
        print("No questions found.")
    else:
        answerSoup = WebScraper.scrape_question(postUrl)
        answer_text_soup = WebScraper.get_answer(answerSoup)
        if answer_text_soup is None:
            print("No answers found.")
        else:
            WebScraper.loop_and_print(answer_text_soup)
    #print(returnThing)