from flask import render_template
from flask import request, redirect, url_for
from flask import flash
from datetime import datetime, date
from . import app
from .database import session, Bullet

@app.route("/")
@app.route("/<string:date>", methods=["GET"])
def home(currentDate=""):
    #PROBLEM date(Y, d, m)
    #SOLUTION switched to date(Y, m, d)
    #currentDate = date.today()
    
    try:
        #currentDate=request.form["date"]
        currentDate=request.args.get("date")
    except:
        #currentDate = date(2017, 10, 11).strftime('%m/%d/%Y')
        currentDate = date.today()

    
    bullets = session.query(Bullet)
    bullets = bullets.filter(Bullet.date == currentDate)
    bullets = bullets.all()
    
    return render_template("bullets.html",
        bullets=bullets,
        date=currentDate,
        )
    
@app.route("/bullet/add", methods=["GET"])
def add_bullet_get():
    return render_template("addBullet.html")
    
@app.route("/bullet/add", methods=["POST"])
def add_bullet_post():
    bullet = Bullet(
        contentType=request.form["contentType"],
        content=request.form["content"],
        date=request.form["date"]
        )
    session.add(bullet)
    session.commit()
    return redirect(url_for("home"))
        
@app.route("/bullet/<int:ID>/edit", methods=["GET"])
def edit_bullet_get(ID):
    bullet = session.query(Bullet).get(ID)
    return render_template("editBullet.html", bullet=bullet)
    
@app.route("/bullet/<int:ID>/edit", methods=["POST"])
def edit_bullet_post(ID):
    
    bullet = session.query(Bullet).get(ID)
    bullet.contentType = request.form["contentType"]
    bullet.content = request.form["content"]
    bullet.date = request.form["date"]
    
    session.commit()
    return redirect(url_for("home"))
    
@app.route("/bullet/<int:ID>/delete", methods=["GET", "POST"])
def delete_bullet(ID):
    bullet = session.query(Bullet).get(ID)
    session.delete(bullet)
    session.commit()
    
    return redirect(url_for("home"))
    
@app.route("/bullet/search", methods=["GET"])
@app.route("/bullet/search/<string:q>", methods=["GET", "POST"])
def search_bullet_display(q=""):
    try:
            #q = request.form["q"]
            q=request.args.get("q")
    except:
            q="adsfkhdhjdfasjkdfakj"
    
    if q:       
        found = session.query(Bullet).filter(Bullet.content.contains(q))
    else:
        found = session.query(Bullet).all()
        
    return render_template("search_display.html",
        bullets=found
        )
        
@app.route("/bullet/<int:ID>/migrate", methods=["GET"])
def migrate_bullet_get(ID):
    bullet = session.query(Bullet).get(ID)
    return render_template("migrate.html", bullet=bullet)
    
@app.route("/bullet/<int:ID>/migrate", methods=["POST"])
def migrate_bullet_post(ID):
    bullet = session.query(Bullet).get(ID)
    bullet.date = request.form["date"]
    
    session.commit()
    return redirect(url_for("home"))
