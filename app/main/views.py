from flask import render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from . import main
from .. import db, login_manager
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/instruction_candidates', methods=['GET', 'POST'])
def instruction_candidates():
    return render_template('instruction_candidates.html')


@main.route('/register_process', methods=['GET', 'POST'])
def register_process():
    return render_template('register_process.html')


@main.route('/pay_process', methods=['GET', 'POST'])
def pay_process():
    return render_template('pay_process.html')


@main.route('/commit', methods=['GET', 'POST'])
def commit():
    return render_template('commit.html')

