import os
import unittest
import multiprocessing
import time
from splinter import Browser
from io import StringIO, BytesIO
from urllib.parse import urlparse
import sys;
from datetime import datetime, date

os.environ["CONFIG_PATH"] = "bulletJournal.config.TestingConfig"
from bulletJournal import app
from bulletJournal.database import session, Bullet, Base, engine

import signal
import psutil


# TO RUN
# PYTHONPATH=. python tests/test_views_acceptance.py

class TestBulletJournalAcceptance(unittest.TestCase):
    """ Tests for BulletJournal """
    
    def setUp(self):
        """ Test setup """
        
        self.browser = Browser("phantomjs")
        
        Base.metadata.create_all(engine)
        
        
        self.process = multiprocessing.Process(target=app.run,
                                               kwargs={"port": 8080})
                                               
        if self.process and not self.process.is_alive():
            self.process.start()
        time.sleep(1)


    def tearDown(self):
        """ Test teardown """
        
        toRemove = session.query(Bullet).all()
        for item in toRemove:
            session.delete(item)
        session.commit()
        
        # self.process.terminate()
        pid = self.process.pid
        
        p = psutil.Process(pid)
        p.terminate() # or p.kill()
        time.sleep(1)
        
        session.close()
        engine.dispose()
        # Base.metadata.drop_all(engine)
        # self.browser.process.send_signal(signal.SIGTERM)
        self.browser.quit()
        # time.sleep(1)
        os.system("pkill phantomjs")
        time.sleep(1)
        
    def test_editBullet(self):
        """ Edit Bullet """
        
        count = session.query(Bullet).count()
        
        date1 = date(2010, 10, 10)
        bullet1 = Bullet(contentType = "task", content = "edit test", date=date1, complete=0)
        session.add(bullet1)
        session.commit()
        
        self.browser.visit("http://127.0.0.1:8080/")
        self.browser.fill("date", date(2010, 10, 10).strftime("%m/%d/%Y"))
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date={}".format(date(2010, 10, 10).strftime("%m/%d/%Y").replace("/", "%2F")))
        self.assertEqual(self.browser.is_text_present("edit test"), True)
        
        self.browser.click_link_by_text("Edit Bullet")
        
        self.browser.choose("contentType", "event")
        self.browser.fill("content", "edit test complete")
        self.browser.fill("date", date(2010, 10, 10).strftime("%m/%d/%Y"))
        
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")
        
        self.browser.fill("date", date(2010, 10, 10).strftime("%m/%d/%Y"))
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date={}".format(date(2010, 10, 10).strftime("%m/%d/%Y").replace("/", "%2F")))
        
    def test_deleteBullet(self):
        """ Delete Test """
        
        # pre-populate date
        date1 = date(2010, 10, 10)
        bullet1 = Bullet(contentType = "task", content = "delete test", date=date1, complete=0)
        session.add(bullet1)
        session.commit()
        
        # change date
        self.browser.visit("http://127.0.0.1:8080/")
        self.browser.fill("date", date(2010, 10, 10).strftime("%m/%d/%Y"))
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date={}".format(date(2010, 10, 10).strftime("%m/%d/%Y").replace("/", "%2F")))
        
        # delete bullet
        self.assertEqual(self.browser.is_text_present("delete test"), True)
        self.browser.click_link_by_text("Delete Bullet")
        
        # check return to homepage
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")
        
        # go to 10-10-10 check for no bullets
        self.browser.fill("date", date(2010, 10, 10).strftime("%m/%d/%Y"))
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date={}".format(date(2010, 10, 10).strftime("%m/%d/%Y").replace("/", "%2F")))
        self.assertEqual(self.browser.is_text_present("delete test"), False)
        
        
    def test_completeBullet(self):
        """ Complete Test """
        
        #pre-populate date
        date1 = date(2010, 10, 10)
        bullet1 = Bullet(contentType = "task", content = "complete test", date=date1, complete=0)
        session.add(bullet1)
        session.commit()
        
        #change date
        self.browser.visit("http://127.0.0.1:8080/")
        self.browser.fill("date", date(2010, 10, 10).strftime("%m/%d/%Y"))
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date={}".format(date(2010, 10, 10).strftime("%m/%d/%Y").replace("/", "%2F")))
        
        #delete bullet
        self.assertEqual(self.browser.is_text_present("complete test"), True)
        self.browser.click_link_by_text("Complete Bullet")
        
        #check return to homepage
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")
        
        #go to 10-10-10 check for no bullets
        self.browser.fill("date", date(2010, 10, 10).strftime("%m/%d/%Y"))
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date={}".format(date(2010, 10, 10).strftime("%m/%d/%Y").replace("/", "%2F")))
        self.assertEqual(self.browser.is_text_present("complete test"), False)
        
    def test_addBullet(self):
        """ Add Test """
        
        self.browser.visit("http://127.0.0.1:8080/bullet/add")
        
        self.browser.choose("contentType", "task")
        self.browser.fill("content", "add test")
        self.browser.fill("date", date(2010, 10, 10).strftime("%m/%d/%Y"))
        
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")
        
        self.browser.fill("date", date(2010, 10, 10).strftime("%m/%d/%Y"))
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date={}".format(date(2010, 10, 10).strftime("%m/%d/%Y").replace("/", "%2F")))
        
        self.assertEqual(self.browser.is_text_present("add test"), True)
        
    def test_homepage(self):
        """ Home Test """
        
        date1 = date(2010, 10, 10)
        
        self.browser.visit("http://127.0.0.1:8080/")
        bullet = self.browser.find_by_tag('h2')
        self.assertEqual([], bullet)
        self.browser.fill("date", date1.strftime("%m/%d/%Y"))
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date={}".format(date1.strftime("%m/%d/%Y").replace("/", "%2F")))
        
    def test_search(self):
        """ Search Test """
        
        date1 = date(2010, 10, 10)
        bullet1 = Bullet(contentType = "task", content = "search test", date=date1, complete=0)
        session.add(bullet1)
        session.commit()
        
        self.browser.visit("http://127.0.0.1:8080/bullet/search")
        self.browser.fill("q", "search test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/bullet/search?q=search+test")
        self.assertEqual(self.browser.is_text_present("search test"), True)
        
    def test_backlog(self):
        """ Backlog Test """
        
        date1 = date(2010, 10, 10)
        bullet1 = Bullet(contentType = "task", content = "backlog test", date=date1, complete=0)
        session.add(bullet1)
        session.commit()

        self.browser.visit("http://127.0.0.1:8080/bullet/backlog")
        self.browser.check("backlog_list")
        
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        
        newDate = date.today()
        newMonth = newDate.month
        if newMonth == 12:
            newMonth = 1
        else:
            newMonth += 1
        newDate = newDate.replace(newMonth)
        
        self.assertEqual(bullet1.date, newDate)
    
if __name__ == "__main__":
   unittest.main()