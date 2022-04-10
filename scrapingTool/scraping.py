from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint

class GetData():
    def __init__(self):
        pass

    def connect(self, url): 
        html = urlopen(url).read()
        self.soup = BeautifulSoup(html, features="html.parser")

    def getAllText(self):     
        # kill all script and style elements
        for script in self.soup(["script", "style"]):
            script.extract()    # rip it out
        # get text
        text = self.soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def getCategories(self):
        categories = []
        for div in self.soup.findAll('div', {'class': 'category'}):
            categories.append(div.text.strip())
        return categories
            
    def getWinners(self, text, categories):
        winners = {}
        for i in range(len(categories)):

            if i + 1< len(categories):
                winners[categories[i]] = text.split(categories[i])[1].split(categories[i+1])[0]
            elif i < len(categories):
                winners[categories[i]] = text.split(categories[i])[1].split("Copyright")[0]
        return winners

    def cleanJson(self, json):
        newValues = {}
        for i in json:
            nomineeDict = {"Winners": [], "Nominees": []}
            nominees = json[i].splitlines()
            for j in nominees:
                if "Winner" in j:
                    nomineeDict["Winners"].append(j)
                else:
                    nomineeDict["Nominees"].append(j)
            newValues[i] = nomineeDict
        pprint(newValues)

url = "http://www.sfadb.com/World_Fantasy_Awards_2021"
getData = GetData()
getData.connect(url)
text = getData.getAllText()
text = text.split("Judges:")[1]
categories = getData.getCategories()
winners = getData.getWinners(text, categories)
getData.cleanJson(winners)