import unittest
import os
import shutil
from urllib.parse import urlparse
from io import StringIO, BytesIO
from bulletJournal.database import Bullet
from datetime import date
import logging

os.environ["CONFIG_PATH"] = "bulletJournal.config.TestingConfig"
from bulletJournal.database import Base, engine, session
from bulletJournal import app

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
    
# TEST LOGGER
test_logger = setup_logger('test_logger', 'test.log')

class TestBulletJournal(unittest.TestCase):
    """ Tests for BulletJournal """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        test_logger.info('I: SETUP COMPLETE')

    def tearDown(self):
        """ Test teardown """
        session.close()

        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        test_logger.info('I: TEARDOWN COMPLETE')
        
    #Unit Tests
    
    def test_migrateBullet(self):
        """ Test migrating an bullet """

        test_logger.info('I: Migrate Test Start')

        date1 = date(2017, 10, 10)
        date2 = date(2017, 11, 11)
        
        bullet1 = Bullet(contentType = "task", content = "add test", date=date1, complete=0)
        
        bullet1.migrate(date2)
        self.assertEqual(bullet1.date, date2)

        test_logger.info('I: Migrate Test End')
    
    #Integration Tests
    
    #Empty bullet server test
    def test_emptyServer_I(self):
        """ Test home page of empty bullets"""

        test_logger.info('I: Get Empty Server Test Start')

        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        bullets = session.query(Bullet).all()
        self.assertEqual(len(bullets), 0)

        test_logger.info('I: Get Empty Server Test End')
    
    #Add bullet test
    def test_addBullet_I(self):
        """ Test adding a bullet """

        test_logger.info('I: Add Bullet Test Start')

        response = self.client.post("/bullet/add", data={
            "contentType": "task",
            "content": "test",
            "date": date.today(),
            "complete": 0
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        bullets = session.query(Bullet).all()
        self.assertEqual(len(bullets), 1)
        
        bullet = bullets[0]
        
        self.assertEqual(bullet.contentType, "task")
        self.assertEqual(bullet.content, "test")
        self.assertEqual(bullet.date, date.today())
        self.assertEqual(bullet.complete, 0)

        test_logger.info('I: Add Bullet Test End')
    
    #Edit Bullet
    def test_editBullet(self):
        """ Test editing a bullet """

        test_logger.info('I: Edit Bullet Test Start')

        bullet = Bullet(contentType = "task", content = "edit test", date=date.today(), complete=0)
        session.add(bullet)
        session.commit()
        
        response = self.client.post("/bullet/1/edit", data={
            "contentType": "note",
            "content": "edit test changed",
            "date": date.today(),
            "complete": 0
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        bullets = session.query(Bullet).all()
        self.assertEqual(len(bullets), 1)
        
        bullet = bullets[0]
        
        self.assertEqual(bullet.contentType, "note")
        self.assertEqual(bullet.content, "edit test changed")
        self.assertEqual(bullet.date, date.today())
        self.assertEqual(bullet.complete, 0)
        
        test_logger.info('I: Edit Bullet Test End')
    
    #Migrate Bullet
    def test_migrateBullet_I(self):
        """ Test migrating a bullet """

        test_logger.info('I: Migrate Bullet Test Start')

        bullet1 = Bullet(contentType = "task", content = "migrate test", date=date.today(), complete = 0)
        session.add(bullet1)
        session.commit()
        
        date1 = date(2017, 10, 10)
        
        response = self.client.post("/bullet/1/migrate", data={
            "date": date1
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        bullets = session.query(Bullet).all()
        self.assertEqual(len(bullets), 1)
        
        bullet = bullets[0]
        
        self.assertEqual(bullet1.date, date(2017, 10, 10))
    
        test_logger.info('I: Migrate Bullet Test End')
    
    #Complete Bullet
    def test_completeBullet_I(self):
        """ Test for completed bullet """

        test_logger.info('I: Complete Bullet Test Start')

        bullet1 = Bullet(contentType = "task", content = "complete test", date=date.today(), complete = 0)
        session.add(bullet1)
        session.commit()
        
        response = self.client.post("/bullet/1/complete", data={
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        bullets = session.query(Bullet).all()
        self.assertEqual(len(bullets), 1)
        
        bullet = bullets[0]
        
        self.assertEqual(bullet1.complete, 1)
        
        test_logger.info('I: Complete Bullet Test End')
    
    
    #Delete Bullet
    def test_deleteBullet_I(self):
        """ Test for deleted bullet """

        test_logger.info('I: Delete Bullet Test Start')

        bullet1 = Bullet(contentType = "task", content = "delete test", date=date.today(), complete = 0)
        session.add(bullet1)
        session.commit()
        
        response = self.client.post("/bullet/1/delete", data={
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        bullets = session.query(Bullet).all()
        self.assertEqual(len(bullets), 0)

        test_logger.info('I: Delete Bullet Test End')

    #Backlog Migration
    def test_backlog_I(self):
        """ Mass bullet migration of backlog """

        test_logger.info('I: Backlog Test Start')

        date1 = date(2000, 1, 1)
        date2 = date.today()
        
        for i in range (0, 5):
            bullet1 = Bullet(contentType="task", content="yes", date=date1, complete=0)
            bullet2 = Bullet(contentType="note", content="no", date=date1, complete=0)
            session.add_all([bullet1, bullet2])
        session.commit()
        
        bullets = session.query(Bullet).all()
        backlog_list = []
        
        for bullet in bullets:
            backlog_list.append(bullet.id)
        
        self.assertEqual(len(backlog_list), 10)
        
        #How to pass the array of ID's from HTML to Views
        response = self.client.post("/bullet/backlog", data={
            "date": date2,
            "backlog_list": [2,4,6,8,10]
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        bullets1 = session.query(Bullet).filter(Bullet.date == date1).all()
        self.assertEqual(len(bullets1), 5)
        bullets2 = session.query(Bullet).filter(Bullet.date == date2).all()
        self.assertEqual(len(bullets2), 5)

        test_logger.info('I: Backlog Test End')

if __name__ == "__main__":
    unittest.main()
        
    