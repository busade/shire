from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///blog.db"
app.secret_key="ichascnchdcuncducbeduc"

db = SQLAlchemy(app)

migrate = Migrate(app,db)


class Users(db.Model, UserMixin):
    __tablename__ = "users" 
    id = db.Column(db.Integer(), primary_key= True, unique=True)
    username = db.Column(db.String(50),nullable = False, unique = True) 
    email = db.Column(db.String(), nullable = False, unique = True)
    gender = db.Column (db.String(), nullable= False)
    password =db.Column(db.String(), nullable = False)
    
    def __repr__(self):
        return f"User: <{self.username}>"

class Posts(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer(), primary_key = True, unique = True)
    title = db.Column(db.String(), nullable= False, unique = True)
    content = db.Column(db.Text(),nullable = False)
    created_on = db.Column(db.DateTime, default = datetime.datetime.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    author = db.Column(db.String(), nullable = False)
    created_by = db.relationship("Users", backref = "articles_by", lazy = True)

    def __repr__(self):
        return f"Title: <{self.title}>"



with app.app_context():
    db.create_all()

# initializing the login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup',methods=["POST","GET"])
def signup():
    print("one")
    if request.method == "POST":
        print("two")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        gender = request.form.get("gender")

        email_check=Users.query.filter_by(email=email).first()
        user_check= Users.query.filter_by(username=username).first()
        if user_check or email_check:

            return ("user or email already exist")
        new_user = Users(username=username, email =email, password =generate_password_hash(password), gender=gender)
        db.session.add(new_user)
        db.session.commit()
        print("three")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods= ["POST", "GET"])
def login():
    email= request.form.get("email")
    password = request.form.get("password")

    if request.method == "POST":
        email_check= Users.query.filter_by(email=email).first()
        if email_check and check_password_hash(email_check.password,password):
            return redirect (url_for('post'))
        else:
            return ("Invalid Email or password")

    return render_template('login.html')

@app.route('/post')
def post():
    return render_template('post.html')



if __name__ == '__main__':
    app.run(debug=True)