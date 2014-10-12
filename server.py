import sqlite3
import time
from flask import Flask, request, g, render_template, redirect

app = Flask(__name__)
DATABASE = "posts.db"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db 

def db_read_posts():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM dilemmas")
    return cur.fetchall()

def db_add_post(dilemma, option1, option2):
    cur = get_db().cursor()
    t = str(time.time())
    post_info = (dilemma, option1, option2, t, 0, 0, None)
    cur.execute("INSERT INTO dilemmas VALUES (?, ?, ?, ?, ?, ?, ?)", post_info) 
    get_db().commit()

def db_change_vote(user_id, vote):
    cur = get_db().cursor()
    if vote=="option1":
        current_votes = cur.execute("SELECT votes1 FROM dilemmas WHERE id=?", (user_id, ))
        new_votes = current_votes.fetchall()[0][0]+1
        cur.execute("UPDATE dilemmas SET votes1=? WHERE id=?", (new_votes, user_id))
    else:
        current_votes = cur.execute("SELECT votes2 FROM dilemmas WHERE id=?", (user_id, ))
        new_votes = current_votes.fetchall()[0][0]+1
        cur.execute("UPDATE dilemmas SET votes2=? WHERE id=?", (new_votes, user_id))
    get_db().commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/api/vote/<user_id>/<curr_display>", methods=["POST"])
def addvote(user_id, curr_display):
    db_change_vote(user_id, request.form['vote'])
    path = "/api/show/" + str(int(curr_display)-10)
    return redirect(path)

@app.route("/")
@app.route("/api/show/<last_show_amt>")
def index(last_show_amt=0):
    dilemmas = db_read_posts()
    show = 10 + int(last_show_amt)
    return render_template('index.html', dilemmas=dilemmas, display=show)


@app.route("/api/dilemma/<curr_display>", methods=["POST"])
def receive_post(curr_display):
    db_add_post(request.form['dilemma'],request.form['option1'],request.form['option2'])
    path = "/api/show/" + str(int(curr_display)-10)
    return redirect(path)

if __name__ == "__main__":
    app.run()
