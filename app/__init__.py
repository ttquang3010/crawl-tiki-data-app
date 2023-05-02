import os

from flask import Flask, session
from flask_session import Session
from datetime import timedelta

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'app/setup/fresher-training-02-9bba1703c510.json'
app = Flask(__name__)
app.secret_key = "Tiki Crawl Data"

# Configure the app to use sessions
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_TYPE'] = 'filesystem'

# Set session lifetime to 15 minutes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
Session(app)

from .views.home import *
from .views.preview import *
from .views.result import *
from .views.invalid_route import *