import unittest
import time
import subprocess
from app.SiteScraper import MyScraper

strValidURL = 'https://www.314e.com/'
strInValidURL = 'httpaaa://www.314e.com/'
strTimeOutURL = 'https://192.168.145.111/myapp'

#Test the function that gets data from URLs
class TestSiteScraper(unittest.TestCase):
    oScraper = MyScraper()
    #Valid URL case
    def test_GetContentsOfSite_Valid(self):
        bStatus, strContents = self.oScraper.GetContentsOfSite(strValidURL)
        self.assertEqual(True, bStatus)
    #Invalid URL case
    def test_GetContentsOfSite_Invalid(self):
        bStatus, strContents = self.oScraper.GetContentsOfSite(strInValidURL)
        self.assertEqual(False, bStatus)
    #Not reachable URL
    def test_GetContentsOfSite_Timeout(self):
        start_time = time.time()
        bStatus, strContents = self.oScraper.GetContentsOfSite(strTimeOutURL, nTimeout=10)
        time_taken = int(time.time() - start_time)
        self.assertEqual(False, bStatus)
        self.assertEqual(True, time_taken <= 10)

    #Fetch data form valid URL
    def test_GetWordAndWordPairCounts_Valid(self):
        self.oScraper.GetWordAndWordPairCounts(1, strValidURL)
        self.assertEqual(True, len(self.oScraper.diAllWords) > 0)
        self.assertEqual(True, len(self.oScraper.diAllWordPairs) > 0)

    #fetch data from invalid URL
    def test_GetWordAndWordPairCounts_Invalid(self):
        #Catch the system exit and verify
        with self.assertRaises(SystemExit) as ar:
            self.oScraper.GetWordAndWordPairCounts(1, strInValidURL)
        self.assertEqual(-1, ar.exception.code)
