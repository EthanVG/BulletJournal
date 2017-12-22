import os
from flask_script import Manager
from bulletJournal.database import session, Bullet
from datetime import datetime, date

from bulletJournal import app

manager = Manager(app)

@manager.command
def run():
    """ Run the BulletJournal app """
    
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

@manager.command
def seed():
    """ Populate the BulletJournal database with bullets """
    setDate = date(2017, 11, 1).strftime('%d/%m/%Y')

    for i in range(0,5):
        bullet1 = Bullet(contentType="task", content="task", date=setDate, complete=0)
        bullet2 = Bullet(contentType="note", content="note", date=setDate, complete=0)
        bullet3 = Bullet(contentType="event", content="event", date=setDate, complete=0)
        session.add_all([bullet1,bullet2,bullet3])
        session.commit()
    

@manager.command
def removeAll():
    """ Remove all data from the database """
    toRemove = session.query(Bullet).all()
    for item in toRemove:
        session.delete(item)
    session.commit()
    
if __name__ == '__main__':
    manager.run()