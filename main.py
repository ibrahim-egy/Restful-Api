from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
db = SQLAlchemy(app)
Bootstrap(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))


@app.route('/', methods=['GET', "POST"])
def home():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['name']).first()
        if user:
            response = make_response(
                jsonify(
                    {"Name": user.username,
                     "password": user.password,
                     "email": user.email,
                     "First-name": user.fname,
                     "Last-name": user.lname,
                     }
                )
            )
            return response
        else:
            flash(f"No Info for This Search: {request.form['name']}")
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
