# WebScraper
Display the top 10 frequent words and the top 10 frequent word pairs

# Details of Project structure
WebScraping\app contains the implementation
WebScraping\tests contains the unit tests
WebScraping\venv contains the virtual env
WebScraping\sampleOutputFor2Levels.log contains the sample output console log
WebScraping\worddata.txt is the example output file that gets created on running the script which contains the word count
WebScraping\wordpairdata.txt is the example output file that gets created on running the script which contains the word pair count

# Execution
1. Activate the virtual env: virenv\Scripts\activate
2. Execute the script with commandline arguments: python app\SiteScraper.py --levels 4 --url https://www.314e.com/
Both URL and the levels can be provided as parameters.
Output files:
   1. worddata.txt -> Word count
   2. wordpairdata.txt -> word pair count

The script can easily be integrated to a CI job as well.

