from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'