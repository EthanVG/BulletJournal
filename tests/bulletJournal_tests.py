import unittest
import os
import shutil
import json, html
# try: from urllib.parse import urlparse
# except ImportError: from urlparse import urlparse # Py2 compatibility
from html.parser import HTMLParser
from io import StringIO, BytesIO

import sys; print(list(sys.modules.keys()))
os.environ["CONFIG_PATH"] = "bulletJournal.config.TestingConfig"

from bulletJournal import app
from bulletJournal.database import Base, engine, session

class TestBulletJournal(unittest.TestCase):
    """ Tests for BulletJournal """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)
        
    def test_get_empty_bullets(self):
        """ Getting bullets from an empty database """
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/html")
        
        data = []
        self.assertEqual(data,[])