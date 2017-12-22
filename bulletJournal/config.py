class DevelopmentConfig(object):
    DATABASE_URI="postgresql://ubuntu:thinkful@localhost:5432/bulletJournal"
    DEBUG = True


class TestingConfig(object):
    DATABASE_URI="postgresql://ubuntu:thinkful@localhost:5432/bulletJournal-test"
    DEBUG = True
    
class TravisConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/bulletJournal-test"
    DEBUG = False
