import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
    date = db.Column(db.DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __str__(self):
        return f'User id: {self.id}'


class profiles(db.Model):
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
    return 'Flask started'


if __name__ == '__main__':
    app.run(debug=True)
