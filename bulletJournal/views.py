from flask import render_template
from flask import request, redirect, url_for
from flask import flash
from datetime import datetime, date
from . import app
from .database import session, Bullet

@app.route("/", methods=["GET"])
@app.route("/page/<int:page>", methods=["GET"])
def home(page=1):
    """ Displays bullets for the selected date, default to the current date """
    
    #PROBLEM date(Y, d, m)
    #SOLUTION switched to date(Y, m, d)
    print(request.args.get("date"))
    currentDate = request.args.get("date")
    
    if currentDate == "" or currentDate is None:
        currentDate=date.today().strftime("%m/%d/%Y")
    
    PAGINATE_BY=10
    page_index = page - 1
    try:
        count = session.query(Bullet).filter(Bullet.complete == 0).count()
    except:
        session.rollback()
        count = session.query(Bullet).filter(Bullet.complete == 0).count()
        
    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0
    
    bullets = session.query(Bullet)
    bullets = bullets.filter(Bullet.date == currentDate)
    bullets = bullets.filter(Bullet.complete == 0)
    bullets = bullets.all()
    bullets = bullets[start:end]
    
    return render_template("bullets.html",
        bullets=bullets,
        date=currentDate,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
        )
    
@app.route("/bullet/add", methods=["GET"])
def add_bullet_get():
    """ Returns page for Add Bullet """
    
    return render_template("addBullet.html")
    
@app.route("/bullet/add", methods=["POST"])
def add_bullet_post():
    """ Adds a bullet """
    
    bullet = Bullet(
        contentType=request.form["contentType"],
        content=request.form["content"],
        date=request.form["date"],
        complete=0
        )
    session.add(bullet)
    session.commit()
    return redirect(url_for("home"))
        
@app.route("/bullet/<int:ID>/edit", methods=["GET"])
def edit_bullet_get(ID):
    """ Returns the Edit Bullet page with selected bullet """
    """ :param ID: ID for selected bullet """
    
    bullet = session.query(Bullet).get(ID)
    return render_template("editBullet.html", bullet=bullet)
    
@app.route("/bullet/<int:ID>/edit", methods=["POST"])
def edit_bullet_post(ID):
    """ Edits selected bullet """
    """ :param ID: ID for selected bullet """
    
    bullet = session.query(Bullet).get(ID)
    bullet.contentType = request.form["contentType"]
    bullet.content = request.form["content"]
    bullet.date = request.form["date"]
    
    session.commit()
    return redirect(url_for("home"))
    
@app.route("/bullet/<int:ID>/delete", methods=["GET", "POST"])
def delete_bullet(ID):
    """ Deletes the selected bullet """
    """ :param ID: ID for selected bullet """
    
    bullet = session.query(Bullet).get(ID)
    session.delete(bullet)
    session.commit()
    
    return redirect(url_for("home"))
    
@app.route("/bullet/search", methods=["GET"])
@app.route("/bullet/search/page/<int:page>", methods=["GET", "POST"])
def search_bullet_display(page=1):
    """ Searches database with bullets whose content contains q """
    """ :param q: search query from user """
        
    q=request.args.get("q", type=str)
        #if q == None:
        #    q = "alskdjhfalskdjfhlhakd"
    
    if q:       
        found = session.query(Bullet).filter(Bullet.content.contains(q))
        found = found.filter(Bullet.complete == 0)
    else:
        found = session.query(Bullet).filter(Bullet.complete == 0)
    
    PAGINATE_BY=10
    page_index = page - 1

    count = found.count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0
    
    found = found[start:end]
    
    return render_template("search_display.html",
        bullets=found,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages,
        q=q
        )
        
        
@app.route("/bullet/<int:ID>/migrate", methods=["GET"])
def migrate_bullet_get(ID):
    """ Returns Migrate page for selected bullet """
    """ :param ID: ID for selected bullet """
    
    bullet = session.query(Bullet).get(ID)
    return render_template("migrate.html", bullet=bullet)
    
@app.route("/bullet/<int:ID>/migrate", methods=["POST"])
def migrate_bullet_post(ID):
    """ Migrates selected bullet to selected date """
    """ :param ID: ID for selected bullet """
    
    bullet = session.query(Bullet).get(ID)
    bullet.migrate(request.form["date"])
    session.commit()
    
    session.commit()
    return redirect(url_for("home"))

@app.route("/bullet/<int:ID>/complete", methods=["GET", "POST"])
def complete_bullet(ID):
    """ Marks bullet as completed """
    """ :param ID: ID for selected bullet """
    
    bullet = session.query(Bullet).get(ID)
    bullet.complete = 1
    session.commit()
    
    return redirect(url_for("home"))
    
@app.route("/bullet/backlog", methods=["GET"])
def backlog_get():
    """ Returns the backlog migration page """
    
    bullets = session.query(Bullet).all()
    found = []
    
    for bullet in bullets:
        if bullet.date < date.today():
            found.append(bullet)
            
    return render_template("backlog.html", bullets=found)
    
@app.route("/bullet/backlog", methods=["POST"])
def backlog_post():
    """ Changes set date of selected bullets """
    
    backlog_list = request.form.getlist("backlog_list")
    toDate = request.form["date"]
    
    if toDate is "" or None:
        toDate = date.today()
        newMonth = toDate.month
        if newMonth == 12:
            newMonth = 1
        else:
            newMonth += 1
        toDate = toDate.replace(newMonth)
        
    for ID in backlog_list:
        
        bullet = session.query(Bullet).get(ID)
        bullet.migrate(toDate)
    
    session.commit()
    return redirect(url_for("home"))
    
    
    
