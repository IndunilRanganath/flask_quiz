# 2.13
# # Ctrl + D ebuwama eka wage wachana hightlight karnna puluwan

# from crypt import methods
from distutils.log import error
from unicodedata import name
from urllib import request
from database import connect_to_database,getDatabase
from flask import Flask, redirect, render_template, url_for, request, g, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] =  os.urandom(24)

@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'quizapp_db'):
        g.quizapp_db.close()

def get_current_user():
    user_result = None
    if 'user' in session:
        user = session['user']
        db = getDatabase()
        user_cursor = db.execute("select * from users where name = ?",[user])
        user_result = user_cursor.fetchone()
    return user_result



@app.route('/')
def index():
    user = get_current_user()
    return render_template("home.html", user = user)

@app.route('/login', methods = ["POST", "GET"])
def login():
    user = get_current_user()
    error = None
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        db = getDatabase()
        fetchedperson_cursor = db.execute("select * from users where name = ?",[name])
        personfromdatabase = fetchedperson_cursor.fetchone()
        if personfromdatabase:
            if check_password_hash(personfromdatabase['password'],password):
                session['user'] = personfromdatabase['name']
                return redirect(url_for('index'))
            else:
                error = "Username or Password is invalid. Try again."
                return render_template('login.html', error = error)
        else:
            error = "Username or Password is invalid. Try again."
            return redirect(url_for('login'))        
    return render_template("login.html", user = user, error = error)




@app.route('/register', methods=["POST","GET"])
def register():
    user = get_current_user()
    if request.method == "POST":
        db = getDatabase()
        name = request.form['name']
        password = request.form['password']
        hash_password = generate_password_hash(password, method='sha256')
        db.execute("insert into users (name, password,teacher,admin) values (?,?,?,?)",
        [name, hash_password,'0','0'])
        db.commit()
        session['user'] = name
        return redirect(url_for('index'))
    return render_template("register.html", user = user)


@app.route('/askquestions')
def askquestions():
    user = get_current_user()
    return render_template("askquestions.html", user = user)

@app.route('/answerquestions')
def answerquestions():
    user = get_current_user()
    return render_template("answerquestions.html", user = user)


@app.route('/allusers', methods =["POST","GET"])
def allusers():
    user = get_current_user()
    db = getDatabase()
    user_cursor = db.execute("select * from users")
    allusers = user_cursor.fetchall()
    return render_template("allusers.html", user = user, allusers = allusers)

@app.route('/promote/<int:id>',  methods = ["POST","GET"])
def promote(id):
    user =  get_current_user()
    if request.method == "GET":
        db =  getDatabase()
        db.execute("update users set teacher = 1 where id = ?", [id])
        db.commit()
        return redirect(url_for('allusers'))
    return render_template("allusers.html",  user = user)





@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
