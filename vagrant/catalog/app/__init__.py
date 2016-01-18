from datetime import datetime
from os import path

from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import session, flash, abort, g
from flask.ext.seasurf import SeaSurf

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
csrf = SeaSurf(app)

from app import forms, models, views  # noqa
