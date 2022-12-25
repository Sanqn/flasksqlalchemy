from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project_sqlalchemy.db"
# initialize the app with the extension
db.init_app(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'User id: {self.id}'


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(500))
    id_users = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __str__(self):
        return f'Profiles id: {self.id}'


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html', title='Main page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print('OK')
        try:
            hash_psw = generate_password_hash(request.form['psw'])
            print(hash_psw)
            user = Users(
                email=request.form["email"],
                psw=hash_psw
            )
            print(user.email)
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            prof = Profiles(
                username=request.form["username"],
                old=request.form["old"],
                city=request.form["city"],
                id_users=user.id
            )
            print(prof.username)
            print(prof.old)
            print(prof.id_users)
            db.session.add(prof)
            db.session.commit()
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            print(f'Error add in DB {e}')

    return render_template('register.html', title='Register')


if __name__ == '__main__':
    app.run(debug=True)
