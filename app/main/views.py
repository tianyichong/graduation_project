from flask import render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')