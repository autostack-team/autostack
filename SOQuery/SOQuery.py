from bs4 import BeautifulSoup
import requests
#from stackapi import StackAPI


class WebScraper:


    # Returns the parsed html of a page.
    def scrape_so(searchStrings):
        
        url = "https://stackoverflow.com/search?q="

        # Build url to search.
        url = url + searchStrings[0]
        for i in searchStrings[1:]:
            url = url + "+" + i
        #print(url)

        # Request page.
        r = requests.get(url)

        # Get html from page.
        html_doc = r.text

        # Convert html to BeautfulSoup lxml.
        soup = BeautifulSoup(html_doc, 'lxml')

        # Returns lxml.
        return soup

    def scrape_question(url):
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
        theTextDiv = theDiv.get("div", {"class": "post-text"})
        

        print(theDiv.find_all("p"))
        print(theDiv.find_all("blockquote"))



if __name__ == "__main__":
    stringToSearch = ["bad", "request", "error", "flask"]
    searchSoup = WebScraper.scrape_so(stringToSearch)
    postUrl = WebScraper.get_post_url(searchSoup)

    answerSoup = WebScraper.scrape_question(postUrl)
    WebScraper.get_answer(answerSoup)
    #print(returnThing)
