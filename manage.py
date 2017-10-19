import os
from flask_script import Manager
from bulletJournal.database import session, Bullet
from datetime import datetime, date
#from bulletJournal.models import Bullet

from bulletJournal import app

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

@manager.command
def seed():
    setDate = date.today()
    setDate = setDate.strftime('%d/%m/%Y')
    
    bullet1 = Bullet(contentType = "task", content = "This is a test", date=setDate)
    bullet2 = Bullet(contentType = "event", content = "This is a test again", date=setDate)
    bullet3 = Bullet(contentType = "note", content = "This is a test yet again again", date=setDate)
    session.add_all([bullet1, bullet2, bullet3,])
    session.commit()
    #TD ADD DATE TO SEED
    
@manager.command
def removeAll():
    toRemove = session.query(Bullet).all()
    for item in toRemove:
        session.delete(item)
    session.commit()
    
if __name__ == '__main__':
    manager.run()