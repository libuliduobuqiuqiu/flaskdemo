# coding: utf-8

"""
    :date: 2023-11-3
    :author: linshukai
    :description: About Flasker's Auth Module
"""

from functools import wraps
from flask import g, redirect, url_for, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
import uuid

from flasker.model import User
from flasker import db


def create_user(username: str, password: str):
    err = None
    try:
        user = User(id=str(uuid.uuid1()), name=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

    except IntegrityError:
        err = "Name已存在，请重新注册"
        db.session.rollback()

    except Exception as e:
        err = e
        db.session.rollback()

    return err


def verify_user(username: str, password: str):
    err = None
    user = User.query.filter(User.name == username).first()

    if user is None:
        err = 'Incorrect username.'
    elif not check_password_hash(user.password, password):
        err = 'Incorrect password.'

    if err is None:
        session.clear()
        session['user_id'] = user.id
        return None

    return err


def login_required(view):
    @wraps(view)
    def wrap_view(*args, **kwargs):
        if g.user is None:
            abort(400)

        return view(*args, **kwargs)

    return wrap_view
