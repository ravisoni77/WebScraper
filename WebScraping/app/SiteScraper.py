import requests
import argparse
import sys
import re
import os
from bs4 import BeautifulSoup as BS
from itertools import islice
from collections import Counter

class MyScraper(object):
    #Dictionary for the words and counts
    diAllWords = {}
    diAllWordPairs = {}
    #We don't need the text from some of the tags
    liUnwantedTags = [
        'html',
        'script',
        'head',
        'style',
        '[document]',
        'meta',
    ]
    #To skip already fetched sites
    liSitesFetched = []

    #Get the contents of a site
    def GetContentsOfSite(self, strURL, nTimeout=60):
        try:
            oData = requests.get(strURL, timeout=nTimeout) 
            return True, oData.content
        except requests.exceptions.RequestException as ex:
            return False, ex
        except Exception as ex:
            return False, ex

    #Get the word and word pair count from the given string
    def GetWordAndWordPairCounts(self, nLevels, strURL):
        #Get contents
        tuRetData = self.GetContentsOfSite(strURL)
        if not tuRetData[0]:
            print (f"Could not fetch the data. Error: {tuRetData[1]}")
            sys.exit(-1)
        print (f'Successfully fetched the data from site {strURL}')
        oSoup = BS(tuRetData[1].decode(), 'html.parser')
        oData = oSoup.find_all(text=True)
        for ele in oData:
            if ele.parent.name not in self.liUnwantedTags:
                #Get the words in the string
                liWords = re.findall('\w+', ele)
                #Get the word pairs and their counts 
                diWordPairs = dict(Counter(zip(liWords, islice(liWords, 1, None))))
                #Add to the global dictionary count
                for tuWordPair in diWordPairs:
                    if tuWordPair in self.diAllWordPairs:
                        self.diAllWordPairs[tuWordPair] += diWordPairs[tuWordPair]
                    else:
                        self.diAllWordPairs[tuWordPair] = diWordPairs[tuWordPair]
                #Get the Word count
                diWords = dict(Counter(liWords))
                #Add to the global dictionary count
                for strWord in diWords:
                    if strWord in  self.diAllWords:
                        self.diAllWords[strWord] += diWords[strWord]
                    else:
                        self.diAllWords[strWord] = diWords[strWord]
        self.liSitesFetched.append(strURL)
        if nLevels == 1:
            return
        else:
            nLevels -= 1
            print (f'Level ------------------------------------------------ {nLevels}')
            for link in oSoup.find_all('a', href=True):
                strLink = link['href']
                if strLink.startswith('http://') or strLink.startswith('https://') and strLink not in self.liSitesFetched:
                    print (f'Trying to fetch data from site --> {strLink}')
                    self.GetWordAndWordPairCounts(nLevels, strLink)
                else:
                    print (f'Site --> {strLink} is not valid or is already searched.')


if __name__ == "__main__":
    oArgPraser = argparse.ArgumentParser()

    #URL as input
    oArgPraser.add_argument('--url', help="URL of the site that needs to be scanned", type=str, default='https://www.314e.com/')
    #Number of levels that needs to be checked
    oArgPraser.add_argument('--levels', help="Number of levels that needs to be checked", type=int, default=4)

    #Collect the arguments
    args = oArgPraser.parse_args()
    strURL = args.url
    nLevels = args.levels

    oScraper = MyScraper()
    #Get the words and word pairs count using recursive function
    oScraper.GetWordAndWordPairCounts(nLevels, strURL)

    #Sort based on occurance count
    liWordData = sorted(oScraper.diAllWords.items(), key=lambda x: x[1], reverse=True)
    liWordPairData = sorted(oScraper.diAllWordPairs.items(), key=lambda x: x[1], reverse=True)

    #Get the top 10
    if len(liWordData) > 10:
        liWordData = liWordData[:10]
    if len(liWordPairData) > 10:
        liWordPairData = liWordPairData[:10]

    #Print the sites searched for data
    print ('--------------------------------Sites---------------------------------')
    print ('\n'.join(oScraper.liSitesFetched))
    print ('----------------------------------------------------------------------')
    #Print the words
    print ('----------------------------------WordCountData-----------------------------------')
    print (dict(liWordData))
    print ('--------------------------------WordPairCountData---------------------------------')
    print (dict(liWordPairData))
    print ('----------------------------------------------------------------------------------')

    #Write into output files which can be read by another program or CI job
    with open('worddata.txt', 'w') as wd:
        wd.write(('\n'.join(map(str,liWordData))))
    with open('wordpairdata.txt', 'w') as wd:
        wd.write(('\n'.join(map(str,liWordPairData))))
    



