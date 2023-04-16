from flask import *
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
from cryptography.fernet import Fernet

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
        return self.authenticated

login_manager = LoginManager()
login_manager.login_view = 'vhod'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/', methods=["GET",'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename = file.filename, Data = file.read(), Login = session['login'])

        db.session.add(upload)
        db.session.commit()
        
        i_d = upload.id
        
        f = Upload.query.filter_by(id=i_d).first()
        
        graph.draw(f.Data, f.filename)
        return redirect('/gr')
        

    else:   
        return render_template("index.html")
        

@app.route('/vhod', methods=["GET",'POST'] )
def vhod():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()
    

        if not user or not check_password_hash(user.password, password):
            flash('Проверьте логин или пароль')
            return redirect('/vhod')
        else:
            session['login'] = user.login
            session['email'] = user.email
            session['password'] = password
            session['id'] = user.id
            return redirect('/user_page')
    else:
        return render_template("vhod.html") 

@app.route('/reg', methods=["GET",'POST'])
def reg():
    if request.method == 'POST':
        login = request.form['login']
        email = request.form['email']
        password = request.form['exampleInputPassword']
        password1 = request.form['exampleInputPassword1']
        
        user_email = Users.query.filter_by(email=email).first()
        user_login = Users.query.filter_by(login=login).first()
        if user_email:
            flash('Email уже используется')
            return redirect('/reg')
        if user_login:
            flash('Логин уже используется')
            return redirect('/reg')
        if password != password1:
            flash('Пароли не совпадают')
            return redirect('/reg')
            
        new_user = Users(email=email, login=login, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        return redirect('/vhod')
    else:
        return render_template("reg.html")

@app.route('/user_page', methods=["GET",'POST'])
def index_user():
    user = Users.query.filter_by(login=session["login"]).first()
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename = file.filename, Data = file.read(), Login = user.login)

        db.session.add(upload)
        db.session.commit()
        
        i_d = upload.id
        f = Upload.query.filter_by(id=i_d).first()
        print(f.filename)
        graph.draw(f.Data, f.filename)
        return redirect('/gr')
    else:   
        return render_template("index_user.html")
    

@app.route('/profile', methods=["GET",'POST'] )
def profile():
    files = Upload.query.filter_by(Login=session['login']).all()
    users = Users.query.order_by(Users.id).all()
    cur_user = Users.query.get(session['id'])

    if request.method == 'POST':
            cur_user.login = request.form['login']
            cur_user.email = request.form['email']
            cur_user.password = generate_password_hash(request.form['password'], method='sha256')
            session['login'] = cur_user.login
            session['email'] = cur_user.email
            session['password'] = request.form['password']
            session['id'] = cur_user.id 
        
            for el in files:
                el.Login = request.form['login']


            db.session.commit()
            return redirect('/profile')

    else:
        return render_template('profile.html', users=users, files=files)


@app.route('/view_user',methods=["GET"]) 
def view_user():
    if request.method == 'GET':
        if request.args.get('login') is None:
            return render_template('permissionerror.html')
        else:
            user = db.session.execute(db.select(Users).where(Users.login == request.args.get('login')))
            if user is None:
                return render_template('permissionerror.html')
            else:
                user = user.all()[0][0]
                files = Upload.query.filter_by(Login=user.login).all()
                users = Users.query.order_by(Users.id).all()
                return render_template('view_user.html', users=users, files=files, userlogin = user.login, useremail = user.email)





@app.route('/download/<path:filename>')
def download(filename):
    f = Upload.query.filter_by(filename=filename).first()
    graph.draw(f.Data,f.filename)
    return redirect("/gr")

@app.route('/gr', methods=["GET","POST"] )
def gr():
    return render_template("gr.html")

if __name__ == "__main__":
    app.run()