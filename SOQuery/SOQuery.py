from bs4 import BeautifulSoup
import requests
from termcolor import colored
#from stackapi import StackAPI
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


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

        # Returns soup object.
        return soup

    # Scrapes html from question.
    def scrape_question(url):
        # Builds url to question.
        url = "https://stackoverflow.com/" + url

        r = requests.get(url)

        html_doc = r.text

        soup = BeautifulSoup(html_doc, 'lxml')

        return soup

    def get_post_url(soup):
        #postUrl = soup("div")

        theDiv = soup.find("div", {"data-position": "1"})
        #print(theDiv)
        theLink = theDiv.find("a", {"class": "question-hyperlink"})
        theRef = theLink.get("href")
        #print(theLink.get("href"))
        
        return theRef

    def get_answer(soup):
        theDiv = soup.find("div", {"itemprop": "acceptedAnswer"})

        # if theDiv is None:
        #     print("Error: no answer")
        #     return

        theText = theDiv.find("div", {"class": "post-text"})

        #print(theText)

        return theText

    def loop_and_print(soup):
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'yellow'))
        for i in soup:
            #print(i.name)
            if i.name == "p":
                print(colored(i.text, 'red'))
            elif i.name == "blockquote":
                print(colored("    " + i.text, 'green'))
            elif i.name == "pre":
                print("\n")
                code = i.find("code")
                #print(code)
                for j in code:
                    #span = j.find("span")
                    print(colored(j, "blue"))
                    #print(highlight(str(j), PythonLexer(), HtmlFormatter()))
        
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'yellow'))
        return

if __name__ == "__main__":
    #stringToSearch = ["bad", "request", "error", "flask"]
    stringToSearch = ["how", "to", "get", "text", "from", "span", "tag", "in", "beautifulsoup"]
    searchSoup = WebScraper.scrape_so(stringToSearch)
    postUrl = WebScraper.get_post_url(searchSoup)

    answerSoup = WebScraper.scrape_question(postUrl)
    answer_text_soup = WebScraper.get_answer(answerSoup)
    WebScraper.loop_and_print(answer_text_soup)
    #print(returnThing)
