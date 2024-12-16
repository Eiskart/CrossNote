#cause im doing this on cs50.dev, the only tool im using is CS50 Duck Debugger.

import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from markupsafe import Markup, escape

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL('sqlite:///note.db')

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    id = session['user_id']
    result = db.execute('SELECT content FROM note WHERE id = ?', id)
    if result:
        content = db.execute('SELECT content FROM note WHERE id=?', id)[0]['content']
        return render_template('index.html', content=content)
    else:
        return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            error = 'Please input'
            return render_template('login.html', error= error)
        row = db.execute('SELECT * FROM user WHERE username = ?', username )
        if len(row)!= 1 or not check_password_hash(row[0]['hash'], password):
            error = "User doesnt exist"
            return render_template('login.html', error=error)
        session['user_id'] = row[0]['id']
        return redirect('/')
    else:
        return render_template('login.html', error= None)

@app.route('/register', methods=['POST' ,'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        row = db.execute('SELECT * FROM user WHERE username = ?' , name )
        if not name or not password:
            error = 'Please input'
            return render_template('register.html', error = error)
        elif password != confirm:
            error = 'Password confirmation is incorrect'
            return render_template('register.html', error= error)
        elif len(row) >= 1:
            error = 'Username already existed'
            return render_template('register.html', error = error)
        else:
            hash = generate_password_hash(password)
            db.execute('INSERT INTO user (username, hash) VALUES (?,?)',name ,hash)
            session['user_id'] = db.execute('SELECT id FROM user WHERE username = ?', name)[0]['id']
            return redirect('/')
    else:
        error = 'TIPS: longer passwords are more secured !'
        return render_template('register.html', error = error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/save', methods=['POST'])
@login_required
def save():
    data = request.get_json()
    content = data['content']
    id = session['user_id']
    result = db.execute('SELECT content FROM note WHERE id = ?',id )
    if result:
       db.execute('UPDATE note SET content = ? where id = ?',content,id)
    else:
       db.execute('INSERT INTO note (id , content) VALUES (?, ?)', id, content)
    return 'Success', 200

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        check = request.form.get("change")
        userid = session["user_id"]
        if check == "username" or check == "hash":
            change = check
            return render_template("change.html", change=change)
        elif check == "Cname":
            newname = request.form.get("new")
            try:
                if not newname:
                    error = 'Please input a valid name'
                    username = db.execute('SELECT username FROM user WHERE id=?',userid)[0]['username']
                    return render_template("change.html", error=error, name=username)
                else:
                    db.execute("UPDATE user SET username = ? WHERE id = ?", newname, userid)
            except ValueError:
                error = 'Name already exist'
                username = db.execute('SELECT username FROM user WHERE id=?',userid)[0]['username']
                return render_template("change.html", error=error, name=username)
            return redirect("/")
        elif check == "Cpass":
            oldpass = request.form.get("old")
            newpass = request.form.get("new")
            if not oldpass or not newpass:
                error ='Please input'
                username = db.execute('SELECT username FROM user WHERE id=?',userid)[0]['username']
                return render_template("change.html", error=error, name=username)
            newhash = generate_password_hash(newpass)
            hashcheck = db.execute("SELECT hash FROM user WHERE id = ?", userid)[0]["hash"]
            if not check_password_hash(hashcheck, oldpass):
                error='Old password is incorrect'
                username = db.execute('SELECT username FROM user WHERE id=?',userid)[0]['username']
                return render_template("change.html", error=error, name=username)
            db.execute("UPDATE user SET hash = ? where id = ?", newhash, userid)
            return redirect("/")
    else:
        userid = session["user_id"]
        username = db.execute('SELECT username FROM user WHERE id=?',userid)[0]['username']
        return render_template("change.html", name=username)





if __name__ == '__main__':
    app.run(debug=True)
