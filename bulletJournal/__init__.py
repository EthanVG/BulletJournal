import os
from flask import Flask
import logging

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "bulletJournal.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import views
from . import filters
from . import api


formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
    
# APP LOGGER
app_logger = setup_logger('app_logger', 'app.log')


# TEST LOGGER
test_logger = setup_logger('test_logger', 'test.log')

