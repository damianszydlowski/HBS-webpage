# -*- coding: utf-8 -*-
from config import *
from flask import Flask, request, flash, url_for, redirect, render_template, abort, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

#flask config
app = Flask(__name__)
app.config.from_object(FlaskConfig)
db = SQLAlchemy(app)

##initializations
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ""

#imports after init
from routes import *
from models import Guest


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)
    session.modified = True


@login_manager.user_loader
def load_user(id):
    return Guest.query.get(int(id))


@app.errorhandler(401)
def page_not_found(e):
    flash('Musisz się zalogować, aby móc wyświetlić tę stronę')
    return render_template('unauthorized.html'), 401


if __name__ == "__main__":
    app.run()