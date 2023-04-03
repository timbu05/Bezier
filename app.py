from flask import Flask, render_template, url_for, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from wtforms.validators import InputRequired
from datetime import datetime
from sqlalchemy.sql import func
import graph
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(50))
    Login = db.Column(db.String(50))
    Data = db.Column(db.LargeBinary)
    Time = db.Column(db.DateTime, default = datetime.utcnow)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/', methods=["GET",'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename = file.filename, Data = file.read())

        db.session.add(upload)
        db.session.commit()
        
        graph.draw(f.Data, f.filename)
        return redirect('/')
        
    return render_template("index.html")

@app.route('/vhod', methods=["GET",'POST'] )
def vhod():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()
        login = user.login

        if not user or not check_password_hash(user.password, password):
            flash('Проверьте логин или пароль')
            return redirect('/vhod')
        else:
            return render_template("index_user.html", login=login)
    else:
        return render_template("vhod.html") 

@app.route('/reg', methods=["GET",'POST'])
def reg():
    if request.method == 'POST':
        login = request.form['login']
        email = request.form['email']
        password = request.form['exampleInputPassword']
        
        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email уже используется')
            return redirect('/reg')

        new_user = Users(email=email, login=login, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        return redirect('/vhod')
    else:
        return render_template("reg.html")

@app.route('/user', methods=["GET",'POST'])
def index_user():
    user = Users.query.filter_by().first()
    login = user.login
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename = file.filename, Data = file.read())

        db.session.add(upload)
        db.session.commit()
        
        i_d = upload.id
        f = Upload.query.filter_by(id=i_d).first()
        return graph.draw(f.Data, f.filename), render_template("index_user.html", login=login)
    else:   
        return render_template("index_user.html", login=login)


if __name__ == "__main__":
    app.run()