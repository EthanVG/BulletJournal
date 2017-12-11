import os
import unittest
import multiprocessing
import time
from splinter import Browser
from io import StringIO, BytesIO
from urllib.parse import urlparse
import sys;
os.environ["CONFIG_PATH"] = "bulletJournal.config.TestingConfig"
from bulletJournal.database import session, Bullet, Base, engine
from bulletJournal import app
from datetime import datetime, date
import signal
import psutil


# TO RUN
# PYTHONPATH=. python tests/test_views_acceptance.py

class TestBulletJournalAcceptance(unittest.TestCase):
    """ Tests for BulletJournal """
    
    def setUp(self):
        """ Test setup """
        print("SETUP")
        
        self.browser = Browser("phantomjs")
        
        Base.metadata.create_all(engine)
        
        
        self.process = multiprocessing.Process(target=app.run,
                                               kwargs={"port": 8080})
                                               
        if self.process and not self.process.is_alive():
            self.process.start()
        time.sleep(1)


    def tearDown(self):
        """ Test teardown """
        print("TEARDOWN")
        
        toRemove = session.query(Bullet).all()
        for item in toRemove:
            session.delete(item)
        session.commit()
        
        #self.process.terminate()
        pid = self.process.pid
        
        p = psutil.Process(pid)
        p.terminate() #or p.kill()
        time.sleep(1)
        print(self.process.is_alive())
        if(self.process.exitcode == -signal.SIGTERM):
            print("TERMINATE SUCCESS")
        else:
            print("TERMINATE FAIL")
        session.close()
        engine.dispose()
        #Base.metadata.drop_all(engine)
        #self.browser.process.send_signal(signal.SIGTERM)
        self.browser.quit()
        #time.sleep(1)
        os.system("pkill phantomjs")
        time.sleep(1)
        print(self.process.is_alive())
        if(self.process.exitcode == -signal.SIGTERM):
            print("TERMINATE SUCCESS 2")
        else:
            print("TERMINATE FAIL 2")
        
    def test_editBullet(self):
        """ Edit Bullet """
        print("START EDIT TEST")
        
        count = session.query(Bullet).count()
        print("COUNT 1: {}".format(count))
        
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
        print(self.browser.find_by_tag("h2").text)
        
        print("EDIT TEST END")
        
    def test_deleteBullet(self):
        """ Delete Test """
        print("DELETE TEST START")
        
        #pre-populate date
        date1 = date(2010, 10, 10)
        bullet1 = Bullet(contentType = "task", content = "delete test", date=date1, complete=0)
        session.add(bullet1)
        session.commit()
        
        #change date
        self.browser.visit("http://127.0.0.1:8080/")
        self.browser.fill("date", date(2010, 10, 10).strftime("%m/%d/%Y"))
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date={}".format(date(2010, 10, 10).strftime("%m/%d/%Y").replace("/", "%2F")))
        
        #delete bullet
        self.assertEqual(self.browser.is_text_present("delete test"), True)
        self.browser.click_link_by_text("Delete Bullet")
        
        #check return to homepage
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")
        
        #go to 10-10-10 check for no bullets
        self.browser.fill("date", date(2010, 10, 10).strftime("%m/%d/%Y"))
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date={}".format(date(2010, 10, 10).strftime("%m/%d/%Y").replace("/", "%2F")))
        self.assertEqual(self.browser.is_text_present("delete test"), False)
        
        print("DELETE TEST END")
        
    def test_completeBullet(self):
        """ Complete Test """
        
        print("COMPLETE TEST START")
        
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
        
        print("COMPLETE TEST END")
        
    def test_addBullet(self):
        """ Add Test """
        print("START ADD TEST")
        
        self.browser.visit("http://127.0.0.1:8080/")
        self.browser.click_link_by_text("Add Bullet")
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/bullet/add")
        
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
        
        print("END ADD TEST")
        
    def test_homepage(self):
        """ Home Test """
        print("START HOME TEST")
        
        date1 = date(2010, 10, 10)
        
        self.browser.visit("http://127.0.0.1:8080/")
        bullet = self.browser.find_by_tag('h2')
        self.assertEqual([], bullet)
        self.browser.fill("date", date1.strftime("%m/%d/%Y"))
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/?date={}".format(date1.strftime("%m/%d/%Y").replace("/", "%2F")))
        
        print("END HOME TEST")
        
        
    def test_search(self):
        """ Search Test """
        
        print("SEARCH TEST START")
        
        date1 = date(2010, 10, 10)
        bullet1 = Bullet(contentType = "task", content = "search test", date=date1, complete=0)
        session.add(bullet1)
        session.commit()
        
        self.browser.visit("http://127.0.0.1:8080/")
        self.browser.click_link_by_text("Search Bullet")
        
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/bullet/search")
        self.browser.fill("q", "search test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/bullet/search?q=search+test")
        self.assertEqual(self.browser.is_text_present("search test"), True)
        
        print("SEARCH TEST END")
        
    def test_backlog(self):
        """ Backlog Test """
        
        print("BACKLOG TEST START")
        
        date1 = date(2010, 10, 10)
        bullet1 = Bullet(contentType = "task", content = "backlog test", date=date1, complete=0)
        session.add(bullet1)
        session.commit()
        
        self.browser.visit("http://127.0.0.1:8080/")
        self.browser.click_link_by_text("Backlog")
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/bullet/backlog")
        
        print(self.browser.find_by_tag("h2").text)
        
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
        
        print("BACKLOG TEST END")
    
if __name__ == "__main__":
   unittest.main()