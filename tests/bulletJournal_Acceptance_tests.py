import os
import unittest
import multiprocessing
import time
from splinter import Browser
from io import StringIO, BytesIO
from urllib.parse import urlparse
from bulletJournal.database import session, Bullet
from datetime import datetime, date

import sys;
os.environ["CONFIG_PATH"] = "bulletJournal.config.TestingConfig"

from bulletJournal import app
from bulletJournal.database import Base, engine, session

# TO RUN
# PYTHONPATH=. python tests/bulletJournal_Acceptance_tests.py

class TestBulletJournalAcceptance(unittest.TestCase):
    """ Tests for BulletJournal """
    
    def setUp(self):
        """ Test setup """
        self.browser = Browser("phantomjs")

        Base.metadata.create_all(engine)

        self.process = multiprocessing.Process(target=app.run,
                                               kwargs={"port": 8080})
        self.process.start()
        time.sleep(1)


    def tearDown(self):
        """ Test teardown """
        
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()
        time.sleep(1)
        
    def test_home_A(self):
        """ Home Test """

        date1 = date(2010, 10, 10)
        
        self.browser.visit("http://127.0.0.1:8080/")
        bullet = self.browser.find_by_css("h2")
        self.assertEqual([], bullet)
        date1 = date1.strftime("%m/%d/%Y")
        self.browser.fill("date", date1)
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date=10%2F10%2F2010")
        #bullet = self.browser.find_by_css("h2")
        
        
        
        
if __name__ == "__main__":
   unittest.main()